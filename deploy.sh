#!/usr/bin/env bash
set -euo pipefail

# ── Couleurs ──
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()  { echo -e "${GREEN}[INFO]  $*${NC}"; }
warn()  { echo -e "${YELLOW}[WARN]  $*${NC}"; }
error() { echo -e "${RED}[ERROR] $*${NC}"; exit 1; }

# ── Pré-requis ──
for cmd in terraform ansible-playbook az ssh; do
  command -v "$cmd" &>/dev/null || error "$cmd n'est pas installé"
done

info "=== Déploiement DevOps Task Manager ==="

# ── Azure login ──
if ! az account show &>/dev/null; then
  warn "Connexion Azure nécessaire..."
  az login
fi
info "Subscription : $(az account show --query name -o tsv)"

# ── Variables ──
GHCR_USER="Brendan-bx"
read -rp "Mot de passe Grafana admin [admin123] : " GRAFANA_PASS
GRAFANA_PASS=${GRAFANA_PASS:-admin123}

# ── 1. Terraform ──
info "Étape 1/3 — Création de l'infrastructure (Terraform)..."
cd terraform
terraform init -input=false
terraform apply -auto-approve

VM_IP=$(terraform output -raw vm_public_ip)
ADMIN_USER=$(terraform output -raw admin_username)
cd ..

info "VM créée : $VM_IP"

# ── 2. Attente SSH ──
info "Étape 2/3 — Attente de la VM..."
for i in $(seq 1 20); do
  if ssh -i terraform/ssh_key.pem -o StrictHostKeyChecking=no -o ConnectTimeout=10 "${ADMIN_USER}@${VM_IP}" "echo ok" &>/dev/null; then
    break
  fi
  warn "Tentative SSH $i/20..."
  sleep 15
done

# ── 3. Ansible ──
info "Étape 3/3 — Configuration de la VM (Ansible)..."

cat > ansible/inventory.ini <<EOF
[vm]
${VM_IP} ansible_user=${ADMIN_USER} ansible_ssh_private_key_file=../terraform/ssh_key.pem ansible_ssh_common_args='-o StrictHostKeyChecking=no'
EOF

EXTRA=("ghcr_user=${GHCR_USER}" "grafana_admin_password=${GRAFANA_PASS}")

cd ansible
ansible-playbook -i inventory.ini playbook.yml -e "${EXTRA[*]}"
cd ..

info "==========================================="
info "  ✅  Déploiement terminé !"
info "==========================================="
info "  App        → http://${VM_IP}:5000/health"
info "  Grafana    → http://${VM_IP}:3000"
info "  Prometheus → http://${VM_IP}:9090"
info "  SSH        → ssh -i terraform/ssh_key.pem ${ADMIN_USER}@${VM_IP}"
info "==========================================="

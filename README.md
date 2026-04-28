# 🚀 DevOps Task Manager

API Flask de gestion de tâches, déployée sur Azure VM avec une pipeline
CI/CD complète, du monitoring et de l'Infrastructure-as-Code.

## Stack technique

| Composant       | Technologie                        |
|-----------------|------------------------------------|
| Application     | Python 3.11 / Flask / Gunicorn     |
| Conteneur       | Docker + Docker Compose            |
| Registry        | GitHub Container Registry (GHCR)   |
| CI/CD           | GitHub Actions                     |
| Qualité de code | SonarCloud                         |
| Monitoring      | Prometheus · Promtail · Loki · Grafana |
| IaC             | Terraform (Azure VM)               |
| Configuration   | Ansible                            |
| Cloud           | Microsoft Azure (compte étudiant)  |

---

## Git Flow

```text
main ─────────────────────────●────────────● (tags: v1.0, v1.1)
                             ╱            ╱
develop ──●──●──●──●──●─────●────●──●────●
          ╲        ╲        ╱
feature/   ●──●──●  ●──●──●
```

### Branches

| Branche       | Rôle                                     |
|---------------|------------------------------------------|
| `main`        | Production — toujours stable             |
| `develop`     | Intégration des features                 |
| `feature/*`   | Développement d'une fonctionnalité       |
| `release/*`   | Préparation d'une version                |
| `hotfix/*`    | Correctif urgent sur production          |

### Workflow quotidien

```bash
# 1. Créer une feature
git checkout develop
git pull origin develop
git checkout -b feature/ma-feature

# 2. Travailler, committer
git add . && git commit -m "feat: ajout endpoint X"

# 3. Pousser et créer une Pull Request → develop
git push origin feature/ma-feature
# → Ouvrir une PR sur GitHub, la CI se lance automatiquement

# 4. Après review + CI verte, merge dans develop

# 5. Release
git checkout -b release/1.0 develop
# → Tests finaux, puis merge dans main ET develop
git tag -a v1.0 -m "Version 1.0"
git push origin main --tags
```

### Branch Protection (GitHub Settings)

- **main** : PR obligatoire, 1 review minimum, CI must pass
- **develop** : PR obligatoire, CI must pass

---

## Répartition du travail (4 membres)

| Membre   | Responsabilités                              |
|----------|----------------------------------------------|
| Membre 1 | Application Flask + Tests + Dockerfile       |
| Membre 2 | CI/CD GitHub Actions + SonarCloud            |
| Membre 3 | Monitoring (Prometheus, Promtail, Grafana)   |
| Membre 4 | Terraform + Ansible + script de déploiement  |

---

## Démarrage rapide

### Pré-requis

- Python 3.11+, Docker, Terraform ≥ 1.5, Ansible, Azure CLI

### Développement local

```bash
# Lancer toute la stack
docker compose up -d --build

# Endpoints
# App        → http://localhost:5000/health
# Prometheus → http://localhost:9090
# Grafana    → http://localhost:3000  (admin/admin)
```

### Tests

```bash
pip install -r requirements-dev.txt
pytest --cov=app
flake8 app/ tests/
```

### Déploiement Azure

```bash
az login
./deploy.sh
```

---

## Secrets GitHub à configurer

| Secret          | Obligatoire | Description                          |
|-----------------|-------------|--------------------------------------|
| `SONAR_TOKEN`   | CI          | Token SonarCloud                     |
| `VM_HOST`       | CD deploy   | IP publique de la VM Azure           |
| `VM_USERNAME`   | CD deploy   | Utilisateur SSH (ex: azureuser)      |
| `VM_SSH_KEY`    | CD deploy   | Clé privée SSH (contenu du .pem)     |

### Rendre l'image GHCR publique (recommandé)

1. Aller dans GitHub → Packages → devops-taskmanager
2. Package Settings → Change visibility → Public

---

## Destruction de l'infrastructure

```bash
cd terraform
terraform destroy -auto-approve
```

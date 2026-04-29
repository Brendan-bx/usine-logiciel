#!/usr/bin/env bash
az vm run-command invoke \
  --name devops-tm-vm \
  --resource-group devops-tm-rg \
  --command-id RunShellScript \
  --scripts "systemctl status sshd && echo '===' && ss -tlnp | grep 22 && echo '===' && ufw status"

az policy assignment list --query "[].displayName" -o tsv
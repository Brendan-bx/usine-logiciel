output "vm_public_ip" {
  description = "Adresse IP publique de la VM"
  value       = azurerm_public_ip.main.ip_address
}

output "admin_username" {
  description = "Utilisateur SSH"
  value       = var.admin_username
}

output "ssh_command" {
  description = "Commande SSH rapide"
  value       = "ssh -i ${local_file.ssh_private_key.filename} ${var.admin_username}@${azurerm_public_ip.main.ip_address}"
}

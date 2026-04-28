variable "project_name" {
  description = "Préfixe pour toutes les ressources"
  type        = string
  default     = "devops-tm"
}

variable "location" {
  description = "Région Azure"
  type        = string
  default     = "francecentral"
}

variable "vm_size" {
  description = "Taille de la VM"
  type        = string
  default     = "Standard_B2s" # 2 vCPU, 4 Go RAM — compatible compte étudiant
}

variable "admin_username" {
  description = "Utilisateur admin SSH"
  type        = string
  default     = "azureuser"
}

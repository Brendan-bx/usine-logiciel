variable "project_name" {
  description = "Préfixe pour toutes les ressources"
  type        = string
  default     = "devops-tm"
}

variable "location" {
  description = "Région Azure"
  type        = string
  default     = "swedencentral"
}

variable "vm_size" {
  description = "Taille de la VM"
  type        = string
  default     = "Standard_B2ls_v2"
}

variable "admin_username" {
  description = "Utilisateur admin SSH"
  type        = string
  default     = "azureuser"
}

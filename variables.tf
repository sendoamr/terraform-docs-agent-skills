variable "name" {
  description = "Nombre del bucket"
  type        = string
}

variable "location" {
  description = "Región del bucket"
  type        = string
  default     = "EU"
}

variable "versioning" {
  description = "Activar versionado"
  type        = bool
  default     = false
}
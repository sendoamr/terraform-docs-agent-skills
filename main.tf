resource "google_storage_bucket" "bucket" {
  name     = var.name
  location = var.location

  uniform_bucket_level_access = true

  versioning {
    enabled = var.versioning
  }
}
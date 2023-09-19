terraform {
  required_providers {
    synthetics = {
      source  = "splunk/synthetics"
      version = "2.0.0"
    }
  }
}

provider "synthetics" {
  product = "observability"
  realm   = "us1"
  apikey  = var.apikey
}

variable "apikey" {
  description = "API key for the synthetics provider"
  type        = string
}
variable "tests" {
  type = list(object({
    name          = string
    url           = string
    location_ids  = list(string)
    frequency     = string
    type          = string
  }))
  default = []
}

resource "synthetics_create_http_check_v2" "http_check" {
  for_each = { for idx, test in var.tests : idx => test }

  test {
    name                = each.value.name
    url                 = each.value.url
    location_ids        = each.value.location_ids
    frequency           = each.value.frequency
    type                = each.value.type
    
    active              = true  # or false, depending on your requirement
    verify_certificates = true  # or false, depending on your requirement
    request_method      = "GET"  # or "POST", "PUT", etc., depending on your requirement
    # ... other fields
  }
}



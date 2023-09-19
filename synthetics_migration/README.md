# Synthetics Test Automation Project

In the fast-paced world of technology, migrating synthetic tests manually from one tool to another can be both time-consuming and prone to errors. This project provides a seamless solution to these challenges, facilitating the bulk migration of synthetic tests from various tools to Splunk Observability. Leveraging the capabilities of Python and Terraform, this automation tool not only saves substantial time but also minimizes the possibility of human errors during the migration process.

Here are the key benefits of using this automation tool:

1. Efficiency: Drastically reduces the time and effort required in the manual migration of synthetic tests.
2. Accuracy: By automating the process, it minimizes the chances of human errors, ensuring a more accurate migration.
3. Simplicity: Easy to set up and use, making the process of migrating to Splunk Observability straightforward and hassle-free.
4. Customization: Allows for customization of test configurations through a simple CSV file format, offering flexibility in migration setups.

With this tool, you can swiftly transition to Splunk Observability, capitalizing on its advanced features and functionalities without the hassle of manual setup. Follow the guidelines outlined in this README to get started with your hassle-free migration journey.

## Table of Contents

- [Synthetics Test Automation Project](#synthetics-test-automation-project)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Getting Started](#getting-started)
    - [Usage Guide](#usage-guide)
    - [Project Structure](#project-structure)
    - [Contributing](#contributing)
    - [License](#license)

## Prerequisites

Ensure you have the following software installed on your system:

- Python (version 3.x)
- Terraform (version 1.x)
- A configured Splunk Synthetics account

## Getting Started

Clone the repository to your local machine and navigate to the project directory.


```sh
git clone <repository_url>
cd <repository_directory>
Python Script: test_automation.py
```
The test_automation.py script reads test configurations from a CSV file, converts them to a structured JSON format, and writes this data to a .tfvars.json file, which is then used by the Terraform script to set up synthetics tests.

Usage
1. Create a CSV file named 'tests.csv' with the following columns:
Test Name,URL,Locations,Polling Interval,Test Type
2. Run the Script:
python test_automation.py
This will generate a variables.tfvars.json file in the specified directory.
Terraform Script
The Terraform script utilizes the splunk/synthetics provider to create synthetics tests based on the data generated by the Python script. The script sets up HTTP checks using the provided data.

Configuration
Here is an outline of the terraform.tf configuration file:

```sh
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
    
    active              = true  
    verify_certificates = true  
    request_method      = "GET"  
    # ... other fields
  }
}

```
### Usage Guide
Setup the necessary environment variables.
Run the Python script to generate the JSON data.
Run the Terraform script to set up the synthetics tests.

### Project Structure
Below is a brief description of the main files and directories in this project:

`test_atuomation.py`: This Python script reads test configurations from a CSV file, converts them to a structured JSON format, and writes this data to a .tfvars.json file.

`terraform.tf`: This is the main configuration file for Terraform, which sets up the necessary providers and resources based on the data generated by the Python script.

`variables.tfvars.json`: This file is generated by the test_automation.py script and contains the structured data needed to create the synthetics tests using Terraform.

`tests.csv`: A template CSV file where users can input the details of the tests they want to set up. The necessary columns are: Test Name, URL, Locations, Polling Interval, and Test Type.

`terraform.tfvars`: File where one of the crucial variable `apikey` is stored to authenticate the API calls with Splunk observability. 

### Contributing
If you'd like to contribute to the project, please fork the repository, create a new branch, make your changes, and submit a pull request.

### License
Include any information about the project's license here (if applicable).
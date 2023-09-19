import csv
from subprocess import call
import json

# Open the CSV file
with open('tests.csv', 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    
    # Create a list to hold all the test configurations
    tests = []
    
    # Loop through each row in the CSV file
    for row in csv_reader:
        
        # Create a dictionary with the values from the CSV row
        test_config = {
            "name": row['Test Name'],
            "url": row['URL'],
            "location_ids": [x.strip() for x in row['Locations'].split(',')],
            "frequency": row['Polling Interval'],
            "type": row['Test Type']
        }
        
        # Append the test config to the list of tests
        tests.append(test_config)

# Convert the list of tests to JSON
# Assuming tests is a list of dictionaries like the one you showed in the example
tests_json = json.dumps({"tests": tests}, indent=4)

# ... (rest of your script)

# Write the JSON string to a .tfvars file
tfvars_file_path = '/Users/rohits/Documents/Engagements/Invesco/synthetics/test_automation/variables.tfvars.json'
with open(tfvars_file_path, 'w') as tfvars_file:
    tfvars_file.write(tests_json)
        
# Initialize and apply the Terraform configuration
call(["terraform", "init"])
call(["terraform", "apply", "-var-file=variables.tfvars.json", "-auto-approve"])


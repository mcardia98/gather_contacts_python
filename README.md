# Gather Contacts
A Python re-implementation of clr2of8/GatherContacts, minus Burp.  Google's continuous scrolling broke the tool, hence the re-implementation.

Scrapes LinkedIn for a specified company.  Optionally output a file with all names, position, and emails found.  Company name provided must come from their LinkedIn URL

EX: https://www.linkedin.com/company/test-company/

The -c argument would take "Test Company" as its value.

Tool then finds the number of employees on the target company's LinkedIn page and scrapes Google for their information.

By default, finds all number of employees on the target company's LinkedIn page, plus an additional 10 employees for additional coverage.

Supports txt and csv output.


## Installation
```
pip3 install -r requirements.txt
```
## Usage
```
usage: gather_contacts.py [-h] -c COMPANY -f FORMAT -d DOMAIN [-o [OUTPUT_FILE ...]] [-n NUM_EMPLOYEES]

Scrapes LinkedIn company for possible valid employees. By default, finds number of employees on company LinkedIn page and grabs number of
employees + 10 for additional coverage. Must verify valid employees.

options:
  -h, --help            show this help message and exit
  -c COMPANY, --company COMPANY
                        Company name as found on LinkedIn URL (excluding hyphens) to scrape.
  -f FORMAT, --format FORMAT
                        Email Format Type: 
                          1 - FirstInitial-LastName 
                          2 - FirstName-LastInitial 
                          3 - FirstName-LastName 
                          4 - FirstInital-Dot-LastName 
                          5 - FirstName-Dot-LastInitial 
                          6 - FirstName-Dot-LastName
  -d DOMAIN, --domain DOMAIN
                        Email Address domain, ex company.com
  -o [OUTPUT_FILE ...], --output-file [OUTPUT_FILE ...]
                        Optional output file, ex: company_scrape.txt,company_scrape.csv company_scrape.txt company_scrape.csv Otherwise
                        prints results to terminal.
  -n NUM_EMPLOYEES, --num-employees NUM_EMPLOYEES
                        Optional number of employees to scrape, ex 49, otherwise grabs all employees found on LinkedIn.
```

## Limitations
CANNOT be run as root.  Currently debugging

## TODO
Large companies may trigger a temporary IP ban and require a captcha.  Tool may fail due to timeout, looking to catch the timeout and write results gathered.

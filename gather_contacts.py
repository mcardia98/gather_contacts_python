import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re 
import time
import math
import csv as CSV

parser = argparse.ArgumentParser(description="""Scrapes LinkedIn company for possible valid employees.\n
								By default, finds number of employees on company LinkedIn page and grabs\n
								number of employees + 10 for additional coverage.  Must verify valid employees.\n""")
parser.add_argument('-c', '--company', type=str, nargs=1, required=True,
                    help='Company name as found on LinkedIn URL (excluding hyphens) to scrape.')
parser.add_argument('-f', '--format', type=int, nargs=1, required=True,
					help="""Email Format Type:\n
					1 - FirstInitial-LastName\n 
					2 - FirstName-LastInitial\n
					3 - FirstName-LastName\n
					4 - FirstInital-Dot-LastName\n
					5 - FirstName-Dot-LastInitial\n
					6 - FirstName-Dot-LastName""")
parser.add_argument('-d', '--domain', type=str, nargs=1, required=True,
					help='Email Address domain, ex company.com')
parser.add_argument('-o', '--output-file', type=str, nargs='*', required=False,
					help="""Optional output file, ex:
					company_scrape.txt,company_scrape.csv
					company_scrape.txt
					company_scrape.csv
					Otherwise prints results to terminal.""")
parser.add_argument('-n', '--num-employees', type=int, nargs=1, required=False, default=None,
					help="Optional number of employees to scrape, ex 49, otherwise grabs all employees found on LinkedIn.")
args = parser.parse_args()
csv = False
txt = False
file_name = args.output_file
if(len(file_name)>2):
	parser.error("More than 2 output files specified.")
if(len(file_name)==1):
	if(',' in file_name[0]):
		file_name = file_name[0].split(',')
	else:	
		file_name = args.output_file[0]
		file_format = file_name.split(".")[1]
		if('csv' not in file_format and 'txt' not in file_format):
			parser.error("Invalid file format, txt or csv.")
		elif('csv' in file_format):
			csv = True
			csv_file = open(file_name, 'w', newline='')
			csv_writer = CSV.writer(csv_file, dialect='excel',delimiter=',')
			header = ["Name", "Position", "Email"]
			csv_writer.writerow(header)
		elif('txt' in file_format):
			txt = True
			txt_file = open(file_name,"w")
			txt_file.write("Name" + "\t" + "Position" + "\t" + "Email\n")
if(len(args.output_file)>1):
	for x in file_name:
		file_name = x
		file_format = file_name.split(".")[1]
		if('csv' not in file_format and 'txt' not in file_format):
			parser.error("Invalid file format, txt or csv.")
		elif('csv' in file_format):
			csv = True
			csv_file = open(file_name, 'w', newline='')
			csv_writer = CSV.writer(csv_file, dialect='excel',delimiter=',')
			header = ["Name", "Position", "Email"]
			csv_writer.writerow(header)
		elif('txt' in file_format):
			txt = True
			txt_file = open(file_name,"w")
			txt_file.write("Name" + "\t" + "Position" + "\t" + "Email\n")
email_format = args.format[0]
email_domain = args.domain[0].strip("@")

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options,service=ChromeService(ChromeDriverManager().install()))

# Go to company site and get employee count
driver.get('http://google.com')
if(args.num_employees[0] == None):	
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'q')))
	driver.find_element(By.NAME,'q').send_keys("site:linkedin.com " + args.company[0] + Keys.ENTER)
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'linked')))
	driver.find_element(By.PARTIAL_LINK_TEXT, 'linked').click()
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'employee')))
	num_employees = driver.find_element(By.PARTIAL_LINK_TEXT, 'employee')
	num_employees = re.sub("[^0-9]", "", num_employees.text)
	driver.get('http://google.com')
else:
	num_employees = args.num_employees[0]
driver.find_element(By.NAME,'q').send_keys("site:linkedin.com/in " + args.company[0] + Keys.ENTER)
time.sleep(1)
for x in range(0,math.ceil(int(num_employees)/10)+1):
	driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
	time.sleep(0.5)
	try:
		driver.find_element(By.LINK_TEXT, 'More results').click()
	except:
		continue
title = driver.find_elements(By.TAG_NAME, 'h3')
for t in title: 
	if('-' not in t.text):
		continue
	reg = re.split(' - ',t.text,2)
	if(',' in reg[0]):
		name = reg[0].split(',',1)[0]
	else:
		name = reg[0]
	title = reg[1]
	if(email_format == 1):
		f_initial = name[0]
		last_name = name.split(" ")
		last_name = last_name[1]
		email_string = f_initial.lower() + last_name.lower() + "@" + email_domain.lower()
	elif(email_format == 2):
		first_name = name.split(" ")[0]
		last_name = name.split(" ")[1][0]
		last_name = last_name[0]
		email_string = first_name.lower() + last_name.lower() + "@" + email_domain.lower()
	elif(email_format == 3):
		first_name = name.split(" ")[0]
		last_name = name.split(" ")[1]
		email_string = first_name.lower() + last_name.lower() + "@" + email_domain.lower()
	elif(email_format == 4):
		f_initial = name[0]
		last_name = name.split(" ")
		last_name = last_name[1]
		email_string = f_initial.lower() + "." +last_name.lower() + "@" + email_domain.lower()
	elif(email_format == 5):
		first_name = name.split(" ")[0]
		last_name = name.split(" ")[1][0]
		last_name = last_name[0]
		email_string = first_name.lower() + "." + last_name.lower() + "@" + email_domain.lower()
	elif(email_format == 6):
		first_name = name.split(" ")[0]
		last_name = name.split(" ")[1]
		email_string = first_name.lower() + "." + last_name.lower() + "@" + email_domain.lower()
	if(txt):
		txt_file.write(name + "\t" + title + "\t" + email_string + "\n")
	if(csv):
		row = [name, title, email_string]
		csv_writer.writerow(row)
	else:
		print(name + "\t" + title + "\t" + email_string)
if(txt):
	txt_file.close()
if(csv):
	csv_file.close()
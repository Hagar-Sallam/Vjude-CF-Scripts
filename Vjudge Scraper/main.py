from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict
import time
import json
import csv
import os.path
from os import path

if not path.exists('data_collected.json'):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # Add your target
    driver.get("")

    # Login process
    link = driver.find_element(by=By.LINK_TEXT, value='Login')
    driver.implicitly_wait(20)
    link.click()

    username = driver.find_element(by=By.ID, value='login-username')
    password = driver.find_element(by=By.ID, value='login-password')


    username.send_keys(""); # Add your username here
    password.send_keys(""); # Add your password here

    link = driver.find_element(by=By.ID, value='btn-login')
    driver.implicitly_wait(20)
    link.click()

    # data retrieval
    elements = driver.find_elements(By.CLASS_NAME, 'accepted')
    mp = defaultdict(set)
    while len(elements)>0:
        driver.implicitly_wait(20)
        for row in elements:
            txt = row.text
            x = txt.split('\n')
            mp[x[0]].add(x[1])
        time.sleep(10)
        link = driver.find_element(by=By.LINK_TEXT, value='Next')
        driver.implicitly_wait(20)
        link.click()
        driver.implicitly_wait(20)
        elements = driver.find_elements(By.CLASS_NAME, 'accepted')

    print(mp)
    driver.quit()

    with open('data_collected.json', 'w') as collectedFile:
        for key, value in mp.items():
            mp[key] = list(value)
        json.dump(mp, collectedFile)
else:
    with open('data_collected.json', 'r') as collectedFile:
        mp = json.load(collectedFile)

with open('Groups.json', 'r') as inputFile:
    json_data = json.load(inputFile)

with open('Mandatory_State.csv', 'w') as outputFile:
    csv_writer = csv.writer(outputFile)

    csv_writer.writerow(["Handle", "Number","State", "Mandatory Solved", "Mandatory not Solved"])
    mandatory_groups = ["GroupX", "GroupY", "GroupZ","GroupA","GroupB"]
    for group in mandatory_groups:
        for vjude_handle in json_data[group]["handles"]:
            total_solved = []
            mandatory_not_solved = []
            header = [vjude_handle]
            if vjude_handle in mp:
                for mandatory_problem in json_data[group]["problems"]:
                    found = False
                    for solved_problem in mp[vjude_handle]:
                        if solved_problem == mandatory_problem:
                            total_solved.append(mandatory_problem)
                            found = True
                            break
                    if found == False:
                        mandatory_not_solved.append(mandatory_problem)
            else:
                csv_writer.writerow([vjude_handle,0, "No", "Zero or Incorrect Handle", "Zero or Incorrect Handle"])
                continue
            csv_writer.writerow([vjude_handle,len(mp[vjude_handle]), {True: "YES", False: "NO"}[len(mandatory_not_solved) == 0], total_solved,
                         mandatory_not_solved])

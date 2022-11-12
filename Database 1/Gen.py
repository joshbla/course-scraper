# Issues:
# https://student.apps.utah.edu/uofu/stu/ClassSchedules/main/1228/seating_availability.html?subject=HIST
# unicodeencodeerror

print("Enrollment Database")

import requests
from bs4 import BeautifulSoup
import pandas
import csv

df = pandas.read_csv('Database 1/Input.csv')

with open('Database 1/Output.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    header = [
        "Year", "Semester", "Class #", "Subject", "Catalog #", 
        "Section", "Title", "Enrollment Cap", "Wait List", 
        "Currently Enrolled", "Seats Available"
        ]
    writer.writerow(header)
    
    i = 0
    for link in df['Link']:
        
        page = requests.get(link)
        print(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        rowList = soup.find_all('tr')
        rowList.pop(0)
        
        for tr in rowList:
            outputRow = []
            outputRow.append(df['Year'][i]) # Year
            outputRow.append(df['Semester'][i]) # Semester
            
            outputRow.append((tr.select("td")[0]).get_text())
            
            for x in range(0, 2):
                outputRow.append((tr.select("td a")[x]).get_text())
            
            for x in range(3, 9):
                outputRow.append((tr.select("td")[x]).get_text())
            
            writer.writerow(outputRow)

        i += 1
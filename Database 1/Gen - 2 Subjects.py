import requests
from bs4 import BeautifulSoup
import pandas
import csv

df = pandas.read_csv('Database 1/Subject Links.csv')

with open('Database 1/Subjects.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    header = ["Subject"]
    writer.writerow(header)

    subjectSet = set()

    for link in df['Link']:
        
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        subjectList = soup.find_all(class_ = "btn btn-light btn-block")

        for subject in subjectList:
            subjectSet.add(subject.get_text().split(" - ", 1)[0])
    
    for subj in subjectSet:
        print(subj.replace(" ", "%20"))
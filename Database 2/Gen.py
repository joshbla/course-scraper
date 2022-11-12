# Issues:
# No catch for "online" verion (not canvas version)
# Skips empty pages. I need to check this works for pages of 1.
# https://student.apps.utah.edu/uofu/stu/ClassSchedules/main/1216/class_list.html?subject=ATFA
# https://student.apps.utah.edu/uofu/stu/ClassSchedules/main/1128/class_list.html?subject=BALLE list index out of range line 82
# https://student.apps.utah.edu/uofu/stu/ClassSchedules/main/1048/class_list.html?subject=LLREC list index out of range line 298
# https://student.apps.utah.edu/uofu/stu/ClassSchedules/main/1114/class_list.html?subject=ONCSC 20 Instructors

import requests
from bs4 import BeautifulSoup
import pandas
import csv
from datetime import datetime

df = pandas.read_csv('Database 2/Input.csv')

with open('Database 2/Output.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    header = [
        "Year", "Semester", "Subject", "Catalog #", 
        "Section", "Title", "Class #", 
        "Instructor 1", "Instructor 2", "Instructor 3", "Instructor 4", "Instructor 5", 
        "Instructor 6", "Instructor 7", "Instructor 8", "Instructor 9", "Instructor 10", 
        "Instructor 11", "Instructor 12", "Instructor 13", "Instructor 14", "Instructor 15", 
        "Instructor 16", "Instructor 17", "Instructor 18", "Instructor 19", "Instructor 20", 
        "Component", "Type", "Units", 
        "Requisites", "Wait List", "Fees", "Seats Available", 
        "Days 1", "Start 1", "End 1", "Building 1", "Room 1", "Meets Start 1", "Meets End 1", 
        "Days 2", "Start 2", "End 2", "Building 2", "Room 2", "Meets Start 2", "Meets End 2", 
        "Days 3", "Start 3", "End 3", "Building 3", "Room 3", "Meets Start 3", "Meets End 3", 
        "Days 4", "Start 4", "End 4", "Building 4", "Room 4", "Meets Start 4", "Meets End 4", 
        "Days 5", "Start 5", "End 5", "Building 5", "Room 5", "Meets Start 5", "Meets End 5", 
        "Days 6", "Start 6", "End 6", "Building 6", "Room 6", "Meets Start 6", "Meets End 6", 
        "Days 7", "Start 7", "End 7", "Building 7", "Room 7", "Meets Start 7", "Meets End 7", 
        "Days 8", "Start 8", "End 8", "Building 8", "Room 8", "Meets Start 8", "Meets End 8", 
        "Days 9", "Start 9", "End 9", "Building 9", "Room 9", "Meets Start 9", "Meets End 9", 
        "Days 10", "Start 10", "End 10", "Building 10", "Room 10", "Meets Start 10", "Meets End 10",
        "Session", 
        "Meets With 1", "Meets With 2", "Meets With 3", "Meets With 4", "Meets With 5", 
        "Meets With 6", "Meets With 7", "Meets With 8", "Meets With 9", "Meets With 10", 
        "Meets With 11", "Meets With 12", "Meets With 13", "Meets With 14", "Meets With 15", 
        ]
    writer.writerow(header)
    
    i = 0
    for link in df['Link']:
        
        page = requests.get(link)
        print(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        classCards = soup.find_all(class_ = "class-info card mt-3")
        
        for card in classCards:
            outputRow = []
            outputRow.append(df['Year'][i]) # Year
            outputRow.append(df['Semester'][i]) # Semester
            
            if len(card.contents) == 1:
                raise Exception
            
            if len(card.contents) > 1: # Skips empty pages. I need to check this works for pages of 1.
                body = card.find(class_ = "card-body row d-none d-md-block")
                body1 = body.find_all(class_= "col-12 p-0")[0]
                header = body1.find('h3')
                body2 = body.find_all(class_= "col-12 p-0")[1]
                body2 = (body2.find(class_ = "row breadcrumb-list list-unstyled")).select("li")
                footer = card.find(class_ = "card-footer mp-1")
                coordinates = footer.find(class_ = "row mb-2")
                session = footer.find(class_ = "row my-2")
                try:
                    meets = footer.find_all(class_ = "row")[1]
                except:
                    meets = False

                SC = ((header.find("a")).get_text()).split()
                outputRow.append(SC[0]) # Subject
                outputRow.append(SC[1]) # Catalog
                outputRow.append((header.find_all("span")[0]).get_text()) # Section
                try:
                    outputRow.append((header.find_all("span")[1]).get_text()) # Title may not be linked
                except:
                    outputRow.append((header.find_all("a")[0]).get_text()) # Title
                
                l = 0
                j = 0
                columnSlice = [
                    "Class Number", 
                    "Instructor", "Instructor", "Instructor", "Instructor", "Instructor",
                    "Instructor", "Instructor", "Instructor", "Instructor", "Instructor", 
                    "Instructor", "Instructor", "Instructor", "Instructor", "Instructor", 
                    "Instructor", "Instructor", "Instructor", "Instructor", "Instructor", 
                    "Component", "Type", "Units", "Requisites", "Wait List", "Fees", 
                    "Seats Available"
                    ]
                while j < len(body2):
                    section = ((body2[j]).get_text().split(":")[0]).lstrip()
                    
                    while section != columnSlice[l]:
                        outputRow.append("")  # Checks the order lines up with the header
                        l += 1
                    
                    if section == "Class Number":
                        data = ((body2[j]).find("span")) # Class
                        if data == None:
                            outputRow.append("")
                        else:
                            outputRow.append(data.get_text())
                    elif section == "Instructor":
                        data = ((body2[j]).select("span a")[0]) # Instructor
                        if data == None:
                            outputRow.append("")
                        else:
                            outputRow.append(data.get_text())
                    elif section == "Component":
                        data = ((body2[j]).find("span")) # Component
                        if data == None:
                            outputRow.append("")
                        else:
                            outputRow.append(data.get_text())
                    elif section == "Type":
                        data = ((body2[j]).find("span")) # Type
                        if data == None:
                            outputRow.append("")
                        else:
                            outputRow.append(data.get_text())
                    elif section == "Units":
                        data = ((body2[j]).find("span")) # Units
                        if data == None:
                            outputRow.append("")
                        else:
                            outputRow.append(data.get_text().strip())
                    elif section.split()[0] == "Requisites":
                        data = body2[j] # Requisites
                        if data == None:
                            outputRow.append("")
                        else:
                            outputRow.append(data.get_text().split()[1])
                    elif section == "Wait List":
                        data = (((body2[j]).find("span"))) # Wait List
                        if data == None:
                            outputRow.append("")
                        else:
                            outputRow.append(data.get_text())
                    elif section.split()[0] == "Fees":
                        data = body2[j] # Fees
                        if data == None:
                            outputRow.append("")
                        else:
                            outputRow.append((data.get_text()).split()[1])
                    elif section == "Seats Available":
                        data = ((body2[j]).find("span")) # Seats Available
                        if data == None:
                            outputRow.append("")
                        else:
                            outputRow.append(data.get_text())
                    else:
                        pass
                    j += 1
                    l += 1
                
                try:
                    tableEmpty = coordinates.find(class_ = "font-italic").get_text().strip()
                except:
                    tableEmpty = None
                tableEmptyTrue = "Days/times/locations to be arranged by instructor"
                tableRows = coordinates.find("tbody")
                if (tableEmpty == tableEmptyTrue) or (tableRows == None) or ((tableRows.get_text()).strip() == ""): # Checks if table is there or empty
                    for k in range(35):
                        outputRow.append("")
                else:
                    tr = tableRows.find_all("tr")
                    if len(tr) > 10:
                        raise Exception("Expected under 11")
                    for row in tr: # Checks for multiple items

                        dayTimeMeets = (row.find(class_ = "text-nowrap text-left p-0")).find_all("span")
                        if not dayTimeMeets: # Checks if dayTime cell is empty
                            outputRow.append("") # Days
                            outputRow.append("") # Start
                            outputRow.append("") # End
                            outputRow.append("") # Meets Start
                            outputRow.append("") # Meets End
                        else:
                            if len(dayTimeMeets) == 3:
                                times = (dayTimeMeets[1]).get_text()
                                start = times.split("-")[0]
                                end = times.split("-")[1]
                                start = (datetime.strptime(start, "%I:%M%p")).time().isoformat()
                                end = (datetime.strptime(end, "%I:%M%p")).time().isoformat()
                                meetsFrom = (((dayTimeMeets[2]).get_text()).split("Meets from ")[1]).split(" to ")
                                meetsStart = meetsFrom[0]
                                meetsEnd = meetsFrom[1]
                                
                                outputRow.append((dayTimeMeets[0]).get_text()) # Days
                                outputRow.append(start) # Start
                                outputRow.append(end) # End
                                outputRow.append(meetsStart) # Meets Start
                                outputRow.append(meetsEnd) # Meets End
                            elif len(dayTimeMeets) == 2:
                                firstTest = (dayTimeMeets[0]).get_text()
                                secondTest = (dayTimeMeets[1]).get_text()
                                
                                if len(firstTest) < 11:
                                    if len(secondTest) == 35: # Day and Meets
                                        outputRow.append(firstTest) # Days
                                        outputRow.append("") # Start
                                        outputRow.append("") # End
                                        meetsFrom = (((dayTimeMeets[1]).get_text()).split("Meets from ")[1]).split(" to ")
                                        meetsStart = meetsFrom[0]
                                        meetsEnd = meetsFrom[1]
                                        outputRow.append(meetsStart) # Meets Start
                                        outputRow.append(meetsEnd) # Meets End
                                    elif len(secondTest) == 15: # Day and Times
                                        outputRow.append(firstTest) # Days
                                        times = (dayTimeMeets[1]).get_text()
                                        start = times.split("-")[0]
                                        end = times.split("-")[1]
                                        start = (datetime.strptime(start, "%I:%M%p")).time().isoformat()
                                        end = (datetime.strptime(end, "%I:%M%p")).time().isoformat()
                                        outputRow.append(start) # Start
                                        outputRow.append(end) # End
                                        outputRow.append("") # Meets Start
                                        outputRow.append("") # Meets End
                                    else:
                                        raise Exception("The dayTimeMeets tests miscategorize")
                                elif len(firstTest) == 15:
                                    if len(secondTest) == 35: # Times and Meets
                                        outputRow.append("") # Days
                                        times = (dayTimeMeets[1]).get_text()
                                        start = times.split("-")[0]
                                        end = times.split("-")[1]
                                        start = (datetime.strptime(start, "%I:%M%p")).time().isoformat()
                                        end = (datetime.strptime(end, "%I:%M%p")).time().isoformat()
                                        outputRow.append(start) # Start
                                        outputRow.append(end) # End
                                        meetsFrom = (((dayTimeMeets[1]).get_text()).split("Meets from ")[1]).split(" to ")
                                        meetsStart = meetsFrom[0]
                                        meetsEnd = meetsFrom[1]
                                        outputRow.append(meetsStart) # Meets Start
                                        outputRow.append(meetsEnd) # Meets End
                                    else:
                                        raise Exception("The dayTimeMeets tests miscategorize")
                                else:
                                    raise Exception("The dayTimeMeets tests miscategorize")
                            elif len(dayTimeMeets) == 1:
                                allTest = (dayTimeMeets[0]).get_text()
                                if len(allTest) < 11:
                                    outputRow.append(allTest) # Days
                                    outputRow.append("") # Start
                                    outputRow.append("") # End
                                    outputRow.append("") # Meets Start
                                    outputRow.append("") # Meets End
                                elif len(allTest) == 15: #times only
                                    outputRow.append("") # Days
                                    start = allTest.split("-")[0]
                                    end = allTest.split("-")[1]
                                    start = (datetime.strptime(start, "%I:%M%p")).time().isoformat()
                                    end = (datetime.strptime(end, "%I:%M%p")).time().isoformat()
                                    outputRow.append(start) # Start
                                    outputRow.append(end) # End
                                    outputRow.append("") # Meets Start
                                    outputRow.append("") # Meets End
                                elif len(allTest) == 35:
                                    outputRow.append("") # Days
                                    outputRow.append("") # Start
                                    outputRow.append("") # End
                                    meetsFrom = ((allTest).split("Meets from ")[1]).split(" to ")
                                    outputRow.append(meetsFrom[0]) # Meets Start
                                    outputRow.append(meetsFrom[1]) # Meets End
                                else:
                                    raise Exception("The dayTimeMeets tests miscategorize")
                            else:
                                raise Exception("Expected 1, 2, or 3 spans")
                        
                        location = row.find(class_ = "text-nowrap text-right p-0")
                        if location.find("a") == None: # Checks if location is not linked
                            goo = location.find("span").get_text().split()
                            if len(goo) > 1:
                                outputRow.append(" ".join(goo[0:-1])) # Building
                                room = goo[-1]
                                if (room != "."):
                                    outputRow.append(goo[-1]) # Room
                                else:
                                    outputRow.append("") # Room
                            elif len(goo) == 1:
                                outputRow.append(goo[0]) # Building
                                outputRow.append("") # Room
                            else:
                                outputRow.append("") # Building
                                outputRow.append("") # Room
                        elif (location.find("a")).get_text() == "CANVAS .": # Checks if location is Canvas and linked
                            outputRow.append("Canvas") # Building
                            outputRow.append("") # Room
                        else: #Checks if location is linked
                            goo = location.find("a").get_text().split()
                            if len(goo) > 1:
                                outputRow.append(" ".join(goo[0:-1])) # Building
                                outputRow.append(goo[-1]) # Room
                            elif len(goo) == 1:
                                outputRow.append(goo[0]) # Building
                                outputRow.append("") # Room
                            else:
                                outputRow.append("") # Building
                                outputRow.append("") # Room
                    for emptyRow in range((10 - len(tr)) * 7):
                        outputRow.append("")
                
                if session == None: # Check for session field
                    outputRow.append("")
                else:
                    outputRow.append((session.select('div a')[0]).get_text().split(": ")[1])
                
                if meets: # Check for Meets-With field
                    ul = meets.find_all("li")
                    if len(ul) > 15:
                        raise Exception("Expected under 16")
                    for li in ul:
                        outputRow.append(li.get_text())
                    for emptyRow in range(15 - len(ul)):
                        outputRow.append("")
                else:
                    for k in range(15):
                        outputRow.append("")
                
                writer.writerow(outputRow)
        else:
                pass
            
        i += 1
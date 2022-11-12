import csv
import pandas

with open('Database 1/Input.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    header = ["Year", "Semester", "Link"]
    writer.writerow(header)

    url = ""
    url1 = "https://student.apps.utah.edu/uofu/stu/ClassSchedules/main/"
    url2 = ""
    url3 = "/seating_availability.html?subject="
    url4 = ""

    data = pandas.read_csv("Database 1/Subjects.csv")
    subjects = data['Subject'].tolist()
    subjects.sort()

    k = 0
    for s in subjects:
        url4 = subjects[k]

        i = 00
        while i < 23:
            
            j = 4
            while j < 9:
                outputRow = []
                outputRow.append(str(20) + str(i).rjust(2, '0'))
                if j == 4:
                    outputRow.append("Spring")
                elif j == 6:
                    outputRow.append("Summer")
                elif j == 8:
                    outputRow.append("Fall")
                
                url2 = "1" + str(i).rjust(2, '0') + str(j)
                url = url1 + url2 + url3 + url4
                outputRow.append(url)
                
                writer.writerow(outputRow)

                j += 2
            i += 1
        k += 1
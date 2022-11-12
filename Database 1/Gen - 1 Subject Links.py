import csv

with open('Database 1/Subject Links.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    header = ["Link"]
    writer.writerow(header)

    url1 = "https://student.apps.utah.edu/uofu/stu/ClassSchedules/main/"
    url3 = "/index.html"
    
    i = 00
    while i < 23:
        
        j = 4
        while j < 9:
            outputRow = []
            
            url2 = "1" + str(i).rjust(2, '0') + str(j)
            url = url1 + url2 + url3
            outputRow.append(url)
            
            writer.writerow(outputRow)

            j += 2
        i += 1
#Issues:
# None

# Pseudocode
# Take whole row
# Extract: Year, Semester, Meets-With-Catalog #, Meets-With-Section
# Search and Match/Find
# Append and delete the row as you find them
# If there is only one row in the output of searching through all meets-with columns:
#   append the row to the output dataframe.
# Else:
#   Take all rows. Compare Currently Enrolled. Modify the largest currently enrolled.
#   For Each:
#       Add to largest: Enrollment Cap, Wait List, Currently Enrolled, Seats Available
# Save Changes

import pandas as pd

fileName = 'Input.xlsx'
sheetName = "Database"
rowstomatch = 9

df = pd.read_excel(fileName, sheet_name = sheetName)
dfout = pd.DataFrame(columns = list(df))
while not df.empty:
    df.reset_index(drop = True, inplace = True)
    cr = df.iloc[0] #cr for current row
    df0 = df.iloc[[0]]
    #print(df0)
    df = df.iloc[1: , :] # Drop first row by selecting all rows from first row onwards
    #print(df)
    year = cr['Year']
    semester = cr['Semester']

    meetsCols = []
    for i in range(0, rowstomatch):
        meetsCols.append(cr[32 + i])

    #collects matching meets-with
    dfs = []
    dfs.append(df0)
    noMatches = False
    for i in meetsCols: # Extraction and search steps into one loop
        if not pd.isna(i): #If column is not empty
            x = i.split()
            course = x[1]
            section = (x[2]).lstrip("0")

            # Searches for match
            df1 = df[df['Year'] == year]
            df2 = df1[df1['Semester'] == semester]
            df3 = df2[df2['Catalog #'] == int(course)]
            df4 = df3[df3['Section'] == int(section)]
            dfs.append(df4)
            #print(df4)
            try:
                df = df[df['Identifier'] != (df4.iloc[0])['Identifier']] # Drops row from original df based upon a unique row identifier
                #print(df)
            except IndexError:
                noMatches = True
            except:
                raise Exception("Unexpected Error")
    
    if noMatches:
        dfout = pd.concat([dfout, df0], ignore_index = True)
    else:
        dfmatch = pd.concat(dfs, ignore_index = True)
        #print(dfmatch)
        dfmax = dfmatch[dfmatch['Currently Enrolled'] == dfmatch['Currently Enrolled'].max()]
        #print(dfmax)
        dfmatch = dfmatch[dfmatch['Identifier'] != (dfmax.iloc[0])['Identifier']] # Drops max row from dfmatch based upon a unique row identifier
        #print(dfmatch)
        for i in range(dfmatch.shape[0]):
            dfmax.iat[0, 8] += dfmatch.iat[i, 8]
            dfmax.iat[0, 9] += dfmatch.iat[i, 9]
            dfmax.iat[0, 10] += dfmatch.iat[i, 10]
            dfmax.iat[0, 11] += dfmatch.iat[i, 11]
        #print(dfmax)
        dfout = pd.concat([dfout, dfmax], ignore_index = True)
    
    print(dfout)

dfout.to_excel("Output.xlsx", sheet_name = 'Database Condensed', index = False)
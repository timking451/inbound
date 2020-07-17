#Inbound scanning for hardware store.

# Import dependencies
import time
import csv
import collections as col
import pandas as pd



# The mcr.txt path on Rover will be:
# C:\Users\Paladin User\Google Drive\King Ace Hardware\Inbound Scanning

# Create and format the dataframe
mcrdf = pd.read_csv("mcr.txt")
mcrdf['OrderQty'] = mcrdf['OrderQty'].astype(int)
mcrdf = mcrdf.astype(str)
mcrdf['Count'] = ""
mcrdf['OK'] = ""
mcrdf = mcrdf.sort_values(by=['Deliverable Unit'], ascending=False)
# Create other dataframes for later reporting
dfshorts = pd.DataFrame(columns=mcrdf.columns)
dfovers = pd.DataFrame(columns=mcrdf.columns)

# Create empty list for UPC scans
scanned_items = []

#mcrdf.head()

#Basic interface decision tree.
#Most common loop is scanning items.
#Also accepts inputs for report generation, etc.
while True:
    print('Please scan an item. Enter "help" for more options.')
    scanned = input()
    scanned = scanned.lstrip('0')
    if scanned == 'help':
        print('''\tEnter 'short' to generate a shortage report.
        Enter 'over' to generate an overage report.
        Enter 'exit' to exit this awesome program.''')
        continue
    if scanned == 'over':
        overage_report()
        continue
    if scanned == 'short':
        shortage_report()
        continue
    if scanned == 'exit':
        break
    else:
        try:
            scanned_items.append(scanned)
            a = mcrdf[mcrdf['UPC'] == scanned]
            print(a)
            print(f"Item count: {scanned_items.count(scanned)}")
        except ValueError:
            print("That item is not expected.")
            overs.append(scanned)

# c is a Counter object, counting occurences of each UPC in scanned_items
# it is a dictionary with the UPC as the key and the count as the value
c = col.Counter(scanned_items)
# MAP the c values onto the Count column
mcrdf['Count'] = mcrdf['UPC'].map(c)
# Reset everything to strings to help with later equivalency tests
mcrdf = mcrdf.astype(str)

#mcrdf.head()

# This is how you iterate over a dataframe.
# Don't forget to use the .index on your dataframe when initializing
# the for loop.
for ind in mcrdf.index:
    if mcrdf['OrderQty'][ind] > mcrdf['Count'][ind]:
        mcrdf['OK'][ind] = "SHORT"
    elif mcrdf['OrderQty'][ind] < mcrdf['Count'][ind]:
        mcrdf['OK'][ind] = "OVER"
    else:
        mcrdf['OK'][ind] = "OK" 

#mcrdf.head()

#Export one big excel file

mcrdf.to_excel('report.xlsx')

time.sleep(3)
"""
for row in mcrdf.index:
    if mcrdf['Count'][row] < mcrdf['OrderQty'][row]:
        r = pd.DataFrame(data=row)
        dfshorts.append(row)
"""

# Import dependencies
import time
import csv
import collections as col
import pandas as pd
import re
import shelve
import pprint

def save_scans(data):
    shelfFile = shelve.open('scanned_items')
    shelfFile['scanned_items'] = data
    shelfFile.close()

def load_scans():
    shelfFile = shelve.open('scanned_items')
    return shelfFile['scanned_items']

# Create and format the dataframe
df = pd.read_csv("MasterCrossReference.txt")
df['OrderQty'] = df['OrderQty'].astype(int)
df = df.astype(str)
df['Count'] = ""
df['OK'] = "---"
df = df.sort_values(by=['Deliverable Unit'], ascending=False)

# Create empty list for UPC scans
scanned_items = []

#Basic interface decision tree.
#Most common loop is scanning items.
#Also accepts inputs for report generation, etc.
while True:
    print('Please scan an item. Enter "help" to for more options.')
    scanned = input()
    scanned = scanned.lstrip('0')
    if scanned == 'exit':
        break
    elif scanned == 'save':
        save_scans(scanned_items)
    elif scanned == 'load':
        scanned_items = load_scans()
    elif scanned == 'help':
        print("'save': Save the current state of the scanned items list")
        print("'load': Load the previously saved scanned items list")
        print("'exit': Terminte the program and generate the tote report")
    else:
        try:
            scanned_items.append(scanned)
            #df['Count'][df['UPC'] == scanned] = scanned_items.count(scanned)
            # c is a Counter object, counting occurences of each UPC in scanned_items
            # it is a dictionary with the UPC as the key and the count as the value
            c = col.Counter(scanned_items)
            # MAP the c values onto the Count column
            df['Count'] = df['UPC'].map(c)
            # Reset everything to strings to help with later equivalency tests
            df = df.astype(str)
            a = df.loc[df.index[df['UPC'] == scanned]].transpose()
            pprint.pprint(a)
            #print(f"Item count: {scanned_items.count(scanned)}")
        except ValueError:
            print("That item is not expected.")
            overs.append(scanned)

# This is how you iterate over a dataframe.
# Don't forget to use the .index on your dataframe when initializing
# the for loop.
for ind in df.index:
    if df['OrderQty'][ind] > df['Count'][ind]:
        df['OK'][ind] = "SHORT"
    elif df['OrderQty'][ind] < df['Count'][ind]:
        df['OK'][ind] = "OVER"
    else:
        df['OK'][ind] = "OK"

#Export one big excel file with filters and formatting
df = df.drop(df[df['OK'] == 'OK'].index)
df['UPC'] = ''
df.sort_values(by=['OK'])
tote = re.compile(r'^T')
df = df[df['Deliverable Unit'].str.match(tote) == True]
df.to_excel('report.xlsx')

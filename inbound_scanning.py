# Import dependencies
from inbound_module import *
import time, csv, pprint
import collections as col
import pandas as pd
#from playsound import playsound

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
    print('Please scan an item. Enter "help" for more options.')
    scanned = input()
    scanned = scanned.lstrip('0')
    if scanned == 'exit':
        break
    elif scanned == 'load':
        scanned_items = load_scans()
    elif scanned == 'totes':
        tote_report(df)
    elif scanned == 'optis':
        opti_report(df)
    elif scanned == 'help':
        print("'load': Load the previously saved scanned items list")
        print("'totes': Generate the totes report")
        print("'optis': Generate the optis report")
        print("'exit': Exit the program")
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
            save_scans(scanned_items)
            print('\a')
        except ValueError:
            print("That item is not expected.")

# This is how you iterate over a dataframe.
# Don't forget to use the .index on your dataframe when initializing
# the for loop.


#Export one big excel file with filters and formatting



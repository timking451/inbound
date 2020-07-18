#Inbound scanning for hardware store.

# Import dependencies
import time
import csv
import collections as col
import pandas as pd
from inbound_module import *

# The mcr.txt path on Rover will be:
# C:\Users\Paladin User\Google Drive\King Ace Hardware\Inbound Scanning

formatting()

# Create empty list for UPC scans
scanned_items = []

#Basic interface decision tree.
#Most common loop is scanning items.
#Also accepts inputs for report generation, etc.
while True:
    print('Please scan an item. Enter "help" for more options.')
    scanned = input()
    scanned = scanned.lstrip('0')
    if scanned == 'help':
        print("There will be a help menu as soon as this program is complicated")
        print("enough to warrant one.")
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

get_counts()

report_filler()

#Export one big excel file
mcrdf.to_excel('report.xlsx')

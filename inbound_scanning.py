# Import dependencies
from inbound_module import *
import time, csv, pprint
import collections as col
import pandas as pd

# from playsound import playsound

# Create and format the dataframe
df = pd.read_csv("MasterCrossReference.txt")
df["OrderQty"] = df["OrderQty"].astype(int)
df = df.astype(str)
df["Count"] = ""
df["OK"] = "---"
df = df.sort_values(by=["Deliverable Unit"], ascending=False)

# Create empty list for UPC scans
scanned_items = []

# Basic interface decision tree.
# Most common loop is scanning items.
# Also accepts inputs for report generation, etc.
while True:
    print('Please scan an item. Enter "help" for more options.')
    scanned = input()
    scanned = scanned.lstrip("0")
    if scanned == "exit":
        break
    elif scanned == "load":
        scanned_items = load_scans()
    elif scanned == "totes":
        tote_report(df)
    elif scanned == "optis":
        opti_report(df)
    elif scanned == "help":
        print("'load':   Load the previously saved scanned items list")
        print("'totes':  Generate the totes report")
        print("'optis':  Generate the optis report")
        print("'check':  Check on the status of an item without recording the scan")
        print("'undo':   Remove the most recently scanned item")
        print("'exit':   Exit the program")
    elif scanned == "check":
        print("Please scan the item you wish to check")
        check = input()
        check = check.lstrip("0")
        print("*************************************")
        print("Here's what I know about that item:")
        print_count(check, scanned_items, df)
        print("*************************************")
    elif scanned == "undo":
        scanned_items.pop()
        print("Item removed")    
    else:
        try:
            scanned_items.append(scanned)
            print_count(scanned, scanned_items, df)
            save_scans(scanned_items)
            print("\a")
        except ValueError:
            print("That item is not expected.")

# This is how you iterate over a dataframe.
# Don't forget to use the .index on your dataframe when initializing
# the for loop.


# Export one big excel file with filters and formatting

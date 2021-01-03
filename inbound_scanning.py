# Import dependencies
import time
import csv
import collections as col
import pandas as pd
import re
import shelve
import pprint
import os
#from playsound import playsound

os.system("rclone copy dropbox:inbound ~/dropbox")

# Create and format the dataframe
df = pd.read_csv("~/dropbox/MasterCrossReference.txt")
df['OrderQty'] = df['OrderQty'].astype(int)
df = df.astype(str)
df['Count'] = ""
df['OK'] = "---"
df = df.sort_values(by=['Deliverable Unit'], ascending=False)

os.system("^C") # Is this really necessary?

scanned_items = [] # Create empty list for UPC scans

def main():
    #Basic interface decision tree.
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
    #    elif scanned == "check":
    #        print("Please scan the item you wish to check")
    #        check = input()
    #        check = check.lstrip("0")
    #        c = col.Counter(scanned_items)
    #        # MAP the c values onto the Count column
    #        df['Count'] = df['UPC'].map(c)
    #        print("*************************************")
    #        print("Here's what I know about that item:")
    #        a = df.loc[df.index[df['UPC'] == check]].transpose()
    #        pprint.pprint(a)
    #        print("*************************************")
        elif scanned == "undo":
            scanned_items.pop()
            print("Item removed")    
        elif scanned == 'help':
            print("'load': Load the previously saved scanned items list")
            print("'totes': Generate the totes report")
            print("'optis': Generate the optis report")
    #        print("'check': Check the status of an item")
            print("'undo': Remove the most recently scanned item")
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
                if len(scanned_items)%5 == 0:
                    save_scans(scanned_items)
                #playsound('beep.wav')
            except ValueError:
                print("That item is not expected.")

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

def save_scans(data):
    shelfFile = shelve.open('scanned_items')
    shelfFile['scanned_items'] = data
    shelfFile.close()

def load_scans():
    shelfFile = shelve.open('scanned_items')
    return shelfFile['scanned_items']

def tote_report(df):
    df_tote = df
    for ind in df_tote.index:
        if df_tote['OrderQty'][ind] > df_tote['Count'][ind]:
            df_tote['OK'][ind] = "SHORT"
        elif df_tote['OrderQty'][ind] < df_tote['Count'][ind]:
            df_tote['OK'][ind] = "OVER"
        else:
            df_tote['OK'][ind] = "OK"

    df_tote = df_tote.drop(df_tote[df_tote['OK'] == 'OK'].index)
    df_tote['UPC'] = ''
    df_tote.sort_values(by=['OK'])
    tote = re.compile(r'^T')
    df_tote = df_tote[df_tote['Deliverable Unit'].str.match(tote) == True]
    df_tote.to_excel('~/dropbox/tote_report.xlsx') 
    os.system("rclone copy ~/dropbox dropbox:inbound")

def opti_report(df):
    df_opti = df
    for ind in df_opti.index:
        if df_opti['OrderQty'][ind] > df_opti['Count'][ind]:
            df_opti['OK'][ind] = "SHORT"
        elif df_opti['OrderQty'][ind] < df_opti['Count'][ind]:
            df_opti['OK'][ind] = "OVER"
        else:
            df_opti['OK'][ind] = "OK"

    df_opti = df_opti.drop(df_opti[df_opti['OK'] == 'OK'].index)
    df_opti['UPC'] = ''
    df_opti.sort_values(by=['OK'])
    opti = re.compile(r'^\d')
    df_opti = df_opti[df_opti['Deliverable Unit'].str.match(opti) == True]
    df_opti.to_excel('~/dropbox/opti_report.xlsx') 
    os.system("rclone copy ~/dropbox dropbox:inbound")

if __name__ == "__main__":
    main()



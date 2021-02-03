import PySimpleGUI as sg 
import time
import csv
import collections as col
import pandas as pd
import re
import shelve
import pprint
import os
import sys
#from playsound import playsound

os.system("rclone copy dropbox:inbound ~/dropbox")

# Create and format the dataframe
df = pd.read_csv("~/dropbox/MasterCrossReference.txt")
df['OrderQty'] = df['OrderQty'].astype(int)
df = df.astype(str)
df['Count'] = ""
df['OK'] = "---"
df = df.sort_values(by=['Deliverable Unit'], ascending=False)

#os.system("^C") # Is this really necessary?

scanned_items = [] # Create empty list for UPC scans


def click_ok(df, scanned):
    scanned = scanned.astype(str).lstrip('0)')
    scanned_items.append(scanned)
    # c is a Counter object, counting occurences of each UPC in scanned_items
    # it is a dictionary with the UPC as the key and the count as the value
    c = col.Counter(scanned_items)
    # MAP the c values onto the Count column
    df['Count'] = df['UPC'].map(c)
    # Reset everything to strings to help with later equivalency tests
    #df = df.astype(str)
    a = df.loc[df.index[df['UPC'] == scanned]].transpose()
    pprint.pprint(a)
    if len(scanned_items)%5 == 0:
        save_scans(scanned_items)
    #playsound('beep.wav')
    window['-OUT-'].Update('')
    window['-OUT-'].print(a)

def click_check():
    window['-OUT-'].Update('')
    window['-OUT-'].print('you clicked check.')

def save_scans(data):
    shelfFile = shelve.open('scanned_items')
    shelfFile['scanned_items'] = data
    shelfFile.close()

def load_scans():
    shelfFile = shelve.open('scanned_items')
    return shelfFile['scanned_items']

def check(df, scanned_items):
    df_check = df.copy(deep=True)
    print("Please scan the item you wish to check")
    check = input()
    check = check.lstrip("0")
    c = col.Counter(scanned_items)
    # MAP the c values onto the Count column
    df_check['Count'] = df_check['UPC'].map(c)
    print("*************************************")
    print("Here's what I know about that item:")
    a = df_check.loc[df_check.index[df_check['UPC'] == check]].transpose()
    pprint.pprint(a)
    print("*************************************")


layout = [[sg.Text('Please scan an item')], 
          [sg.Input(do_not_clear=False, key='-IN-')],       
          [sg.Multiline('', size=(45, 7), key='-OUT-', auto_refresh=True)], 
          [sg.Ok(), sg.Button('Check'),      
          sg.Button('Remove'), sg.Button('Tote Report'),
          sg.Button('Opti Report')]]

layout_check = [[sg.Text('Here\'s what I know about that                     item:')],
                [sg.Multiline('Boop', size=(45,5))],
                [sg.Ok()]]

window = sg.Window('Inbound Scanning', layout)

while True:
    event, values = window.read()
    if event == 'Check':
        click_check()
    elif event == 'Ok':
        click_ok(df, values['-IN-'])
    if event == 'Remove':
        break
window.close()


"""
def click_ok():
    window['-OUT-'].Update('')
    window['-OUT-'].print('you clicked ok!')

def click_check():
    window['-OUT-'].Update('')
    window['-OUT-'].print('you clicked check.')

layout = [[sg.Text('Please scan an item')], 
          [sg.Input(do_not_clear=False)],       
          [sg.Multiline('', size=(45, 7), key='-OUT-', auto_refresh=True)], 
          [sg.Ok(), sg.Button('Check'),      
          sg.Button('Remove'), sg.Button('Tote Report'),
          sg.Button('Opti Report')]]

layout_check = [[sg.Text('Here\'s what I know about that                     item:')],
                [sg.Multiline('Boop', size=(45,5))],
                [sg.Ok()]]

window = sg.Window('Inbound Scanning', layout)

while True:
    event, values = window.read()
    if event == 'Check':
        click_check()
    elif event == 'Ok':
        click_ok()
    elif event == 'Remove':
        break
window.close()

sg.Popup(event, values[0])
"""
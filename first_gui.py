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

os.system("rclone copy dropbox:inbound ~/dropbox")

# Create and format the dataframe
df = pd.read_csv("~/dropbox/MasterCrossReference.txt")
df['OrderQty'] = df['OrderQty'].astype(int)
df = df.astype(str)
df['Count'] = ""
df['OK'] = "---"
df = df.sort_values(by=['Deliverable Unit'], ascending=False)

scanned_items = [] # Create empty list for UPC scans

def click_ok(df, scanned):
    scanned = scanned.lstrip('0)')
    scanned_items.append(scanned)
    # c is a Counter object, counting occurences of each UPC in scanned_items
    # it is a dictionary with the UPC as the key and the count as the value
    c = col.Counter(scanned_items)
    # MAP the c values onto the Count column
    df['Count'] = df['UPC'].map(c)
    a = df.loc[df.index[df['UPC'] == scanned]].transpose()
    #if len(scanned_items)%5 == 0:
     #   save_scans(scanned_items)
    window['-OUT-'].Update(a)

def save_scans(data):
    shelfFile = shelve.open('scanned_items')
    shelfFile['scanned_items'] = data
    shelfFile.close()

def load_scans():
    shelfFile = shelve.open('scanned_items')
    return shelfFile['scanned_items']

def check(df):
    layout = [[sg.Text('Scan the item you wish to check')],
            [sg.Input(do_not_clear=False, key='-IN-')],
            [sg.Multiline("\n\n\nPlease scan the item you wish to check", size=(50, 9), font='Arial 15', key='-OUT-', auto_refresh=True)], 
            [sg.Ok(), sg.Button('Exit')]]
    
    window = sg.Window('CHECK', layout, modal=True)

    while True:
        event, values = window.read()

        if event == 'Ok':
            df_check = df.copy(deep=True)
            values['-IN-'] = values['-IN-'].lstrip('0)')
            c = col.Counter(scanned_items)
            df_check['Count'] = df_check['UPC'].map(c)
            a = df_check.loc[df_check.index[df_check['UPC'] == values['-IN-']]].transpose()
            window['-OUT-'].Update(a)
            
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
    window.close()


def tote_report(df):
    window['-OUT-'].Update('\n\n\nGenerating Tote Report.\nPlease wait...', justification='center')
    df_tote = df.copy(deep=True)
    for ind in df_tote.index:
        if int(df_tote['OrderQty'][ind]) > int(df_tote['Count'][ind]):
            df_tote.loc[ind, 'OK'] = 'SHORT'
        elif int(df_tote['OrderQty'][ind]) < int(df_tote['Count'][ind]):
            df_tote.loc[ind, 'OK'] = "OVER"
        else:
            df_tote.loc[ind, 'OK'] = "OK"

    df_tote = df_tote.drop(df_tote[df_tote['OK'] == 'OK'].index)
    df_tote['UPC'] = ''
    df_tote.sort_values(by=['OK'])
    tote = re.compile(r'^T')
    df_tote = df_tote[df_tote['Deliverable Unit'].str.match(tote) == True]
    df_tote.to_excel('~/dropbox/tote_report.xlsx') 
    os.system("rclone copy ~/dropbox dropbox:inbound")
    window['-OUT-'].Update('\n\n\nTote Report is ready.\n You may continue scanning.', justification='center')

def opti_report(df):
    window['-OUT-'].Update('\n\n\nGenerating Opti Report.\nPlease wait...', justification='center')
    df_opti = df.copy(deep=True)
    for ind in df_opti.index:
        if int(df_opti['OrderQty'][ind]) > int(df_opti['Count'][ind]):
            df_opti.loc[ind, 'OK'] = 'SHORT'
        elif int(df_opti['OrderQty'][ind]) < int(df_opti['Count'][ind]):
            df_opti.loc[ind, 'OK'] = "OVER"
        else:
            df_opti.loc[ind, 'OK'] = "OK"

    df_opti = df_opti.drop(df_opti[df_opti['OK'] == 'OK'].index)
    df_opti['UPC'] = ''
    df_opti.sort_values(by=['OK'])
    opti = re.compile(r'^\d')
    df_opti = df_opti[df_opti['Deliverable Unit'].str.match(opti) == True]
    df_opti.to_excel('~/dropbox/opti_report.xlsx') 
    os.system("rclone copy ~/dropbox dropbox:inbound")
    window['-OUT-'].Update('\n\n\nOpti Report is ready.\nYou may continue scanning.', justification='center')

#col = [sg.Multiline('', size=(30, 60), font='Arial 8', key='-LOG-', auto_refresh=False)]

layout = [[sg.Text('Please scan an item')], #sg.Column(col)],
          [sg.Input(do_not_clear=False, key='-IN-')], #sg.Multiline('', size=(30, 60), font='Arial 8', key='-LOG-', auto_refresh=False)],      
          [sg.Multiline('', size=(45, 9), font='Arial 30', key='-OUT-', auto_refresh=True)], 
          [sg.Ok(), sg.Button('Check'),      
          sg.Button('Remove'), sg.Button('Tote Report'),
          sg.Button('Opti Report')]]

window = sg.Window('Inbound Scanning', layout)

while True:
    event, values = window.read()
    if event == 'Check':
        check(df)
    elif event == 'Ok':
        click_ok(df, values['-IN-'])
    elif event == 'Remove':
        scanned_items.pop()
        window['-OUT-'].Update('Item Removed')
    elif event == 'Tote Report':
        tote_report(df)
    elif event == 'Opti Report':
        opti_report(df)
    elif event == sg.WIN_CLOSED:
        break
window.close()


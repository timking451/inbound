import shelve, re
import collections as cl
import pandas as pd

def short_over(df):
    for ind in df.index:
        if df['Count'][ind] == '':
            df['Count'][ind] = '0'
    df['OrderQty'] = df['OrderQty'].astype(int)
    df['Count'] = df['Count'].astype(int)
    df.loc[df.OrderQty > df.Count, df.OK] = 'SHORT'
"""
    for ind in df.index:
        if df['OrderQty'][ind] > df['Count'][ind]:
            df.loc['OK'][ind] = "SHORT"
        elif df['OrderQty'][ind] < df['Count'][ind]:
            df['OK'][ind] = "OVER"
        else:
            df['OK'][ind] = "OK"
"""            
    return df
            
def save_scans(data):
    shelfFile = shelve.open('scanned_items')
    shelfFile['scanned_items'] = data
    shelfFile.close()

def load_scans():
    shelfFile = shelve.open('scanned_items')
    return shelfFile['scanned_items']

def tote_report(df):
    short_over(df)
    df = df.drop(df[df['OK'] == 'OK'].index)
    df['UPC'] = ''
    df.sort_values(by=['OK'])
    tote = re.compile(r'^T')
    df = df[df['Deliverable Unit'].str.match(tote) == True]
    df.to_excel('tote_report.xlsx') 

def opti_report(df):
    df = short_over(df)
    df = df.drop(df[df['OK'] == 'OK'].index)
    df['UPC'] = ''
    df.sort_values(by=['OK'])
    opti = re.compile(r'^\d')
    df = df[df['Deliverable Unit'].str.match(opti) == True]
    df.to_excel('opti_report.xlsx') 

def print_count(scanned, scanned_items, df):
    # df['Count'][df['UPC'] == scanned] = scanned_items.count(scanned)
    # c is a Counter object, counting occurences of each UPC in scanned_items
    # it is a dictionary with the UPC as the key and the count as the value
    c = cl.Counter(scanned_items)
    # MAP the c values onto the Count column
    df["Count"] = df["UPC"].map(c)
    # Reset everything to strings to help with later equivalency tests
    df = df.astype(str)
    a = df.loc[df.index[df["UPC"] == scanned]].transpose()
    print(a)
    # print(f"Item count: {scanned_items.count(scanned)}")


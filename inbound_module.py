import shelve, re

def short_over(df):
    for ind in df.index:
        if df['OrderQty'][ind] > df['Count'][ind]:
            df['OK'][ind] = "SHORT"
        elif df['OrderQty'][ind] < df['Count'][ind]:
            df['OK'][ind] = "OVER"
        else:
            df['OK'][ind] = "OK"
            
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
    short_over(df)
    df = df.drop(df[df['OK'] == 'OK'].index)
    df['UPC'] = ''
    df.sort_values(by=['OK'])
    opti = re.compile(r'^\d')
    df = df[df['Deliverable Unit'].str.match(opti) == True]
    df.to_excel('opti_report.xlsx') 


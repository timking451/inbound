def formatting():
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

def get_counts():
    # c is a Counter object, counting occurences of each UPC in scanned_items
    # it is a dictionary with the UPC as the key and the count as the value
    c = col.Counter(scanned_items)
    # MAP the c values onto the Count column
    mcrdf['Count'] = mcrdf['UPC'].map(c)
    # Reset everything to strings to help with later equivalency tests
    mcrdf = mcrdf.astype(str)

def report_filler():
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

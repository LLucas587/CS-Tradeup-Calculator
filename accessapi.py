import requests
import pandas as pd
pd.options.display.max_columns = 999
pd.options.display.max_rows = None

import scrape
import re

def api():
    response = requests.get('http://csgobackpack.net/api/GetItemsList/v2/')
    return (response.json())

def modifyData():
    """
    Converts api call to pandas dataframe and removes information we do not need 
    """
    response = requests.get('http://csgobackpack.net/api/GetItemsList/v2/')
    df=pd.DataFrame(response.json()['items_list'])
    df=df.T
    df=df[df['type']=='Weapon'] # Removing Non Weapons
    df=df[df['weapon_type']!='Knife']
    df=df[df['marketable']==1]
    df.drop('sticker', axis=1, inplace=True)
    df.drop('tournament', axis=1, inplace=True)
    df.drop('souvenir', axis=1, inplace=True)
    df.drop('knife_type', axis=1, inplace=True)
    df.drop('stock', axis=1, inplace=True)
    return df
    
def addCollection(df):
    """
    Adds Collection Column to pandas dataframe
    """
    skincollect=scrape.createCollectDict()
    collectioninfo=[]
    for ind in df.index:
        name = df['name'][ind]
        name = re.sub("[\(\[].*?[\)\]]", "", name)[:-1]
        if name in skincollect.keys():
            # df['collection'][ind] = skincollect[name]
            collectioninfo += [skincollect[name]]
        else:
            # df['collection'][ind] = None
            collectioninfo += [None]
    df['collection'] = collectioninfo


def createCollection()->pd.DataFrame:
    """
    Creates pandas dataframe of skins with a collection column
    """
    df=modifyData()
    addCollection(df)
    return df

    
if __name__ == '__main__':
    print(createCollection())
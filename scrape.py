import requests
from bs4 import BeautifulSoup

def getCollections()->[]:
    URL = "https://csgostash.com/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    dropdowns =  soup.find_all("li", {"class": "dropdown"}) 
    collections = dropdowns[5]
    collectionLinks =[]
    for collection in collections:
        collectionLinks += [collection]
    collectionLinks = str(collectionLinks[3]).splitlines()
    collectionLinks.pop(0)
    collectionLinks.pop()
    collectionLinks2=[]
    for link in collectionLinks:
        link = link[13:]
        end = link.index('>')
        link = link[:end-1]
        collectionLinks2 += [link]
    return collectionLinks2

def getSkins(url:str)->[str]:
    """
    url - From getCollections
    """
    URL = url
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    skinbox =  soup.find_all("div", {"class": "well result-box nomargin"})
    skinlist = []
    for skins in skinbox:
        skin_name = skins.find("h3")
        if skin_name != None:
            skinlist+=[skin_name.text]
    return (skinlist)

def createCollectDict()->dict[str, str]:
    """
    Interacts with getCollections and getSkins to create dictionary storing skins and respective collections
    """
    collections=getCollections()
    collectdict={}
    for url in collections:
        collectdict[url]=getSkins(url)
    skindict={}
    for url in collections:
        for skin in collectdict[url]:
            skindict[skin]=url
    return skindict







if __name__ == '__main__':
    print(createCollectDict())
    
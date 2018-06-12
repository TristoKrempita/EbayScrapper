import requests
from bs4 import BeautifulSoup
pageNumber = 1
url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=arduino&_sacat=0"#+str(pageNumber)
r_html = requests.get(url).text
soup = BeautifulSoup(r_html,"html.parser")
chr = soup.find_all('h3',class_="s-item__title")
cijene = soup.find_all('span',class_="s-item__price")
links = soup.find_all('a',class_="s-item__link")
#for c in cijene:
#    print(str(c.string)[1:])

filterCijena = float(input("Upper limit filter price: "))

class grafa:
    ime = None
    cijena = None
    link = None

grafe = []
grafeFinal=[]
for graf in range(len(cijene)):
    grafe.append(grafa())
for i in range(0,len(cijene)):
    #assigns title text to the ime variable of object
    grafe[i].ime = chr[i].text
    #turning the string we got from the price in the $3.45 format into a 3.45 float
    if(any(char.isdigit() for char in str(cijene[i].string))):
        grafe[i].cijena = float(str(cijene[i].string)[1:])
    #if the price isn't a price at all we set the value to -0.5 and filter it later
    else:
        grafe[i].cijena = -0.5
    #we assign the href memeber of the tag to the link variable of object
    grafe[i].link = links[i]['href']

#sorting the array of objects by attribute cijena
grafe.sort(key=lambda x: x.cijena, reverse=False)
#prints list of items until upper limit
for x in grafe:
    if(x.cijena != None and x.cijena<filterCijena and x.cijena != -0.5):
        print(x.ime," | ",x.cijena," | ",x.link,"\n")

with open('graficke','w',encoding='utf-8') as file:
    for x in grafe:
        if(x.cijena != None and x.cijena<filterCijena and x.cijena != -0.5):
            file.write(str(x.ime)+" | "+str(x.cijena)+" | "+str(x.link)+"\n")
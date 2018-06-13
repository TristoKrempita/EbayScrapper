import requests
from bs4 import BeautifulSoup

userSearch = input("What do you want to search for?\n>")
url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw="
userSearch = userSearch.split(' ')
for search in userSearch:
    url += search+"+"
#removing the excess '+'
url = url[:-1]
print(url)
r_html = requests.get(url).text
soup = BeautifulSoup(r_html,"html.parser")
chr = soup.find_all('h3',class_="s-item__title")
cijene = soup.find_all('span',class_="s-item__price")
links = soup.find_all('a',class_="s-item__link")
cijeneFinal = []
for i in range(0,len(cijene)):
    #if the parent is the same it means there are 2 or more prices in the same item category and we don't want them to clog up the cijene[] and cause
    #some items to have wrong prices attached to them so we check for that and remove any prices but the base one
    if((cijene[i].parent.parent.parent.parent.parent == cijene[i-1].parent.parent.parent.parent.parent)):
        continue
    else:
        cijeneFinal.append(cijene[i])
values = [len(chr),len(cijeneFinal),len(links)]
#print(values)
filterCijena = float(input("Upper limit filter price: "))
#print(">"+str(filterCijena))
class item:
    ime = None
    cijena = None
    cijenaString = None
    link = None
    parentTag = None

replaced = ""
items = []
itemsFinal=[]
#return this after you fix the bid 2 prices on 1 item being treated as 2 prices on 2 items
for graf in range(min(values)):
    items.append(item())
for i in range(0,min(values)):
    #assigns title text to the ime variable of object
    if(chr[i].text[0:11].lower() == "new listing"):
        items[i].ime=chr[i].text[11:]
    else:
        items[i].ime = chr[i].text
    items[i].cijenaString = cijeneFinal[i].text
    #turning the string we got from the price in the $3.45 format into a 3.45 float
    if(any(char.isdigit() for char in str(cijeneFinal[i].string))):
        #if the price has a ',' replace all '.' with '' and all ',' with '.' and remove last 2 digits (the decimal remainder)
        if(',' in str(cijeneFinal[i].string)[1:]):
            replaced = str(cijeneFinal[i].string)[1:].replace(".","")
            replaced = replaced[:-2]
            replaced = replaced.replace(",",".")
            items[i].cijena = float(replaced)
        #if the price doesn't have a ',' juts remove the '$' sign and store it as a float inside the item class
        else:
            items[i].cijena = float(str(cijeneFinal[i].string)[1:])
    #if the price isn't a price at all we set the value to the first decimal of the first number ($0.13 to $13.5) => 0.1
    else:
        items[i].cijena = float(str(cijeneFinal[i].text)[1:4])
        #print("|||"+str(float(str(cijeneFinal[i].text)[1:4])))
    #we assign the href memeber of the tag to the link variable of object
    items[i].link = links[i]['href']
    items[i].parentTag = chr[i].parent.parent.parent

#sorting the array of objects by attribute cijena
items.sort(key=lambda x: x.cijena, reverse=False)

#makes a new list of items and stores the ones that have free shipping in it
freeShipping = []
for i in range(0,len(items)):
    ship = items[i].parentTag.find_all("span",class_="s-item__shipping s-item__logisticsCost")
    for s in ship:
        if(s.text=="Free Shipping"):
            items[i].ime= "<b>FREE SHIPPING : </b>" +items[i].ime
            freeShipping.append(items[i])

#merges freeShipping with items
for x in items:
    if(x in freeShipping):
        continue
    else:
        freeShipping.append(x)
br=0
#prints list of items until upper limit
for x in freeShipping:
    if(x.cijena != None and x.cijena<filterCijena and x.cijena != -0.5):
        print(x.ime," | ",x.cijenaString," | ",x.link,"\n")
#prints a list of items in the "Name | Price | LINK" format in a HTML file with clickable links
with open('ebayList.html','w',encoding='utf-8') as file:
    for x in freeShipping:
        if(x.cijena != None and x.cijena<filterCijena and x.cijena != -0.5):
            br+=1
            file.write("<p>"+str(x.ime)+" | "+str(x.cijenaString)+" | "+"<a href = \""+str(x.link)+"\"> LINK </a>"+"</p>")
print("Number of items: ",br)

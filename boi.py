import requests
from bs4 import BeautifulSoup

userSearch = input("What do you want to search for?\n>")
url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw="
userSearch = userSearch.split(' ')
for search in userSearch:
    url += search+"+"
url = url[:-1]
print(url)
r_html = requests.get(url).text
soup = BeautifulSoup(r_html,"html.parser")
chr = soup.find_all('h3',class_="s-item__title")
cijene = soup.find_all('span',class_="s-item__price")
links = soup.find_all('a',class_="s-item__link")
br=0
cijeneFinal = []
for i in range(0,len(cijene)):
    if((cijene[i].parent.parent.parent.parent.parent == cijene[i-1].parent.parent.parent.parent.parent)):
        continue
    else:
        cijeneFinal.append(cijene[i])
values = [len(chr),len(cijeneFinal),len(links)]
print(values)
filterCijena = float(input("Upper limit filter price: "))
print(">"+str(filterCijena))
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
        if(',' in str(cijeneFinal[i].string)[1:]):
            replaced = str(cijeneFinal[i].string)[1:].replace(".","")
            replaced = replaced[:-2]
            replaced = replaced.replace(",",".")
            items[i].cijena = float(replaced)
        else:
            items[i].cijena = float(str(cijeneFinal[i].string)[1:])
    #if the price isn't a price at all we set the value to the first decimal of the first number ($0.13 to $13.5) => 0.1
    else:
        items[i].cijena = float(str(cijeneFinal[i].text)[1:4])
        #print("|||"+str(float(str(cijeneFinal[i].text)[1:4])))
    #we assign the href memeber of the tag to the link variable of object
    items[i].link = links[i]['href']
    items[i].parentTag = chr[i].parent.parent.parent

#for x in items:
#    print("Parent {}".format(items[i].parentTag))
#sorting the array of objects by attribute cijena
items.sort(key=lambda x: x.cijena, reverse=False)

#TODO free shipping
freeShipping = []
for i in range(0,len(items)):
    ship = items[i].parentTag.find_all("span",class_="s-item__shipping s-item__logisticsCost")
    for s in ship:
        if(s.text=="Free Shipping"):
            freeShipping.append(items[i])


#TODO merge rest of items with freeShipping
for x in items:
    if(x in freeShipping):
        continue
    else:
        freeShipping.append(x)




#prints list of items until upper limit
for x in freeShipping:
    if(x.cijena != None and x.cijena<filterCijena and x.cijena != -0.5):
        br+=1
        print(x.ime," | ",x.cijenaString," | ",x.link,"\n")

with open('ebayList.html','w',encoding='utf-8') as file:
    for x in items:
        if(x.cijena != None and x.cijena<filterCijena and x.cijena != -0.5):
            file.write("<p>"+str(x.ime)+" | "+str(x.cijenaString)+" | "+"<a href = \""+str(x.link)+"\"> LINK </a>"+"</p>")
print("Number of items: "+str(br))

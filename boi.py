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
        print(cijene[i].text)
        print(cijene[i-1].text)
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
        #TODO fix the big numbers being a problem by deleting all '.' characters and replacing all ',' characters with '.'
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

#sorting the array of objects by attribute cijena
#items.sort(key=lambda x: x.cijena, reverse=False)
#prints list of items until upper limit
for x in items:
    if(x.cijena != None and x.cijena<filterCijena and x.cijena != -0.5):
        br+=1
        print(x.ime," | ",x.cijenaString," | ",x.link,"\n")

with open('ebayList.txt','w',encoding='utf-8') as file:
    for x in items:
        if(x.cijena != None and x.cijena<filterCijena and x.cijena != -0.5):
            file.write(str(x.ime)+" | "+str(x.cijenaString)+" | "+str(x.link)+"\n")
print("Number of items: "+str(br))

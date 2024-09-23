import requests 
import spacy
import csv
from bs4 import BeautifulSoup 
nlp=spacy.load("en_core_web_sm")
URL = "https://en.wikipedia.org/wiki/List_of_members_of_the_17th_Lok_Sabha"
headers = { 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
        'Accept-Encoding': 'utf-8' } 
r = requests.get(url=URL , headers=headers) 
soup = BeautifulSoup(r.content, 'html5lib') 
my_list = []
prowspan=0
pname=''
crowspan=0
cname=''
for otable in soup.body.find_all('table'):
    pname=''
    cname=''
    is_first_row=True
    otr=otable.tbody.contents[0]
    oth=otr.find_all('th')
    if(len(list(oth))==4):
        if((oth[1].text.strip()=="Constituency") and (oth[2].text.strip()=="Name") and (oth[3].text.strip()=="Party")):
            for otr1 in otable.tbody.find_all('tr'):
                otd=otr1.find_all(['th','td'])
                if(is_first_row == True):
                    is_first_row = False
                    continue
                if(len(otd)==5):
                    dMP = { 'Constituency':otd[1].text.strip() , 'Name':otd[2].text.strip() , 'Party':otd[4].text.strip() , 'hyperlink':otd[2].a["href"] }
                    pname = dMP['Party']
                    cname = dMP['Constituency']
                    if 'rowspan' in otd[4]:
                        prowspan = otd[4]["rowspan"]
                    if 'rowspan' in otd[1]:
                        crowspan = otd[1]["rowspan"]
                    my_list.append(dMP)
                elif(len(otd)==3):
                    dMP = { 'Constituency':otd[1].text.strip() , 'Name':otd[2].text.strip() , 'Party':pname , 'hyperlink':otd[2].a["href"] }
                    cname = dMP['Constituency']
                    if 'rowspan' in otd[1]:
                        crowspan = otd[1]["rowspan"]
                    my_list.append(dMP)
                elif(len(otd)==4):
                    dMP = { 'Constituency':cname , 'Name':otd[1].text.strip() , 'Party':otd[3].text.strip() , 'hyperlink':otd[1].a["href"] }
                    pname = dMP['Party']
                    if 'rowspan' in otd[3]:
                        prowspan = otd[3]["rowspan"]
                    my_list.append(dMP)
                elif(len(otd)==2):
                    if otd[1].has_attr('rowspan'):
                        cname=otd[1].text.strip()
                    elif((otd[1].text.strip()) != "Vacant" ):
                        dMP = { 'Constituency':cname , 'Name':otd[1].text.strip() , 'Party':pname , 'hyperlink':otd[1].a["href"] }
                        my_list.append(dMP)
                elif(len(otd)==1):
                    if((otd[0].text.strip()) != "Vacant" ):
                        dMP = { 'Constituency':cname , 'Name':otd[0].text.strip() , 'Party':pname , 'hyperlink':otd[0].a["href"] }
                        my_list.append(dMP)
#print(my_list)
#print(len(my_list))
csv_file_path = 'D:\\py\\mps\\a.csv'
with open(csv_file_path, 'w', newline='') as csvfile:
     csv_writer = csv.DictWriter(csvfile, fieldnames=my_list[0].keys())
     csv_writer.writeheader()
     csv_writer.writerows(my_list)
    

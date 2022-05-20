import pandas as pd
df=pd.read_csv('cleaned_dataset.csv')  
print(df)
import requests
from bs4 import BeautifulSoup
import re
from time import sleep
from random import randint

base_url="https://www.crunchbase.com/organization/"
my_session = requests.session()
for_cookies = my_session.get(base_url)
cookies = for_cookies.cookies
proxies = {"http": "http://10.10.1.10:3128",
           "https": "http://10.10.1.10:1080"}
headers = {
   
   'authority': 'www.crunchbase.com' ,
   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' ,
   'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8' ,
   'cache-control': 'max-age=0' ,
   'cookie': 'cid=Cign2GI74Yp9qwArBqR2Ag==; pxcts=332db9ce-ab20-11ec-9a61-495544427069; _pxvid=332db29b-ab20-11ec-9a61-495544427069; __cflb=02DiuJLCopmWEhtqNz4kXQy9t2cDTGoJWKF9EDp5jw6uz; xsrf_token=ZpUQYedoj2uCMxPTL/b3JDA51tb2IBhJ3et9FOZ8b1U=; _pxhd=85nnHmcZZEZYG4Zp-6wDamyMeIiIr8V-xN/SQp1M6uvwCcmQ3ZfKr/K3CeqEOv8pigpZ-wEaWVnGIRohtbhsUg; _px3=184fcddb2bf536c6fc744fc486c20517899c67f2e2d48bea51eb774a87868537:RpqnE8TUri/7VgtVM7aGJcCGlzzotubldBa8TPj6sqCfAVU624diCqDxQP2c/kJCvFZL2ZQaSss/sOQQpIZ3VQ==:1000:7cXt9zAT34UGG3t2xuWuZZc+pIijyT0XMWCW/eBZh0HEAdLsPD0AuAOgR3RFnYc8QVaMM+fOP+IXUrEAnnFSU9MWRTQ/+P33/d7ayoPnS8va26wylQPJyNyQveufJpfBuW9oTU0CRn2ahAV91aDrnCmI+/3+HTp0408N5qZXkD7FpapOKszbPzHjFloakdv4b/fv/2s8pndmxJ9+9aa7TQ==' ,
   'referer': 'https://www.crunchbase.com/organization/waywire' ,
   'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Opera";v="86"',
   'sec-fetch-dest': 'document' ,
   'sec-fetch-mode': 'navigate' ,
   'sec-fetch-site': 'same-origin' ,
   'sec-fetch-user': '?1' ,
   'sec-gpc': '1' ,
   'upgrade-insecure-requests': '1' ,
   'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36' ,

  }

diversity_given=[]
rank=[]
num_employee=[]
funding=[]
funding_total=[]
number_of_investor=[]
operating_status=[]

for data in df['slug name']:
    URL=base_url+data
    print(URL)
  

    response = requests.get(URL, headers=headers,cookies=cookies) 
    sleep(randint(1,3))
    print(response.status_code)
    if(response.status_code==200):

        soup=BeautifulSoup(response.content, "html.parser")
        spans = soup.find_all("span")
        for span in spans:
            links = span.find_all('a')
            for link in links:
                link_url=link['href']
            # print(link_url)

                employee_url='/search/people/field/organizations/num_employees_enum/'+data
                funding_type='/search/funding_rounds/field/organizations/last_funding_type/'+data

                ranking=re.search(r'/search/organization.companies/field/organizations/rank_org_company/(\d+)',link_url)
                diversity=re.findall(r'/search/organizations/field/organizations/diversity_spotlights/(\w+)',link_url)
                # print(diversity)
                if(diversity!=None):
                    for i in diversity:
                        if(i=="women"):
                            diversity_given.append(1)
                
                

                if(ranking!=None):
                    ranking_url=str(ranking.group())
                    if(link_url==ranking_url):
                        rank.append(link.contents[0])
                
                if(link['href']==employee_url):
                    num_employee.append(link.contents[0])
                if(link['href']==funding_type):
                    funding.append(link.contents[0])
            
        # print(response.content)
        # print(soup.get_text())

        span_funding_total = soup.find("span" ,  {"class":"component--field-formatter field-type-money ng-star-inserted"})
        if span_funding_total!=None:
            funding_total.append((span_funding_total).text)
        investor=soup.find_all("span",{"class":"component--field-formatter field-type-integer ng-star-inserted"})
        if(len(investor)>1):
            number_of_investor.append(investor[1].text)
        else:
            number_of_investor.append('')
        span=soup.find_all("span",{"class":"component--field-formatter field-type-enum ng-star-inserted"})
        if(len(span)>1):
            operating_status.append(span[1].text)

        
    if(response.status_code==404):
        diversity_given.append(0)
        rank.append('')
        num_employee.append('')
        funding.append('')
        funding_total.append('')
        number_of_investor.append('')
        operating_status.append('')
    if(response.status_code==403):
        break
    print(rank)
    print(num_employee)
    print(funding)
    print(funding_total)
    print(number_of_investor)
    print(operating_status)
    print(diversity_given)


df['rank']=rank
df['number of employee']=num_employee,
df['funding']=funding
df['funding total']=funding_total
df['number of investors']=number_of_investor
df['operating status']=operating_status
df.to_csv('new_data.csv')
print(df)

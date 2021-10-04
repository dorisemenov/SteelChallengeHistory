import requests
from bs4 import BeautifulSoup

def get_scores(uspsa_num):
  # Put USPSA Number here
  url = 'http://scsa.org/classification/'+uspsa_num+'/all'
  #print(url)

  with requests.Session() as s:
    index_page= s.get(url)
    soup = BeautifulSoup(index_page.text, 'html.parser')
 
    for hr2 in soup.find_all('h2'):
      if hr2.text.find('Classification Record for') == 0:
        CompetitorName = hr2.text

    data=[]  
    div = ''
    i = 0
    for table in soup.find_all(id='ClassifiersTable'):
        table_rows = table.find_all('tr')
        for tr in table_rows:
          i = i +1
          th = tr.find("th", {'class': ['text-center']})
          try:
            # Found the table header row labelling the Division
            # Assign this now and all rows thereafter will be marked with this division until the next division is found
            div = th.text
          except:
            cells = tr.find_all('td')
            cells = [ele.text.strip() for ele in cells]
            if len(cells) == 6:
              # remove last column which just has an image showing it was used in classification
              cells.pop(5)
              cells.insert(0, div)
              cells.append(i)
              data.append(cells)
              #print(cells)
 
  return [CompetitorName, data]
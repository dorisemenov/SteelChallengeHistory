import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date

# ----------------------------------------------------------------------------
# scrape Steel Challenge historical scores from SCSA.org using USPSA number
# USPSA must include the 1 or 2 character prefixt
# ----------------------------------------------------------------------------
def get_scores(uspsa_num):
    uspsa_num = uspsa_num.upper()

    # Put USPSA Number here
    url = 'http://scsa.org/classification/' + uspsa_num + '/all'
    #print(url)
    today = date.today()

    with requests.Session() as s:
        index_page = s.get(url)
        soup = BeautifulSoup(index_page.text, 'html.parser')
 
        for hr2 in soup.find_all('h2'):
            if hr2.text.find('Classification Record for') == 0:
                CompetitorName = hr2.text

        data = []  
        div = ''
        i = 0
        for table in soup.find_all(id='ClassifiersTable'):
            table_rows = table.find_all('tr')
            for tr in table_rows:
                i = i + 1
                th = tr.find("th", {'class': ['text-center']})
                try:
                    # Found the table header row labelling the Division
                    # Assign this now and all rows thereafter will be marked with this
                    # division until the next division is found
                    div = th.text
                except:
                    cells = tr.find_all('td')
                    cells = [ele.text.strip() for ele in cells]
                    if len(cells) == 6:
                        # remove last column which just has an image showing it was used in classification
                        cells.pop(5)
                        cells.insert(0, uspsa_num)
                        cells.insert(1, div)
                        cells.append(today)
                        data.append(cells)
                        #print(cells)
 
    # 0 uspsa number
    # 1 division 
    # 2 event
    # 3 date
    # 4 stage
    # 5 time
    # 6 peak

    df = pd.DataFrame(data)
    df.rename(columns={0:'USPSA_NUM',
                       1:'DIVISION',
                       2:'EVENT',
                       3:'EVENT_DATE',
                       4:'STAGE',
                       5:'TIME',
                       6:'PEAK',
                       7:'REFRESH_DT'}, 
                       inplace=True)
    df['EVENT_DATE']= pd.to_datetime(df['EVENT_DATE'], format='%b %d, %Y')
    return df


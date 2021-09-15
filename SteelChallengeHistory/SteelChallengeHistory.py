# Scans SCSA.org for a specified competetor's historical scores
# and puts in a data frame
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import math

# Put USPSA Number here
uspsa = '' 

url = 'http://scsa.org/classification/'+uspsa+'/all'
print(url)

with requests.Session() as s:
  index_page= s.get(url)
  soup = BeautifulSoup(index_page.text, 'html.parser')
  
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

# 0 division
# 1 event
# 2 date
# 3 stage
# 4 time
# 5 peak
df = pd.DataFrame(data)
#print(df)

#df.head()

df.rename(columns={0:'division',
                  1:'event',
                  2:'date',
                  3:'stage',
                  4:'time',
                  5:'peak'}, 
                 inplace=True)
#df.info()

df['time'] = pd.to_numeric(df['time'])
df['date'] = pd.to_datetime(df['date'], format='%b %d, %Y')

mindt = df['date'].min()
maxdt = df['date'].max()

# Next step is to break up the data by division and graph
#print(df.sample(5))
table = pd.pivot_table(df, values='time', index=['date','stage'], columns=['division'])

#print(table.sample(n=5))
numfigs = len(table.columns)

print('Number of figures to create: '+str(numfigs))
numrows = math.ceil(numfigs/2)
fig, ax = plt.subplots(numrows, 2)
#, sharex=True
ax = ax.flatten()

# If # of Divisions are Odd, then hide/remove the last plot
if (numfigs % 2) != 0:  
  ax[numrows*2-1].set_visible(False)

i = 0

for col in (table.columns):    
  # Select column contents by column
  columnSeriesObj = table[col]
  #print('Column Name : ', col)
  divtbl = pd.pivot_table(table, values=col, index='date', columns=['stage'])
  #plt.title(col)
  
  ax[i] = plt.subplot(numrows, 2, i+1)
  ax[i].set_title(col)

  # Year Ticks
  years = YearLocator()   # every year
  months = MonthLocator()  # every month

  maxfmt = mdates.DateFormatter('%y')

  ax[i].set_xlim(mindt, maxdt)
  ax[i].xaxis.set_major_locator(years)
  ax[i].xaxis.set_major_formatter(maxfmt)
  ax[i].tick_params(which='major', length=7)
  
  # Month Ticks
  ax[i].xaxis.set_minor_locator(months)
  minfmt = mdates.DateFormatter('%m')

  ax[i].tick_params(which='minor', length=4)

  plt.locator_params(axis='y', nbins=8) 
  plt.xticks(rotation=60)

  plt.plot(divtbl, label=divtbl.columns.values)
  i = i+1


#print('Number of Divisions: ' + str(i))
plt.subplots_adjust(wspace=0.2, 
                    hspace=0.9)
#plt.legend(loc='upper left')
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import math
from scores import get_scores

# Graphs a competetor's historical scores for each division using Historical scores in SCSA.org
def graph_scores(scores):
  figureTitle = scores[0]
  df = pd.DataFrame(scores[1])

  # 0 division
  # 1 event
  # 2 date
  # 3 stage
  # 4 time
  # 5 peak

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
  #print(df.sample(5))

  df['time'] = pd.to_numeric(df['time'])
  df['date'] = pd.to_datetime(df['date'], format='%b %d, %Y')

  # get overall min and max dates for all divisions to sync x axis in all division graphs
  mindt = df['date'].min()
  maxdt = df['date'].max()

  # similarly sync max time across all divisions for y axis
  maxtime = df['time'].max()

  # Next step is to break up the data by division and graph
  table = pd.pivot_table(df, values='time', index=['date','stage'], columns=['division'])

  #print(table.sample(n=5))

  numfigs = len(table.columns)

  #print('Number of figures to create: '+str(numfigs))
  numrows = math.ceil(numfigs/2)
  fig, ax = plt.subplots(numrows, 2)
  ax = ax.flatten()

  # If # of Divisions are Odd, then hide/remove the last (empty) plot
  if (numfigs % 2) != 0:  
    ax[numrows*2-1].set_visible(False)

  i = 0

  for col in (table.columns):    
    # Select column contents by column
    columnSeriesObj = table[col]

    #print('Column Name : ', col)

    # pivot the data to support graphing stage times as lines
    divtbl = pd.pivot_table(table, values=col, index='date', columns=['stage'])
    #plt.title(col)
  
    ax[i] = plt.subplot(numrows, 2, i+1)
    ax[i].set_title(col)

    # Year Ticks
    years = YearLocator()   # every year
    months = MonthLocator()  # every month

    maxfmt = mdates.DateFormatter('%y')

    ax[i].set_xlim(mindt, maxdt)
    ax[i].set_ylim(0, maxtime)

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
  plt.legend(bbox_to_anchor=(1.1, 1.1))
  plt.suptitle(figureTitle)
  figManager = plt.get_current_fig_manager()
  figManager.window.state("zoomed")
  plt.show()


# Execute a sample
print("Competitor's USPSA Number with prefix (A, TY, L):")
uspsa_num = input()
comp_scores = get_scores(uspsa_num)
graph_scores(comp_scores)
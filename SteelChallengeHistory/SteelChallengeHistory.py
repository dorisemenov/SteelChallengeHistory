from scores import store_scores
from scrape import get_scores
import pandas as pd


# ----------------------------------------------------------------------------
# Pull Competitor's scores and store in database
# ----------------------------------------------------------------------------
def capture(uspsa_num):
    df = get_scores(uspsa_num)
    #df.to_csv(outfile)
    store_scores(df)
    #graph_scores(df)


# Execute a sample
#uspsa_num = 'TY110637'
#outfile = 'd:/temp/scores.csv'

#print("Competitor's USPSA Number with prefix (A, TY, L):")
#uspsa_num = input()

# Populate datbase with_sample competitor's scores

#capture('TY110637') # Nicholas Semenov
#capture('A114373') # Dori Semenov
#capture('TY106435') # Bridget Cunningham
#capture('TY106436') # Emily Cunningham
#capture('TY36570') # KC EUSEBIO

capture('A129661') # Kenshiro Nagata
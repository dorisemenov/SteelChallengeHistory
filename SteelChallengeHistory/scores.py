from sqlalchemy import create_engine
import pymysql
import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
    

username = config['DEFAULT']['DB_USER'] 
passw = config['DEFAULT']['DB_USERPWD'] 

hostname = 'steelchallenge-1.cuscxlctqsax.us-west-2.rds.amazonaws.com'
dbname = 'SCSA'

# ----------------------------------------------------------------------------
# push scraped scores to AWS MySQL db
# ----------------------------------------------------------------------------
def store_scores(df):
    engine = create_engine('mysql+pymysql://'+username+':'+passw+'@'+hostname)
    #+'/'+dbname

    with engine.begin() as connection:
        df.to_sql('SCORE', engine, schema='SCSA', if_exists='append', index=False) 


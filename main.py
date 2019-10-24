#!/usr/bin/env python
# coding: utf-8

'''
I am not using any proxy or user-agent here, as many statistics websites don't block any ip & I am only accesing website with less than 1 attempts/second
'''

# import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import pickle
import re
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')




def scrap():
    '''
    Sraping for data
    '''
    print("--------------------------------------------------------------------------")
    print("Scraping and saving data")
    print("--------------------------------------------------------------------------")
    # specify the url
    url = 'http://howstat.com/cricket/Statistics/Players/PlayerYears_ODI.asp?PlayerID='
    idList = [] # List to hold Id's of ODI player
    idName = {} # Dict to hold Id's and corresponding names 

    # As wesite's PlayerID is of 4 digits(Max 9999 players possible)
    for id in range(1,10000): 
        id = str(id).zfill(4)
        page = requests.get(url+id)
        # parse the html using beautiful soup and store in variable soup
        soup = BeautifulSoup(page.content,'lxml')
        title = soup.title.text
        # Player haven't played any ODI
        if 'Error' in title:
            continue
        idList.append(id)
        pName = re.split('-',title)[1].strip() # Extract Player name
        idName[id] = pName
        table = soup.find_all(id="bat")
        df = pd.read_html(str(table))
        df = df[0]
        df = df.iloc[1:-1,df.columns.isin(list('08'))] # Extract Year and score columns only
        df[0][1] = pName
        df.to_csv('CSV\\'+id+'.csv',index = False) # Save player's record 

    # Save list and dict for future use    
    # write dict to a file
    output = open('idName.pkl', 'wb')
    pickle.dump(idName, output)
    output.close()

    # write list to a file
    output = open('idList.pkl', 'wb')
    pickle.dump(idList, output)
    output.close()


# In[ ]:


def task1():
    '''
    Task 1: List of all ODI players
    '''
    print("--------------------------------------------------------------------------")
    print("Task 1:List of all ODI players\n")
    print("--------------------------------------------------------------------------")
    # read dict back from the file
    pkl_file = open('idName.pkl', 'rb')
    idName = pickle.load(pkl_file)
    pkl_file.close()
    # Sort according to player name
    sorted_d = sorted(idName.items(), key=lambda kv: kv[1])
    print("List of all the ODI players(In alphabetical order):"+'\033[1m'+"\n\nName\t\t\tID"+'\033[0m')
    for Id, name in sorted_d:
        print(f"{name:<30}\t{Id}")


def task23():
    '''
    Task 2: Runs of player
    '''
    print("--------------------------------------------------------------------------")
    print("\n\nTask 2:Runs of player\n")
    print("--------------------------------------------------------------------------")
    # read dict back from the file
    pkl_file = open('idName.pkl', 'rb')
    idName = pickle.load(pkl_file)
    pkl_file.close()

    # read list back from the file
    pkl_file = open('idList.pkl', 'rb')
    idList = pickle.load(pkl_file)
    pkl_file.close()

    print("\n\nPlease enter the ID of player to see his scores:")
    Id = input()
    Id = Id.zfill(4)
    if Id in idList:
        df = pd.read_csv('CSV\\'+Id+'.csv')
        years = list(df.iloc[1:,0])
        runs = list(df.iloc[1:,1])
        pName = df.iloc[0,0]
        cRuns = []
        x = 0
        for i in range(0, len(runs)):
            x = x+int(runs[i])
            cRuns.append(x)
            runs[i] = int(runs[i])
        index = np.arange(len(years))
        # Year-wise scores plot
        plt.bar(index, runs,color='b')
        plt.xlabel('Years')
        plt.ylabel('Total Runs In The Year')
        plt.xticks(index, years,rotation=30)
        plt.title('Runs scored by '+pName)
        for i, run in enumerate(runs):
            plt.text(x=i-0.4,y=run+1,s=str(run))
        plt.show()
        
        '''
        Task 3: Cumulative scores of player
        '''
        print("--------------------------------------------------------------------------")
        print("Task 3: Cumulative scores of player\n")
        print("--------------------------------------------------------------------------")
        # Cumulative scores plot
        plt.bar(index, cRuns,color='r')
        plt.xlabel('Years')
        plt.ylabel('Cumulative Runs Till Year')
        plt.xticks(index, years,rotation=30)
        plt.title('Cumulative Runs scored by '+pName)
        for i, run in enumerate(cRuns):
            plt.text(x=i-0.4,y=run,s=str(run))
        plt.show()
    else:
        print("Please enter a valid ID")
        task23()


# In[ ]:


def main():
    scrapAgain = False
    if scrapAgain:
        scrap()
    else:       
        # Perform task
        task1()
        task23()
    
if __name__== "__main__":
    main()


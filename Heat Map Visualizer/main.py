# -*- coding: utf-8 -*-
import pandas as pd
import seaborn as sns
"""
Created on Thu Jun 23 15:06:01 2022

@author: kevjia
"""

TEST2 = 'G:\Info\Exchange\Otto Bachmann\Tekscan Demo Data -13042022\Ballard - test 2.csv'
TEST3 = 'G:\Info\Exchange\Otto Bachmann\Tekscan Demo Data -13042022\Ballard - test 3.csv'
TEST4 = 'G:\Info\Exchange\Otto Bachmann\Tekscan Demo Data -13042022\Ballard - test 4.csv'


def singleframeHmap(file, destination): # for Test 2 and 3
    
    # since data doesn't use column headers, set header=None to properly format data
    df =  pd.read_csv(file, skiprows = 27, encoding='ansi',low_memory = False, header=None)
        
    df.dropna(inplace = True)
    df = df.astype(float)
    ax = sns.heatmap(df)  
    
    print(df)
    
    for item in ax.get_yticklabels():
        item.set_rotation(0)

    for item in ax.get_xticklabels():
        item.set_rotation(90)
    
    # invert axis for 'grid' appearance
    ax.invert_yaxis()
    
    # add simple header
    hmapTitle = file.split('\\')[-1].replace('.csv', '')
    ax.set_title(hmapTitle)
                           
    # export hmap to selected directory
    figure = ax.get_figure()    
    figSave = str(destination + '\\' + hmapTitle + '.png')
    figure.savefig('%s' % figSave, dpi=400)
    
    # clear current hmap to prevent overlapping
    figure.clf()

def multiframeHmap(file, destination, rowsPerFrame):
    df =  pd.read_csv(file, skiprows = 27, encoding='ansi',low_memory = False, header=None) 
    
    df.dropna(inplace = True)
    df = df.astype(int)
    
    # define case-by-case variables
    MAXROWS = int(df.shape[0])
    MAXFRAMES = int(MAXROWS / rowsPerFrame)
    
    framesDict = {}
    
    for frame in range (MAXFRAMES - 1):
        tempFrameData = []
        for row in range(0, MAXROWS, rowsPerFrame):
            for i in range(row, row + rowsPerFrame, 1):
                print(i)
                tempFrameData.append(df.iloc[i])
            frameDf = pd.concat(tempFrameData, axis=0, ignore_index=True)
            framesDict[frame] = frameDf



    # obtain rows
   # print(df.iloc[17379]) 
    
    # 17380 rows x 44 columns
    # What we basically have is 395 frames of 44x44 hmaps
    
    
    #print(df)
    return 0


# call functions
DESTINATION = 'G:\Info\Exchange\Kevin J\Heat Map Visualziation'
#singleframeHmap(TEST2, DESTINATION)
#singleframeHmap(TEST3, DESTINATION)
multiframeHmap(TEST4, DESTINATION, 44)  # Each frame is 44x44
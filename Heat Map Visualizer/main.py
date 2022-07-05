# -*- coding: utf-8 -*-
import pandas as pd
import seaborn as sns
import os
import cv2
import re

"""
Created on 2022-06-24

@author: kevjia

Purpose: To allow for the graphing of single frame and multiframe heatmaps using functions. 

         For singleframe heatmaps, the procedure is simple as the data is simply passed as a pandas dataframe and graphed using
         the seaborn module

         For multiframe heatmaps, code sorts raw data in order to sample each frame systematically. 
         A Hmap is generated for each frame, which are then concatenated into a .mp4 video using the cv2 module.

Notes:
        - Code was designed in a semi-flexible way e.g for multiframe heatmaps, users can pass the rows per frame to help 
        the code slice the raw data file properly.
        - If the format of the raw data files change in the future, the code won't work as is and will require modifications
"""
def singleframeHmap(file, destination): # for Test 2 and 3
    
    # since data doesn't use column headers, set header=None to properly format data
    df =  pd.read_csv(file, skiprows = 27, encoding='ansi',low_memory = False, header=None)
        
    df.dropna(inplace = True)
    df = df.astype(float)
    ax = sns.heatmap(df)  
    
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

def animateFrame(frameName, dataframe, destination): # Similar function to above, but without the skiprows
    ax = sns.heatmap(dataframe)  
    
    for item in ax.get_yticklabels():
        item.set_rotation(0)

    for item in ax.get_xticklabels():
        item.set_rotation(90)
    
    # invert axis for 'grid' appearance
    ax.invert_yaxis()    
    
    # frame title
    hmapTitle = ('Frame ' + str(frameName))
    ax.set_title(hmapTitle)
                           
    # export hmap to selected directory
    figure = ax.get_figure()    
    figSave = str(destination + '\\' + hmapTitle + '.png')
    figure.savefig('%s' % figSave, dpi=400)
    
    # clear current hmap to prevent overlapping
    figure.clf()   

def key(value):
    """Extract numbers from string and return a tuple of the numeric values"""
    return tuple(map(int, re.findall('\d+', value)))

def multiframeHmap(file, destination, imageDirectory, rowsPerFrame):    # for Test 4
    df =  pd.read_csv(file, skiprows = 27, encoding='ansi',low_memory = False, header=None) 
    
    df.dropna(inplace = True)
    df = df.astype(int)
    
    # define case-by-case variables
    MAXROWS = int(df.shape[0])
    
    framesDict = {}

    # using pandas .iloc, we can split the dataframe evenly depending on the parameters 
    for row in range(0, MAXROWS, rowsPerFrame): # this is actually more "frame" than "row"
        dfSlice = df.iloc[row: row + rowsPerFrame]
        # for clarity, convert number of rows to frame no. ranging from 0-394
        framesDict[row/rowsPerFrame] = dfSlice

    # iterate through dictionary and graph each hmap frame
    for item in framesDict:
        animateFrame(item, framesDict[item], imageDirectory)

    # combine .pngs into frame-by-frame video
    imageList = []
    for image in os.listdir(imageDirectory):
        imageList.append(image)

    # sort list of images in terms of ascending frame order
    imageList = sorted(imageList, key=key)
    
    # get image parameters from first image in list      
    # not index 0 due to Thumbs.db somehow ending up in the list
    imgParams = cv2.imread(os.path.join(imageDirectory, imageList[1]))
    height, width, layers = imgParams.shape
    size = (width, height)
    
    fileTitle = 'Ballard Test 4 Video'
    VIDEXT = '.mp4'
    
    vidTitle = os.path.join(destination, (fileTitle + VIDEXT) )

    # change this to change playback speed
    frameRate = 2.0
    
    out = cv2.VideoWriter(vidTitle, cv2.VideoWriter_fourcc(*'MP4V'), frameRate, size)
    
    i = 0
    for image in imageList:
        if image.endswith('.png'):
            imagePath = os.path.join(imageDirectory, image)
            frame = cv2.imread(imagePath)
            out.write(frame)
            print('Frame ' + str(i) + ' has been rendered!')
            i += 1
    
    # release all frames
    out.release()
        
# call functions to generate test 2, 3, 4 data
DESTINATION = 'G:\Info\Exchange\Kevin J\Heat Map Visualziation'
IMAGEFOLDER = 'G:\Info\Exchange\Kevin J\Heat Map Visualziation\Hmap Frames'


TEST2 = 'G:\Info\Exchange\Kevin J\Heat Map Visualziation\Raw Data\Ballard - test 2.csv' #'G:\Info\Exchange\Otto Bachmann\Tekscan Demo Data -13042022\Ballard - test 2.csv'
TEST3 = 'G:\Info\Exchange\Kevin J\Heat Map Visualziation\Raw Data\Ballard - test 3.csv' #'G:\Info\Exchange\Otto Bachmann\Tekscan Demo Data -13042022\Ballard - test 3.csv'
TEST4 = 'G:\Info\Exchange\Kevin J\Heat Map Visualziation\Raw Data\Ballard - test 4.csv' #'G:\Info\Exchange\Otto Bachmann\Tekscan Demo Data -13042022\Ballard - test 4.csv'

singleframeHmap(TEST2, DESTINATION)
singleframeHmap(TEST3, DESTINATION)
multiframeHmap(TEST4, DESTINATION, IMAGEFOLDER, 44)  # Each frame is 44x44

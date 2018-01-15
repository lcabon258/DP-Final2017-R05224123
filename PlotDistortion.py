  # -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 22:29:34 2017

@author: WayneSun
"""

import numpy as np
import cv2
import glob
import os

from matplotlib import pyplot as plt 

from PIL import Image
from PIL.ExifTags import TAGS

def Change_EXIF_KEYS(EXIF_DICT):
    """Use PIL TAGS module to change the key from ID to String"""
    NewDict = {} # Save new exif data
    for k,v in iter(EXIF_DICT.items()):
        #print("k,v = {} , {}".format(k,v))
        NewDict[TAGS.get(k)]=v
    return NewDict


def get_img_size_from_exif(imgpath):
    EXIF = Image.open(imgpath)._getexif()
    EXIF = Change_EXIF_KEYS(EXIF)
    ExifImageHeight = EXIF["ExifImageHeight"] #rows
    ExifImageWidth = EXIF["ExifImageWidth"] #columns
    
    return (ExifImageWidth,ExifImageHeight)

class sensor_size_finder(object):    
    def __init__(self):    
        self.sensor_size={}
    def add(self,CameraName,Col_Row_arr):
        self.sensor_size[CameraName]=Col_Row_arr
    def find(self,key):
        return self.sensor_size[key]
        
        
def main(K1,K2,K3,P1,P2):
    #init
    s=sensor_size_finder()
    s.add("NIKON D700",(36. , 23.9))
    #D700 Sensor size:
    D700_col,D700_row=s.find("NIKON D700")
    print(D700_col,D700_row)
    #pixel size:
    ImgCol = 4256
    ImgRow = 2832
    SizeCol = D700_col/ImgCol
    SizeRow = D700_row/ImgRow
    PixSize = (SizeCol+SizeRow)/2*1e3
    interval=20
    print (SizeCol,SizeRow,PixSize)
    
    ColArr = np.arange(-ImgCol/2,ImgCol/2,interval)
    RowArr = np.arange(-ImgRow/2,ImgRow/2,interval) 
    X,Y = np.meshgrid(ColArr,RowArr)

    ## Radial Distortion
    r = np.sqrt(np.power(X,2)+np.power(Y,2))
    XRvec = X*(K1*np.power(r,2)+K2*np.power(r,4)+K3*np.power(r,6))
    YRvec = Y*(K1*np.power(r,2)+K2*np.power(r,4)+K3*np.power(r,6))
    ZR = np.sqrt(np.power(XRvec,2)+np.power(YRvec,2))
    ## Decentering Distortion
    XDvec = P1*(np.power(r,2)+2*np.power(X,2))+2.*P2*X*Y
    YDvec = P2*(np.power(r,2)+2*np.power(Y,2))+2.*P1*X*Y
    ZD = np.sqrt(np.power(XDvec,2)+np.power(YDvec,2))
    #Plot
    fig,ax = plt.subplots(1,2)
    ax[0].quiver(X,Y,XRvec,YRvec)
    CS1 = ax[0].contour(X,Y,ZR)
    ax[0].clabel(CS1,inline=1,fontsize=10)
    ax[0].set_title("Radial Distortion")
    ax[0].set_xlabel("Column")
    ax[0].set_ylabel("Row")
    ax[0].set_aspect('equal')

    ax[1].quiver(X,Y,XDvec,YDvec)
    CS2 = ax[1].contour(X,Y,ZD)
    ax[1].clabel(CS2,inline=1,fontsize=10)
    ax[1].set_title("Decentering Distortion")
    ax[1].set_xlabel("Column")
    ax[1].set_ylabel("Row")
    ax[1].set_aspect('equal')
    fig.show()
    
    fig2,ax2 = plt.subplots(1,1)
    ax2.quiver(X,Y,XRvec+XDvec,YRvec+YDvec)
    ax2.set_title("Lens Distortion")
    ax2.set_xlabel("Column")
    ax2.set_ylabel("Row")
    ax2.set_aspect('equal')
    fig2.show()    
    
    # Yang Ver
    ColArr = np.arange(-ImgCol/2*PixSize,ImgCol/2*PixSize,interval*PixSize)
    RowArr = np.arange(-ImgRow/2*PixSize,ImgRow/2*PixSize,interval*PixSize) 
    X,Y = np.meshgrid(ColArr,RowArr)
    ## Radial Distortion
    r = np.sqrt(np.power(X,2)+np.power(Y,2))
    dr = K1*np.power(r,3)+K2*np.power(r,5)+K3*np.power(r,7)
    dxr = X*dr/r
    dyr = Y*dr/r
    dzr = np.sqrt(np.power(dxr,2)+np.power(dyr,2))/PixSize/np.sqrt(2)
    ## Decentering Distortion
    dxd = P1*(np.power(r,2)+2*np.power(X,2))+2.*P2*X*Y
    dyd = P2*(np.power(r,2)+2*np.power(Y,2))+2.*P1*X*Y
    dzd = np.sqrt(np.power(dxd,2)+np.power(dyd,2))/PixSize/np.sqrt(2)

    #Plot
    fig3,ax3 = plt.subplots(1,2)
    ax3[0].quiver(X/PixSize+ImgCol/2,Y/PixSize+ImgRow/2,dxr,dyr)
    CS3 = ax3[0].contour(X/PixSize+ImgCol/2,Y/PixSize+ImgRow/2,dzr)
    ax3[0].clabel(CS3,inline=1,fontsize=10)
    ax3[0].set_title("Radial Distortion")
    ax3[0].set_xlabel("Column")
    ax3[0].set_ylabel("Row")
    ax3[0].set_aspect('equal')

    ax3[1].quiver(X/PixSize+ImgCol/2,Y/PixSize+ImgRow/2,dxd,dyd)
    CS4 = ax3[1].contour(X/PixSize+ImgCol/2,Y/PixSize+ImgRow/2,dzd)
    ax3[1].clabel(CS4,inline=1,fontsize=10)
    ax3[1].set_title("Decentering Distortion")
    ax3[1].set_xlabel("Column")
    ax3[1].set_ylabel("Row")
    ax3[1].set_aspect('equal')
    fig3.show()

if __name__ == "__main__":
    K1 = -0.0818055
    K2 = 0.0914584
    K3 = -0.0225251
    K4 = 0 #fisheye uses
    K5 = 0 #fisheye uses
    P1 = -0.000347622
    P2 = 0.00024699

    main(K1,K2,K3,P1,P2)

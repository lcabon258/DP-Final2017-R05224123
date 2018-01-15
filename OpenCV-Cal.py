# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 13:41:40 2017

@author: CWSun @ GISLAB-2
@mail: r05224123@ntu.edu.tw
"""
import numpy as np
import cv2
import glob
import os

path=r"D:\CWSunProject\CameraCalibration\Fuji"
os.chdir(path)

# Paramters
ChessRow = 13
ChessColumn = 13 
ChessSize = 30 #mm

# 計算需要的參數
InnerRow = ChessRow - 1
InnerColumn = ChessColumn - 1

ObjP=np.zeros((InnerRow*InnerColumn,3), np.float32)
ObjP[:,:2] = np.mgrid[0:InnerRow,0:InnerColumn].T.reshape(-1,2)

# 迭代終止條件
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 準備儲存物點與對應的像點的陣列，以供校正時使用。
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# 找出所有的影像
images = glob.glob('*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # 嘗試找到棋盤的內角
    ret, corners = cv2.findChessboardCorners(gray, (InnerRow,InnerColumn),None)

    # 如果有找到的話，ret 會傳回 True
    if ret == True:
        objpoints.append(ObjP)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # 在視窗中顯示供參考
        img = cv2.drawChessboardCorners(img, (InnerRow,InnerColumn), corners2,ret)
        cv2.imshow('img',img)
        cv2.waitKey(1000)

cv2.destroyAllWindows()
# 說明：https://docs.opencv.org/3.0-beta/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#calibratecamera 
# camera matrix, distortion coefficients, rotation and translation vectors
# distortion coefficients (k1,k2,p1,p2[,k3[,k4,k5,k6[,s1,s2,s3,s4[,τx,τy]]]]) of 4, 5, 8, 12 or 14 elements. 
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

print("ret")
print(ret)
print("mtx")
print(mtx)
print("dist")
print(dist)
print("rvecs")
print(rvecs)
print("tvecs")
print(tvecs)

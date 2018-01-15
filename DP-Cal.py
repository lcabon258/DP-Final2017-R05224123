#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 10:51:11 2017

@author: Aspiring_Wayne
"""

import Coordinate_Calculator as CC
import csv,io

class CoordinateCalculator(object):
    def __init__(self,StationName):
        self.records = []
        self.StationName = StationName
        self.H = 0.
        self.HA_Ref=None
    

    def CSV_Load(self,csv_path):
        with io.open(csv_path,"rt") as f:
            r = csv.reader(f)
            for R in r :
                if R[0].startswith("H="):
                    self.H=float(R[0].split("=")[1])
                    print("Set Instrument Height to {}".format(self.H))
                    continue
                elif R[0].startswith("後視"):
                    ID = R[0]
                    HA_p = R[1].split(":")
                    HA_b = R[2].split(":")
                    VA_p = R[3].split(":")
                    VA_b = R[4].split(":")
                    SD = float(R[5])
                    Record = CC.Record(self.StationName,ID,self.H,SD,\
                                   HA_p[0],HA_p[1],HA_p[2],HA_b[0],HA_b[1],HA_b[2],
                                   VA_p[0],VA_p[1],VA_p[2],VA_b[0],VA_b[1],VA_b[2])
                    self.HA_Ref = Record.HA
                ID = R[0]
                HA_p = R[1].split(":")
                HA_b = R[2].split(":")
                VA_p = R[3].split(":")
                VA_b = R[4].split(":")
                SD = float(R[5])
                Record = CC.Record(self.StationName,ID,self.H,SD,\
                                   HA_p[0],HA_p[1],HA_p[2],HA_b[0],HA_b[1],HA_b[2],
                                   VA_p[0],VA_p[1],VA_p[2],VA_b[0],VA_b[1],VA_b[2])
                print(R)
                print(str(Record))
                self.records.append(Record)
        print("{} records loaded from csv file.".format(len(self.records)))
    
    def Write_Coordinates(self,out_path):
        with io.open(out_path,"wt") as of:
            w = csv.writer(of)
            w.writerow(["ID","X","Y","Z"])
            print("HA_Ref = {}".format(str(self.HA_Ref)))
            #print("Type = {}".format(type(self.HA_Ref)))
            for i in range(len(self.records)):
                #C = self.records[i].calculate_coordinate(HA_Ref)
                C = self.records[i].calculate_coordinate(self.HA_Ref)
                w.writerow([self.records[i].Circle_ID,C[0],C[1],C[2]])

class CoordinateCalculator_Ref(object):
    def __init__(self,StationName):
        self.records = []
        self.StationName = StationName
        self.H = 0.
        self.HA_Ref=None
    

    def CSV_Load(self,csv_path,Ref_Angle=None):
        with io.open(csv_path,"rt") as f:
            r = csv.reader(f)
            self.HA_Ref = Ref_Angle
            for R in r :
                if R[0].startswith("H="):
                    self.H=float(R[0].split("=")[1])
                    print("Set Instrument Height to {}".format(self.H))
                    continue
                ID = R[0]
                HA_p = R[1].split(":")
                HA_b = R[2].split(":")
                VA_p = R[3].split(":")
                VA_b = R[4].split(":")
                SD = float(R[5])
                Record = CC.Referenced_Record(self.StationName,ID,self.H,SD,\
                                   HA_p[0],HA_p[1],HA_p[2],HA_b[0],HA_b[1],HA_b[2],
                                   VA_p[0],VA_p[1],VA_p[2],VA_b[0],VA_b[1],VA_b[2],\
                                   Ref_Angle)
                print(R)
                print(str(Record))
                self.records.append(Record)
        print("{} records loaded from csv file.".format(len(self.records)))
    
    def Write_Coordinates(self,out_path,Ad,Am,As):
        with io.open(out_path,"wt") as of:
            w = csv.writer(of)
            w.writerow(["ID","X","Y","Z"])
            print("HA_Ref = {}".format(str(self.HA_Ref)))
            #print("Type = {}".format(type(self.HA_Ref)))
            for i in range(len(self.records)):
                #C = self.records[i].calculate_coordinate(HA_Ref)
                C = self.records[i].calculate_coordinate2(CC.Angle(Ad,Am,As))
                w.writerow([self.records[i].Circle_ID,C[0],C[1],C[2]])


if __name__ == "__main__":
    csv_path=r"D:\DP-M9全測站測量資料1-cp950.csv"
    out=r"D:\DP-M9全測站測量資料1-cp950-out.csv"
    CC2 = CoordinateCalculator("Front")
    CC2.CSV_Load(csv_path)
    CC2.Write_Coordinates(out)
    
    #Station 2
    csv_path=r"D:\DP-M9全測站測量資料2-cp950.csv"
    out=r"D:\DP-M9全測站測量資料2-cp950-out.csv"
    CC3 = CoordinateCalculator_Ref("Back")
    CC3.CSV_Load(csv_path,CC.Angle(359,59,54))
    CC3.Write_Coordinates(out,38,47,36)    

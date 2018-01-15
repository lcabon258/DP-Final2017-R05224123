# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 11:52:14 2017

@author: GISLAB-2
"""
import numpy as np

def dms2dd(AngleObj):
    """degree minutes to decimal degree
    input:
        AngleObj : Object with deg,mi,sec record
    output:
        dd : decimal degree (float)"""
    return AngleObj.deg+(AngleObj.mi/60)+(AngleObj.sec/3600)

def dd2dms(dd,out_type="AZI"):
    """decimal degree to degree minute second
    input:
        dd : decimal degree (float)
        out_type : either "AZI" or "ANG" 
            AZi : return Azimuth object
            ANG : return Angle object
    output : 
        Angle or Azimuth object
    """
    d = int(dd)
    m = int((dd-d)*60)
    s = (dd-d-m/60)*3600
    if  out_type == "AZI":
        return Azimuth(d,m,s)
    elif out_type == "ANG":
        return Angle(d,m,s)
    else:
        raise ValueError("Keywords of \"out_type\" must be \"AZI\" or \"ANG\"")

class Angle(object):
    def __init__(self,deg,mi,sec):
        self.deg = int(deg)
        self.mi = int(mi)
        self.sec = float(sec)
        self.dd = self.dms2dd()
    
    def set_angle(self,deg,mi,sec):
        self.deg = deg
        self.mi = mi
        self.sec = sec
        
    def dms2dd(self):
        """degree minute second to secimal degree"""
        return self.deg+(self.mi/60)+(self.sec/3600)
    
    def check_angle(self):
        if self.sec >= 60.:
            self.sec = self.sec - 60
            self.mi = self.mi + 1
        elif self.sec < 0.:
            self.sec = self.sec + 60.
            self.mi = self.mi - 1
        if self.mi >= 60:
            self.mi = self.mi -60
            self.deg = self.deg + 1
        elif self.mi < 0:
            self.mi = self.mi + 60
            self.deg = self.deg - 1
        return
    
    def check_angle2(self,AngObj):
        if AngObj.sec >= 60.:
            AngObj.sec = AngObj.sec - 60.
            AngObj.mi = AngObj.mi + 1
        elif AngObj.sec < 0.:
            AngObj.sec = AngObj.sec + 60.
            AngObj.mi = AngObj.mi - 1
        if AngObj.mi >= 60:
            AngObj.mi = AngObj.mi -60
            AngObj.deg = AngObj.deg + 1
        elif AngObj.mi < 0:
            AngObj.mi = AngObj.mi + 60
            AngObj.deg = AngObj.deg - 1
            
    # Operators
    def __str__(self):
        return "{:}°{:}'{:.4}\"".format(self.deg,self.mi,self.sec)
    
    def __add__(self,other):
        if other.deg >= 0 :
            result = Angle(self.deg,self.mi,self.sec)
            #print("__add__, result before operate : {}".format(str(result)))
            result.deg = result.deg + other.deg
            #print("__add__, result.deg : {}".format(result.deg))
            result.mi = result.mi + other.mi
            #print("__add__, result.mi : {}".format(result.mi))
            result.sec = result.sec + other.sec
            #print("__add__, result.sec : {}".format(result.sec))
            result.check_angle()
            #print("__add__, result after check : {}".format(str(result)))
        else :
            result = self.__sub__(Angle(-1 * other.deg,other.mi,other.sec) )
        return result
    
    def __add__2(self,deg,mi,sec):
        """Case : sub a negative value"""
        result = Angle(self.deg,self.mi,self.sec)
        result.sec = result.sec + sec
        result.mi = result.mi + mi
        result.deg = result.deg + deg
        result.check_angle()
        return result
    
    def __radd__(self,other):
        if other == 0 :
            return self
        else:
            return self.__add__(other)
    
    def __sub__(self,other):
        if other.deg >= 0:
            if self.__ge__(other):
                #print("__sub__, self >= other.deg")
                result = Angle(self.deg,self.mi,self.sec)
                result.sec = result.sec - other.sec
                result.mi = result.mi - other.mi
                result.deg = result.deg - other.deg
                result.check_angle()
            else:
                #print("__sub__, self < other.deg")
                result = Angle(self.deg,self.mi,self.sec)
                result.sec = other.sec - result.sec
                result.mi = other.mi - result.mi
                result.deg = (other.deg - result.deg)
                result.check_angle()
                result.deg = -1 * result.deg
        else:
            result = self.__add__(Angle(-1 * other.deg,other.mi,other.sec))
        return result
    
    def __sub__2(self,deg,mi,sec):
        """Case : add a negative value"""
        result = Angle(self.deg,self.mi,self.sec)
        result.sec = result.sec - sec
        result.mi = result.mi - mi
        result.deg = result.deg - deg
        result.check_angle()
        return result
    
    def __rsub__(self,other):
        if other == 0 :
            return self
        else:
            return self.__sub__(other)
    
    def __truediv__(self,other):
        float(other)
        dd = dms2dd(Angle(self.deg,self.mi,self.sec))
        dd = dd/other
        return dd2dms(dd,"ANG")
    # Bool operator
    def __lt__(self,other):#<
        if self.deg < other.deg:
            return True
        elif self.deg == other.deg:
            if self.mi < other.mi:
                return True
            elif self.mi == other.mi:
                if self.sec < other.sec:
                    return True
        else:
            return False
        
    def __gt__(self,other):#>
        if self.deg > other.deg:
            return True
        elif self.deg == other.deg:
            if self.mi > other.mi:
                return True
            elif self.mi == other.mi:
                if self.sec > other.sec:
                    return True
        else:
            return False
        
    def __eq__(self,other):#==
        if other == None :
            return False
        else:
            return ( (self.deg == other.deg) and (self.mi == other.mi) and (self.sec == other.sec) )
    
    def __ge__(self,other):#>=
        return (self.__gt__(other) or self.__eq__(other))
    
    def __le__(self,other):#<=
        return (self.__lt__(other) or self.__eq__(other))
    
class Azimuth(Angle):
    def __init__(self,deg,mi,sec):
        super().__init__(deg,mi,sec)
        self.dd = self.dms2dd()
        self.angle = Angle(self.deg,self.mi,self.sec)
        self.check_angle()
        
    def check_angle(self):
        if self.sec >= 60.:
            self.sec = self.sec - 60.
            self.mi = self.mi + 1.
        elif self.sec < 0.:
            self.sec = self.sec + 60.
            self.mi = self.mi - 1.
            
        if self.mi >= 60.:
            self.mi = self.mi -60.
            self.deg = self.deg + 1.
        elif self.mi < 0.:
            self.mi = self.mi + 60.
            self.deg = self.deg - 1.
            
        if self.deg >= 360:
            self.deg = self.deg - 360.
        elif self.deg < 0. :
            self.sec = 60 - self.sec
            self.mi = 59. - self.mi
            self.deg = self.deg + 359.
            self.check_angle()
        return
    
    def dd2dms(self,dd):
        d = int(dd)
        m = int((dd-d)*60)
        s = (dd-d-m/60)*3600
        return Azimuth(d,m,s)
        
    def check_angle2(self,AngObj):
        if AngObj.deg < 0.:
            AngObj.sec = 60 - AngObj.sec
            AngObj.mi = 59. - AngObj.mi
            AngObj.deg = AngObj.deg + 359.
            
        if AngObj.sec >= 60.:
            AngObj.sec = AngObj.sec - 60.
            AngObj.mi = AngObj.mi + 1
        elif AngObj.sec < 0.:
            AngObj.sec = AngObj.sec + 60.
            AngObj.mi = AngObj.mi - 1
            
        if AngObj.mi >= 60:
            AngObj.mi = AngObj.mi -60
            AngObj.deg = AngObj.deg + 1
        elif AngObj.mi < 0:
            AngObj.mi = AngObj.mi + 60
            AngObj.deg = AngObj.deg - 1
            
        if AngObj.deg >= 360:
            AngObj.deg = AngObj.deg - 360

        """
        elif AngObj.deg < 0. :
            AngObj.sec = 60 - AngObj.sec
            AngObj.mi = 59 - AngObj.mi
            AngObj.deg = AngObj.deg + 359
            AngObj.check_angle()
        """
        return Azimuth(AngObj.deg,AngObj.mi,AngObj.sec)
    def __str__(self):
        return "{:}°{:}'{:.4}\"".format(self.deg,self.mi,self.sec)
    def __add__(self,other):
        #print("__add__ Other: {}".format(other))
        if other.deg >= 0 :
            result = Azimuth(self.deg,self.mi,self.sec)
            result.deg = result.deg + other.deg
            result.mi = result.mi + other.mi
            result.sec = result.sec + other.sec
            result.check_angle()
        else :
            result = self.__sub__(Azimuth(-1.*other.deg,other.mi,other.sec))
        return result
    
    def __add__2(self,deg,mi,sec):
        """Case : sub a negative value"""
        result = Azimuth(self.deg,self.mi,self.sec)
        #print("__add__2 initial result : {}".format(result))
        result.sec = result.sec + sec
        result.mi = result.mi + mi
        result.deg = result.deg + deg
        result.check_angle()
        return result
    def __sub__(self,other):
        #print("__sub__ Other: {}".format(other))
        if other.deg >= 0:
            if self >= other:
                result = Angle(self.deg,self.mi,self.sec)
                #print("__sub__, self >= other, result : {}".format(str(result)))
                result.sec = result.sec - other.sec
                #print("__sub__, self >= other,result.sec : {}".format(result.sec))
                result.mi = result.mi - other.mi
                #print("__sub__, self >= other,result.mi : {}".format(result.mi))
                result.deg = result.deg - other.deg
                #print("__sub__, self >= other,result.deg : {}".format(result.deg))
                
                result = self.check_angle2(result)
                #print("__sub__, self >= other,result : {}".format(result))
            else:
                result = Angle(self.deg,self.mi,self.sec)
                #print("__sub__, self < other,result : {}".format(str(result)))
                result.sec = other.sec - result.sec
                #print("__sub__, self < other,result.sec : {}".format(result.sec))
                result.mi = other.mi - result.mi
                #print("__sub__, self < other,result.mi : {}".format(result.mi))
                result.deg = other.deg - result.deg
                #print("__sub__, self < other,result.deg : {}".format(result.deg))
                result.check_angle() # Angle object
                #print("__sub__, self < other,Angle check2 result : {}".format(result))
                result.deg = -1 * result.deg
                #print("__sub__, self < other,result.deg : {}".format(result))
                self.check_angle2(result)
                #print("__sub__, self < other,self.check2 result : {}".format(result))
                
        else:
            result = self.__add__(Azimuth(-1.*other.deg,other.mi,other.sec))
        return result
    
    def __sub__2(self,deg,mi,sec):
        """Case : add a negative value"""
        result = Azimuth(self.deg,self.mi,self.sec)
        print("__sub__2 initial result : {}".format(result))
        result.sec = result.sec - sec
        result.mi = result.mi - mi
        result.deg = result.deg - deg
        result.check_angle()
        return result
    
    def __truediv__(self,other):
        float(other)
        dd = self.dms2dd()
        dd = dd/other
        return self.dd2dms(dd)

class HA_Circle(object):
    def __init__(self,Dir_deg,Dir_mi,Dir_sec,Back_deg,Back_mi,Back_sec):
        self.Positive = Azimuth(Dir_deg,Dir_mi,Dir_sec)
        self.Back = Azimuth(Back_deg,Back_mi,Back_sec)
        #self.avg = (self.Positive + (self.Back - Azimuth(180,0,0) )) / 2.
        self.avg = self.avg()
        #self.avg = None
    def __str__(self):
        return "HA_Circle object :\n\t\tPositive: {}\n\t\tBack {}\n\t\tAverage : {}".format(str(self.Positive),str(self.Back),str(self.avg))
    def avg(self):
        B = dms2dd(self.Back - Azimuth(180,0,0))
        A = self.Positive.dms2dd()
        Avg = (A+B)/2
        return dd2dms(Avg)
        
class VA_Circle(object):
    def __init__(self,Pos_Deg,Pos_mi,Pos_sec,Back_deg,Back_mi,Back_sec):
        self.Positive = Azimuth(Pos_Deg,Pos_mi,Pos_sec)
        self.Back = Azimuth(Back_deg,Back_mi,Back_sec)
        self.avg = (self.Positive.angle + (Angle(360,0,0)  - self.Back.angle )) / 2.
    def __str__(self):
        return "VA_Circle object :\n\t\tPositive: {}\n\t\tBack {}\n\t\tAverage : {}".format(str(self.Positive),str(self.Back),str(self.avg))
    
class Record(object):
    """
    Input: 
        Station_Name     : 站名
        Circle_ID        : 站點名
        H                : 儀器高(m)
        SD               : 斜距(m)
        HA_Pos_deg=None  : 水平角正鏡 度
        HA_Pos_mi=None   : 水平角正鏡 分
        HA_Pos_sec=None  : 水平角正鏡 秒
        HA_Back_deg=None : 水平角倒鏡 度
        HA_Back_mi=None  : 水平角倒鏡 分
        HA_Back_sec=None : 水平角倒鏡 秒
        VA_Pos_deg=None  : 天頂距正鏡 度
        VA_Pos_mi=None   : 天頂距正鏡 分
        VA_Pos_sec=None  : 天頂距正鏡 秒
        VA_Back_deg=None : 天頂距倒鏡 度
        VA_Back_mi=None  : 天頂距倒鏡 分
        VA_Back_sec=None : 天頂距倒鏡 秒
    Methods:
        set_HA : 設定水平角（正鏡度、分、秒、倒鏡度、分、秒）
        set_HA : 設定天頂距（正鏡度、分、秒、倒鏡度、分、秒）
        set_SD : 設定斜距
        set_H  : 設定儀器高
        calculate_coordinate(ref_HA_object=None) : 計算測點座標（選擇提供參考角度）
    Note:
        Direct position telescope : 正鏡   Back mirror : 倒鏡"""
    def __init__(self,Station_Name,Circle_ID,H,SD,\
                 HA_Pos_deg=None,HA_Pos_mi=None,HA_Pos_sec=None,\
                 HA_Back_deg=None,HA_Back_mi=None,HA_Back_sec=None,\
                 VA_Pos_deg=None,VA_Pos_mi=None,VA_Pos_sec=None,\
                 VA_Back_deg=None,VA_Back_mi=None,VA_Back_sec=None):
        self.Station_Name = Station_Name #測站名
        self.Circle_ID = Circle_ID # 測點
        self.H = H
        self.SD = SD # 斜距
        self.HA,self.VA = None,None
        # Check weather HA is given.
        if ( (HA_Pos_deg != None) and (HA_Pos_mi != None) and (HA_Pos_sec != None) \
            and (HA_Back_deg != None) and (HA_Back_mi != None) and (HA_Back_sec != None)):
            self.HA = HA_Circle(HA_Pos_deg,HA_Pos_mi,HA_Pos_sec,\
                                HA_Back_deg,HA_Back_mi,HA_Back_sec)
        else:
            print("[Warning] The HA is not set !")
            print("HA_Pos_deg = {}, HA_Pos_mi = {}, HA_Pos_sec = {}".format(HA_Pos_deg,HA_Pos_mi,HA_Pos_sec))
            print("HA_Back_deg = {}, HA_Back_mi = {}, HA_Back_sec = {}".format(HA_Back_deg,HA_Back_mi,HA_Back_sec))
        # Check weather VA is given
        if ( (VA_Pos_deg != None) and (VA_Pos_mi != None) and (VA_Pos_sec != None) \
            and (VA_Back_deg != None) and (VA_Back_mi != None) and (VA_Back_sec != None)):
            self.VA = VA_Circle(VA_Pos_deg,VA_Pos_mi,VA_Pos_sec,\
                                VA_Back_deg,VA_Back_mi,VA_Back_sec)
        else:
            print("[Warning] The VA is not set !")
            print("VA_Pos_deg = {}, VA_Pos_mi = {}, VA_Pos_sec = {}".format(VA_Pos_deg,VA_Pos_mi,VA_Pos_sec))
            print("VA_Back_deg = {}, VA_Back_mi = {}, VA_Back_sec = {}".format(VA_Back_deg,VA_Back_mi,VA_Back_sec))
        return
    def __str__(self):
        return "Record :\n\tStation: {}\n\tInstument height : {}\n\tCircle_ID: {}\n\tSD: {}m\n\tHA: {}\n\tVA:{}".format(\
                self.Station_Name,self.H,self.Circle_ID,self.SD,str(self.HA),str(self.VA))
        
    def set_HA(self,HA_Pos_deg,HA_Pos_mi,HA_Pos_sec,\
                 HA_Back_deg,HA_Back_mi,HA_Back_sec):
        self.HA = HA_Circle(HA_Pos_deg,HA_Pos_mi,HA_Pos_sec,\
                            HA_Back_deg,HA_Back_mi,HA_Back_sec)
        return
    def set_VA(self,VA_Pos_deg,VA_Pos_mi,VA_Pos_sec,\
               VA_Back_deg,VA_Back_mi,VA_Back_sec):
        self.VA = VA_Circle(VA_Pos_deg,VA_Pos_mi,VA_Pos_sec,\
                            VA_Back_deg,VA_Back_mi,VA_Back_sec)
        return
    def set_SD(self,SD):
        self.SD=SD
        return
    def set_H(self,H):
        self.H=H
        return
    
    def calculate_coordinate(self,ref_HA_object=None):
        """Calculate the coordinate by given HA,VA,SD
        Input  : ref_HA_object (Optional) - The HA of back_sight
        Output : (X,Y,Z) - The coordinate by given """
        if isinstance(ref_HA_object,HA_Circle):
            HA = self.HA.avg.dd - ref_HA_object.avg.dd
            print("ID : {} Original : {} --> Referenced : {}".format(self.Circle_ID,dd2dms(self.HA.avg.dd),dd2dms(HA)))
        elif isinstance(ref_HA_object,Angle):
            HA =  self.HA.avg.dd - ref_HA_object.dms2ss()
            print("ID : {} Original : {} --> Referenced : {}".format(self.Circle_ID,dd2dms(self.HA.avg.dd),dd2dms(HA)))
        else: # None
            HA = self.HA.avg.dd
        HA = np.radians(HA)
        VA = np.radians(self.VA.avg.dd)
        X = self.SD * np.sin(VA) * np.sin(HA)
        Y = self.SD * np.sin(VA) * np.cos(HA)
        Z = self.SD * np.cos(VA) + self.H
        return (X,Y,Z)
        #Start Calculation
        
    def correctA_HA(self,AngleObj):
        self
    
class Referenced_Record(Record):
    def __init__(self,Station_Name,Circle_ID,H,SD,\
                 HA_Pos_deg=None,HA_Pos_mi=None,HA_Pos_sec=None,\
                 HA_Back_deg=None,HA_Back_mi=None,HA_Back_sec=None,\
                 VA_Pos_deg=None,VA_Pos_mi=None,VA_Pos_sec=None,\
                 VA_Back_deg=None,VA_Back_mi=None,VA_Back_sec=None,HA_Ref=None):
        super().__init__(Station_Name,Circle_ID,H,SD,\
                 HA_Pos_deg,HA_Pos_mi,HA_Pos_sec,\
                 HA_Back_deg,HA_Back_mi,HA_Back_sec,\
                 VA_Pos_deg,VA_Pos_mi,VA_Pos_sec,\
                 VA_Back_deg,VA_Back_mi,VA_Back_sec)
        self.HA_Ref = HA_Ref
        self.HA_Corrected = None
        if not isinstance(self.HA_Ref,Angle):
            print("[Warning] The HA_Ref is not a Angle object. Set to \"None\".")
            self.HA_Ref = None
        else:
            self.HA_Corrected = self.HA.avg.dd - dms2dd(self.HA_Ref)
            
    def calculate_coordinate2(self,ref_HA_Angle_Object=None):
        """Calculate the coordinate by given HA,VA,SD
        Input  : ref_HA_object (Optional) - The HA of back_sight
        Output : (X,Y,Z) - The coordinate by given """
        if isinstance(ref_HA_Angle_Object,Angle):
            HA = self.HA_Corrected - dms2dd(ref_HA_Angle_Object)
            print("ID : {} Original : {} --> Referenced : {}".format(self.Circle_ID,dd2dms(self.HA.avg.dd),dd2dms(HA)))
        else: # None
            HA = self.HA_Corrected
        HA = np.radians(HA)
        VA = np.radians(self.VA.avg.dd)
        X = self.SD * np.sin(VA) * np.sin(HA)
        Y = self.SD * np.sin(VA) * np.cos(HA)
        Z = self.SD * np.cos(VA) + self.H
        return (X,Y,Z) 
    def __str__(self):
        return "Referenced Record :\n\tStation: {}\n\tInstument height : {}\n\tCircle_ID: {}\n\tSD: {}m\n\tHA: {}\n\tVA:{}\n\tCorrected HA : {}".format(\
                self.Station_Name,self.H,self.Circle_ID,self.SD,str(self.HA),str(self.VA),dd2dms(self.HA_Corrected))

    pass
        

def Test():
    print("===== Angle =====")
    A,B,C = Angle(100,15,51),Angle(300,15,55),Angle(-10,10,5)
    print("A=" + str(A), "B= "+str(B),"C= "+str(C))
    print("A+B "+str(A+B)) # 400,31,46
    print("A-B "+str(A-B)) # -200,0,4
    print("A>B "+str(A>B)) # False
    print("A<B "+str(A<B)) # True
    print("A+C "+str(A+C)) # 90,5,46
    print("A-C "+str(A-C)) # 110,25,56
    print("===== Azimuth Object =====")
    A,B,C = Azimuth(100,15,51),Azimuth(300,15,55),Azimuth(-10,10,5)
    print("A=" + str(A), "B= "+str(B),"C= "+str(C))
    print("A+B "+str(A+B)) # 40,31,46
    print("A-B "+str(A-B)) # 159,59,56
    print("A>B "+str(A>B)) # False
    print("A<B "+str(A<B)) # True
    print("A+C "+str(A+C)) # 90,5,46
    print("A-C "+str(A-C)) # 110,25,56
    print("B+C "+str(B+C)) # 290,5,50

def Test2():
    print("===== HA =====")
    A = HA_Circle(331,44,53,151,44,48)
    print("Back : {}".format(str(A.Back))) # 151°44'48.0"
    print(A.Back.mi > Azimuth(180,0,0).mi) # 331,44,48
    print("Back > Azimuth(180) : {}".format(A.Back > Azimuth(180,0,0))) # False
    print("Back - Azimuth(180) : {}".format(str(A.Back - Azimuth(180,0,0)))) # 331.0°44.0'48.0"
    print("dms2dd(self.Back - Azimuth(180,0,0)) : {}".format(str(dms2dd(A.Back - Azimuth(180,0,0))))) # 331.74666666666667
    print("A.Positive.dms2dd() : {}".format(str(A.Positive.dms2dd()))) # 331.7480555555556
    #print(A.avg)
    #print(A.avg.dms2dd())
    print(A) # Pos: 331°44'53.0" Back: 151°44'48.0" Avg : 331°44'50.5"
    
    print("===== VA ======")
    B = VA_Circle(91,31,29,268,28,51)
    print(B)
    print("360 - Back : {}".format(str(Angle(360,0,0) - B.Back.angle))) # 91°31'9.0"
    print("Postive.angle : {}".format(str(B.Positive.angle))) # 91°31'29.0"
    print("Positive + (360 - Back ) : {}".format(str(B.Positive.angle + (Angle(360,0,0) - B.Back.angle) ))) # 183°2'38.0"
    print("(Positive + (360 - Back ))/2 : {}".format(str((B.Positive.angle + (Angle(360,0,0) - B.Back.angle))/2 ))) # 91°31'19.0"
def Test3():
    R = Record("Front","A",1.5385,4.2524,331,44,53,151,44,48,91,24,56,268,35,26)
    print(R)
    print(R.calculate_coordinate())
if __name__ == "__main__":
    print("Test1\n")
    Test()
    print("\n\nTest2\n")
    Test2()
    print("\n\nTest3\n")
    Test3()

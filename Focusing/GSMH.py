from PIL import Image as p
import numpy as np
import math

#define
sizepic = [0,0]
timer = [0,0,0,0]
PI = 3.1415926

def getrgb(path):#得到图像中各个点像素的RGB三通道值
    pd = p.open(path)
    sizepic[0] = pd.size[0]
    sizepic[1] = pd.size[1]
    nr = np.empty((sizepic[0],sizepic[1]))
    ng = np.empty((sizepic[0],sizepic[1]))
    nb = np.empty((sizepic[0],sizepic[1]))
    for i in range(0,sizepic[0]):
        for j in range(0,sizepic[1]):
            nr[i][j] = pd.getpixel((i,j))[0]
            ng[i][j] = pd.getpixel((i,j))[1]
            nb[i][j] = pd.getpixel((i,j))[2]
    return nr,ng,nb
    
def Matrixmaker(r):#通过半径和坐标计算高斯函数矩阵
    summat = 0
    ma = np.empty((2*r+1,2*r+1))
    for i in range(0,2*r+1):
        for j in range(0,2*r+1):
            gaussp = (1/(2*PI*(r**2))) * math.e**(-((i-r)**2+(j-r)**2)/(2*(r**2))) 
            ma[i][j] = gaussp
            summat += gaussp
    print(ma)
    print(summat)
    for i in range(0,2*r+1):
        for j in range(0,2*r+1):
            ma[i][j] = ma[i][j]/summat
    print("矩阵如下:")
    return ma
          
def newrgb(ma,nr,ng,nb,r):#生成新的像素rgb矩阵
    newr = np.empty((sizepic[0],sizepic[1]))
    newg = np.empty((sizepic[0],sizepic[1]))
    newb = np.empty((sizepic[0],sizepic[1]))
    for i in range(r+1,sizepic[0]-r):
        for j in range(r+1,sizepic[1]-r):
            o = 0 
            for x in range(i-r,i+r+1):
                p = 0
                for y in range(j-r,j+r+1):
                    #print("x{},y{},o{},p{}".format(x,y,o,p))
                    newr[i][j] += nr[x][y]*ma[o][p]
                    newg[i][j] += ng[x][y]*ma[o][p]
                    newb[i][j] += nb[x][y]*ma[o][p]
                    p += 1
                o += 1            
    return newr,newg,newb

def cpic(r,g,b,path,rd):
    pd = p.open(path)
    for i in range(rd+1,sizepic[0]-rd+1):
        for j in range(rd+1,sizepic[1]-rd+1):
            pd.putpixel((i,j),(int(r[i][j]),int(g[i][j]),int(b[i][j])))
    print("正在导出图片..")
    pd.save("blurred.jpg")
    
def main():
    rd = eval(input("请输入模糊的半径："))
    path = input("请输入图片的地址(包括后缀):")
    nr,ng,nb = getrgb(path)
    matx = Matrixmaker(rd)
    print(matx)
    print("正在转换..")
    newr,newg,newb = newrgb(matx,nr,ng,nb,rd)
    print("正在准备输出..")
    cpic(newr,newg,newb,path,rd)
    print("{} - >> {}".format(path.split('/')[-1],"blurred.png"))
main()
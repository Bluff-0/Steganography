#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
from tqdm import tqdm
import numpy as np


# In[2]:


class Encode:
    
    # Decimal to 8-bit Binary conversion
    def dectobin(num):
        temp= bin(num).replace('0b','')
        while len(temp)<8:
            temp= '0' + temp
        return temp
    
    # Transformation of a complete image to binary
    def bincodedimage(image):
        t= [[ ['#' for col in range(image.shape[2])] for col in range(image.shape[1])] for row in range(image.shape[0])]
        i= 0
        for _ in tqdm(range(image.shape[0])):
            if i >= image.shape[0]:
                break
            for j in range(image.shape[1]):
                t[i][j][0]= (Encode.dectobin(image[i][j][0]))
                t[i][j][1]= (Encode.dectobin(image[i][j][1]))
                t[i][j][2]= (Encode.dectobin(image[i][j][2]))
            i+=1
        return t
    
    #Encoding an image to another one
    def encodeimage(binoriginal, binhide):
        i= 0
        for _ in tqdm(range(len(binhide))):
            if i >= len(binhide):
                break
            for j in range(len(binhide[0])):
                binoriginal[i][j][0]= binoriginal[i][j][0][:4] + binhide[i][j][0][::-1][4:]
                binoriginal[i][j][1]= binoriginal[i][j][1][:4] + binhide[i][j][1][::-1][4:]
                binoriginal[i][j][2]= binoriginal[i][j][2][:4] + binhide[i][j][2][::-1][4:]
            i+=1
        return binoriginal
    
    # Converting Binary Coded Image to Decimal Coded Image
    def backtodecimal(image):
        t= [[ [0 for col in range(3)] for col in range(len(image[0]))] for row in range(len(image))]
        i= 0
        for _ in tqdm(range(len(image))):
            if i >= len(image):
                break
            for j in range(len(image[0])):
                t[i][j][0]= int(image[i][j][0], 2)
                t[i][j][1]= int(image[i][j][1], 2)
                t[i][j][2]= int(image[i][j][2], 2)
            i+=1
        return t

    
def flowcontrolEncoder(m,n):
    mainImage= cv2.imread(m)
    print(m)
    binarymainImage= Encode.bincodedimage(mainImage)
    hiddenImage= cv2.imread(n)
    binaryhiddenImage= Encode.bincodedimage(hiddenImage)
    binaryencodedImage= Encode.encodeimage(binarymainImage, binaryhiddenImage)
    mergedImage= Encode.backtodecimal(binaryencodedImage)
    cv2.imwrite("/".join(m.split('/')[:-1])+'/mod.png', np.uint8(mergedImage))
    messagebox.showinfo( "Completed", "Mod.png is saved in the Desktop")


# In[3]:


class Decode:

    def dectobin(num):
        temp= bin(num).replace('0b','')
        while len(temp)<8:
            temp= '0' + temp
        return temp
    
    def bincodedimage(image):
        t= [[ ['#' for col in range(image.shape[2])] for col in range(image.shape[1])] for row in range(image.shape[0])]
        i= 0
        for _ in tqdm(range(image.shape[0])):
            if i >= image.shape[0]:
                break
            for j in range(image.shape[1]):
                t[i][j][0]= (Decode.dectobin(image[i][j][0]))
                t[i][j][1]= (Decode.dectobin(image[i][j][1]))
                t[i][j][2]= (Decode.dectobin(image[i][j][2]))
            i+=1
        return t
    
    def decodeimage(image):
        i= 0
        for _ in tqdm(range(len(image))):
            if i >= len(image):
                break
            for j in range(len(image[0])):
                image[i][j][0]= image[i][j][0][4:][::-1] + '0000'
                image[i][j][1]= image[i][j][1][4:][::-1] + '0000'
                image[i][j][2]= image[i][j][2][4:][::-1] + '0000'
            i+=1
        return image

    def backtodecimal(image):
        t= [[ [0 for col in range(3)] for col in range(len(image[0]))] for row in range(len(image))]
        i= 0
        for _ in tqdm(range(len(image))):
            if i >= len(image):
                break
            for j in range(len(image[0])):
                t[i][j][0]= int(image[i][j][0], 2)
                t[i][j][1]= int(image[i][j][1], 2)
                t[i][j][2]= int(image[i][j][2], 2)
            i+=1
        return t
    
    
def flowcontrolDecoder(m='C:\\Users\\KIIT\\Desktop\\mod.png'):
    secretImage= cv2.imread(m)
    binImage= Decode.bincodedimage(secretImage)
    decodedImage= Decode.decodeimage(binImage)
    hiddenImage= Decode.backtodecimal(decodedImage)
    cv2.imwrite("/".join(m.split('/')[:-1])+'/secret.png', np.uint8(hiddenImage))
    messagebox.showinfo( "Completed", "Secret.png is saved in the Desktop")


# In[4]:


from tkinter import *
from tkinter.filedialog import  *
from PIL import Image,ImageTk
from tkinter import messagebox
import matplotlib.pyplot as plt


# In[7]:


def encode():
    a.destroy()
    enc=Tk()
    enc.title("encode")
    enc.geometry("500x400+300+150")

    label1=Label(text="Secret Image").place(relx=0.1,rely=0.1,height=20,width=100)

    def op1():
        global fileopen
        fileopen=StringVar()
        fileopen=askopenfile(initialdir="/Destop",title="select file",filetypes=(("png files","png"),("all files",".*")))
        if fileopen is not None:
            Label(text="File is Set, You are ready to go").place(relx=0.5, rely=0.3, height=20, width=100) 



    buttonselect1 = Button(text="Select Image File", command=op1).place(relx=0.4, rely=0.1)
    label2 = Label(text="Cover Image").place(relx=0.1, rely=0.5, height=20, width=100)

    def op2():
        global fileopen1
        fileopen1 = StringVar()
        fileopen1 = askopenfile(initialdir="/Destop", title="select file",
                               filetypes=(("png files", "png"), ("all files", ".*")))
        if fileopen1 is not None:
            Label(text="File is Set, You are ready to go").place(relx=0.5, rely=0.6, height=20, width=100)
    buttonselect2 = Button(text="Select Image File",command=op2).place(relx=0.4, rely=0.5)

    buttonencode=Button(text="Encode", command= lambda: flowcontrolEncoder(fileopen.name,fileopen1.name)).place(relx=0.5, rely=0.8)
    
def decode():
    a.destroy()
    dec = Tk()
    dec.title("decode")
    dec.geometry("500x400+300+150")

    def openfile():
        global fileopen
        fileopen = StringVar()
        fileopen = askopenfile(initialdir="/Destop", title="select file",filetypes=(("png files", "png"), ("all files", ".*")))
        if fileopen is not None:
            Label(text="File is Set, You are ready to go").place(relx=0.5, rely=0.5, height=20, width=100)
    buttonselect2 = Button(text="select file",command=openfile).place(relx=0.5, rely=0.3)
    buttonencode=Button(text="Decode", command= lambda: flowcontrolDecoder(fileopen.name)).place(relx=0.5, rely=0.7)


# In[10]:


a = Tk()
a.title("IMAGE STEGANOGRAPHY")
a.geometry("500x400+300+150")
encodebutton=Button(a,text="Encode",command=encode).place(relx=0.3,rely=0.3,height=40,width=80)
decodebutton=Button(a,text="Decode",command=decode).place(relx=0.5,rely=0.3,height=40,width=80)
a.mainloop()


# In[ ]:





# In[ ]:





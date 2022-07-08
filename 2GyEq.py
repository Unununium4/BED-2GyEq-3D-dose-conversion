# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 10:02:45 2021

@author: anmorrow
"""

import easygui
import sys
import os
import pydicom
import numpy as np

import random
import subprocess

try:
    f = easygui.fileopenbox("Please select the dicom dose file")
except:
    easygui.msgbox("Please enter a valid file")
    sys.exit()

nfxtxt= easygui.enterbox("How many fractions?")
try:
    nfx=float(nfxtxt)
    if(float(nfx) < 0 ):
        raise Exception('')
except:
    easygui.msgbox("Please enter a floating point number greater than 0")
    sys.exit()

ABtxt = easygui.enterbox("What a/b to use?")
try:
    AB = float(ABtxt)
    if(float(AB) < 0 ):
        raise Exception('')
except:
    easygui.msgbox("Please enter a floating point number greater than 0")
    sys.exit()

newfn = os.path.splitext(os.path.basename(f))[0]

dosefile = pydicom.dcmread(f)
dosearray=dosefile.pixel_array

scaling = dosefile.DoseGridScaling

rows = len(dosefile.pixel_array)
columns = len(dosefile.pixel_array[0])
slices = len(dosefile.pixel_array[0,0])


newf = os.path.dirname(f) + "\\" + newfn + "2GyEq.dcm"

newarray = np.empty((rows,columns,slices ), dtype = np.uint32)

for i in range(rows):
    for j in range(columns):
        for k in range (slices):
            newarray[i,j,k] =  dosearray[i,j,k] * ((scaling*dosearray[i,j,k]/nfx + AB)/(2+AB))

dosefile.PixelData = newarray.tobytes()

dosefile.SeriesInstanceID = str(random.randint(0,1000000000000000000000000000000))
dosefile[0x20,0xe].value = str(random.randint(0,1000000000000000000000000000000))
dosefile.ReferencedRTPlanSequence[0].ReferencedSOPInstanceUID = str(random.randint(0,1000000000000000000000000000000))
dosefile.StudyInstanceUID = str(random.randint(0,1000000000000000000000000000000))
dosefile.SOPInstanceUID = str(random.randint(0,1000000000000000000000000000000))

dosefile.SeriesDescription =os.path.splitext(os.path.basename(newf))[0]
dosefile.save_as(newf)

'''repeat for BED.  i have lazily just copied most of the code over.
'''

dosefile = pydicom.dcmread(f)
dosearray=dosefile.pixel_array

scaling = dosefile.DoseGridScaling

rows = len(dosefile.pixel_array)
columns = len(dosefile.pixel_array[0])
slices = len(dosefile.pixel_array[0,0])


newf = os.path.dirname(f) + "\\" + newfn + "BED.dcm"

newarray = np.empty((rows,columns,slices ), dtype = np.uint32)

for i in range(rows):
    for j in range(columns):
        for k in range (slices):
            newarray[i,j,k] =  dosearray[i,j,k] * (1+ (scaling*dosearray[i,j,k]/nfx)/AB )

dosefile.PixelData = newarray.tobytes()

dosefile.SeriesInstanceID = str(random.randint(0,1000000000000000000000000000000))
dosefile[0x20,0xe].value = str(random.randint(0,1000000000000000000000000000000))
dosefile.ReferencedRTPlanSequence[0].ReferencedSOPInstanceUID = str(random.randint(0,1000000000000000000000000000000))
dosefile.StudyInstanceUID = str(random.randint(0,1000000000000000000000000000000))
dosefile.SOPInstanceUID = str(random.randint(0,1000000000000000000000000000000))

dosefile.SeriesDescription =os.path.splitext(os.path.basename(newf))[0]
dosefile.save_as(newf)

easygui.msgbox('Done!')
subprocess.Popen('explorer ' + os.path.dirname(newf))


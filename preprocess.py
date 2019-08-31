import os
import numpy as np
import math
import random
import cv2 as cv
import nibabel as nib
import matplotlib.pyplot as plt

def read_data(path):
	return nib.load(path)

def to_uint8(img):
    vol=vol.astype(np.float)
    vol[vol<0]=0
    return ((vol-vol.min())*255.0/vol.max()).astype(np.uint8)

def histeq(img):
    for slice_index in range(vol.shape[2]):
        vol[:,:,slice_index]=cv.equalizeHist(vol[:,:,slice_index])
    return vol


if __name__=='__main__':
	for f in os.walk(path):
		for file in f:
    		file_path=file
    		img=to_uint8(readVol(file))
    		histeqed=histeq(img)
    	for slice_index in range(histeqed.shape[2]):
    		plt.imsave(file+'_pre.jpg',histeqed[:,;,slice_index])

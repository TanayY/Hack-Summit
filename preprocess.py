import os
import numpy as np
import math
import random
import cv2 as cv
import nibabel as nib
import matplotlib.pyplot as plt

def read_data(path):
  d = nib.load(path)
  return (d.get_data())

def to_uint8(vol):
    vol=vol.astype(np.float)
    vol[vol<0]=0
    return ((vol-vol.min())*255.0/vol.max()).astype(np.uint8)

def histeq(vol):
    for slice_index in range(vol.shape[2]):
        vol[:,:,slice_index]=cv.equalizeHist(vol[:,:,slice_index])
    return vol

def rotate(stack_list,angle,interp):
    for stack_list_index,stacked in enumerate(stack_list):
        raws,cols=stacked.shape[0:2]
        M=cv.getRotationMatrix2D(((cols-1)/2.0,(raws-1)/2.0),angle,1)
        stack_list[stack_list_index]=cv.warpAffine(stacked,M,(cols,raws),flags=interp)
    return stack_list

# in: T1 volume, foreground threshold, margin pixel numbers
# out: which region should be cropped
def calc_crop_region(stack_list_T1,thre,pix):
    crop_region=[]
    for stack_list_index,stacked in enumerate(stack_list_T1):
        _,threimg=cv.threshold(stacked[:,:,int(stacked.shape[2]/2)].copy(),thre,255,cv.THRESH_TOZERO)
        pix_index=np.where(threimg>0)
        if not pix_index[0].size==0:
            y_min,y_max=min(pix_index[0]),max(pix_index[0])
            x_min,x_max=min(pix_index[1]),max(pix_index[1])
        else:
            y_min,y_max=pix,pix
            x_min,x_max=pix,pix
        y_min=(y_min<=pix)and(0)or(y_min)
        y_max=(y_max>=stacked.shape[0]-1-pix)and(stacked.shape[0]-1)or(y_max)
        x_min=(x_min<=pix)and(0)or(x_min)
        x_max=(x_max>=stacked.shape[1]-1-pix)and(stacked.shape[1]-1)or(x_max)
        crop_region.append([y_min,y_max,x_min,x_max])
    return crop_region

# in: crop region for each slice, how many slices in a stack
# out: max region in a stacked img
def calc_max_region_list(region_list,stack_num):
    max_region_list=[]
    for region_list_index in range(len(region_list)):
        y_min_list,y_max_list,x_min_list,x_max_list=[],[],[],[]
        for stack_index in range(stack_num):
            query_list=get_stackindex(region_list_index,stack_num,len(region_list))
            region=region_list[query_list[stack_index]]
            y_min_list.append(region[0])
            y_max_list.append(region[1])
            x_min_list.append(region[2])
            x_max_list.append(region[3])
        max_region_list.append([min(y_min_list),max(y_max_list),min(x_min_list),max(x_max_list)])
    return max_region_list

# in: size, devider
# out: padded size which can be devide by devider
def calc_ceil_pad(x,devider):
    return math.ceil(x/float(devider))*devider

# in: stack img list, maxed region list
# out: cropped img list
def crop(stack_list,region_list):
    cropped_list=[]
    for stack_list_index,stacked in enumerate(stack_list):
        y_min,y_max,x_min,x_max=region_list[stack_list_index]
        cropped=np.zeros((calc_ceil_pad(y_max-y_min,16),calc_ceil_pad(x_max-x_min,16),stacked.shape[2]),np.uint8)
        cropped[0:y_max-y_min,0:x_max-x_min,:]=stacked[y_min:y_max,x_min:x_max,:]
        cropped_list.append(cropped.copy())
    return cropped_list

cropped=[]
if __name__=='__main__':
  for i in range(len(allimg_list)):
    file = allimg_list[i]
    print(file)
    img=to_uint8(read_data(file))
    histeqed=(histeq(img))
    rotated=rotate(stack_list,angle)
    region=calc_crop_region(rotated,50,5)
    max_region=calc_max_region_list(region,5)
    cropped.append(crop(rotated,max_region))


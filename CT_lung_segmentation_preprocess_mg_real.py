# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 18:16:30 2019

@author: mit
"""

#CT-lung_segmentation_preprocess

import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from skimage.io import imread
from skimage.transform import pyramid_reduce, resize

import os, glob

img_list = sorted(glob.glob('D:/need to debugging/Ct_lung_dataset/finding-lungs-in-ct-data/2d_images/*.tif'))
mask_list = sorted(glob.glob('D:/need to debugging/Ct_lung_dataset/finding-lungs-in-ct-data/2d_masks/*.tif'))

print(len(img_list), len(mask_list))

IMG_SIZE = 256

x_data, y_data = np.empty((2, len(img_list), IMG_SIZE, IMG_SIZE, 1), dtype=np.float32)

for i, img_path in enumerate(img_list):
    img = imread(img_path)
    img = resize(img, output_shape=(IMG_SIZE, IMG_SIZE, 1), preserve_range=True)
    x_data[i] = img
    
for i, img_path in enumerate(mask_list):
    img = imread(img_path)
    img = resize(img, output_shape=(IMG_SIZE, IMG_SIZE, 1), preserve_range=True)
    y_data[i] = img
    
y_data /= 255.

fig, ax = plt.subplots(1, 2)
ax[0].imshow(x_data[12].squeeze(), cmap='gray')
ax[1].imshow(y_data[12].squeeze(), cmap='gray')

x_train, x_val, y_train, y_val = train_test_split(x_data, y_data, test_size=0.1)

base_path = 'D:/need to debugging/Ct_lung_dataset/finding-lungs-in-ct-data/'

if not(os.path.exists(base_path + 'dataset')):
    os.mkdir(base_path + 'dataset')
    
np.save(base_path + 'dataset/x_train.npy', x_train)
np.save(base_path +'dataset/y_train.npy', y_train)
np.save(base_path +'dataset/x_val.npy', x_val)
np.save(base_path +'dataset/y_val.npy', y_val)

print(x_train.shape, y_train.shape)
print(x_val.shape, y_val.shape)

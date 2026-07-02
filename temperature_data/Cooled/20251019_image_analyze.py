import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image #python image library for exif data
from PIL.ExifTags import TAGS # for Exif tags

#import pytesseract # for OCR of min/max

import glob
#import os

# Get a list of all files ending with .jpg (case-insensitive) in the current directory
jpg_files = glob.glob("*.jpg") + glob.glob("*.JPG")

cold_temps = np.array([])
mid_temps = np.array([])
hot_temps = np.array([])
hotspot_temps = np.array([])
times = np.array([])
# Iterate through the list of JPG files
for file_name in jpg_files:
    print(f"Processing file: {file_name}")

    exif = Image.open(file_name)._getexif()
    for tag_id, value in exif.items():
        tag_name = TAGS.get(tag_id, tag_id)
        if tag_name == 'DateTimeOriginal':
            time = value
    #print(time)
    #print(time[11:13])
    times = np.append(times,3600*int(time[11:13])+60*int(time[14:16])+int(time[17:19]))


    # read image

    im = cv2.imread(file_name,cv2.IMREAD_GRAYSCALE)
    # calculate mean value from RGB channels and flatten to 1D array
    #print(im)
    #print(im[44:560,160:270])
    #print(np.mean(im[160:270,44:560],axis=0))

    #cv2.imshow("Image", im)
    xmin = 15
    xmax = 270
    ymin = 112
    ymax = 122

    xcalmin = 460
    xcalmax = 530
    ycalmin = 395
    ycalmax = 460

    # location of upper end of image scale
    xhotmin = 279
    xhotmax = 316
    yhotmin = 5
    yhotmax = 25

    # location of lower end of image scale
    xcoldmin = 278
    xcoldmax = 316
    ycoldmin = 216
    ycoldmax = 237
    #cv2.imshow("Image", im[ymin:ymax,xmin:xmax])
    #cv2.imshow("Image", im[yhotmin:yhotmax,xhotmin:xhotmax])
    #cv2.imshow("Image", im[ycoldmin:ycoldmax,xcoldmin:xcoldmax])
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #break
    #vals = im.mean(axis=2).flatten()
    # calculate histogram
    #counts, bins = np.histogram(vals, range(257))
    # plot histogram centered on values 0..255
    avg_pixel=np.mean(im[ymin:ymax,xmin:xmax],axis=0)
    #calibration = np.mean(im[ycalmin:ycalmax,xcalmin:xcalmax])
    config = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.'


    #try:
    #    maxtemp =float(pytesseract.image_to_string(im[yhotmin:yhotmax,xhotmin:xhotmax],config=config))
    #except:
    #    cv2.imshow("Image", im[yhotmin:yhotmax,xhotmin:xhotmax])
    #    cv2.waitKey(0)
    #    cv2.destroyAllWindows()
    #    maxtemp = float(input("enter Hot temp: "))
    #print(maxtemp)

    #mintemp =float(pytesseract.image_to_string(im[ycoldmin:ycoldmax,xcoldmin:xcoldmax],config=config))
    #print(mintemp)
    #print(np.max(avg_pixel))
    #print(np.min(avg_pixel))
    avg_temp = 21.0+(102.0-21.0)/255*(avg_pixel)
    avg_size = 3
    cold_spot = 19
    mid_spot = 150
    hotspot_spot = 220
    hot_spot = 254

    cold_temps = np.append(cold_temps,np.mean(avg_temp[(cold_spot-avg_size):(cold_spot+avg_size)]))
    mid_temps = np.append(mid_temps,np.mean(avg_temp[(mid_spot-avg_size):(mid_spot+avg_size)]))
    hotspot_temps = np.append(hotspot_temps,np.mean(avg_temp[(hotspot_spot-avg_size):(hotspot_spot+avg_size)]))#avg_temp[409]
    hot_temps = np.append(hot_temps,np.mean(avg_temp[(hot_spot-avg_size):(hot_spot+avg_size)]))#avg_temp[494]
    #print(file_name[11:13])
    #print(file_name[14:16])
    #print(file_name[17:19])

    #times = np.append(times,3600*int(file_name[11:13])+60*int(file_name[14:16])+int(file_name[17:19]))
    #np.append(times,avg_temp[270])
    
    plt.plot(avg_temp)
    #plt.title
    #plt.bar(bins[:-1] - 0.5, counts, width=1, edgecolor='none')
    #plt.xlim([-0.5, 255.5])
plt.show()
print(times)
tvals = times- np.min(times,axis=0)

indexes = tvals.argsort()

#return s[indexes], p[indexes]

#print(abstimes)
plt.plot(tvals[indexes],cold_temps[indexes],'.b')

plt.plot(tvals[indexes],mid_temps[indexes],'.g')
plt.plot(tvals[indexes],hot_temps[indexes],'.r')
plt.plot(tvals[indexes],hotspot_temps[indexes],'.k')
plt.show()
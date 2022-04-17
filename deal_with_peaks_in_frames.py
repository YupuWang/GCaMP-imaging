import os
import sys
import pickle
import numpy
from class_pre_treatment import pre_treatment
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift
import matplotlib.pyplot as plt

working_path="C:/Users/Yupu Wang/Google Drive/GCaMP data/20201211 GCaMP/20201211-016"
in_movie_folder=working_path+"/"+"movie"

if not os.path.exists(in_movie_folder):  # if input folder not exist, stop the following step
    print("Input fast5 folder not found.")
    exit(10)

for item in os.listdir(in_movie_folder):
    file_name=in_movie_folder+"/"+item
    if os.path.isfile(file_name) and item.split("_")[-1]=="PreSelect.pkl":  # open the input file with the position of peaks
        print(file_name)
        with open(file_name,"rb") as f:
            movie=pickle.load(f)  # input the movie object with position of peaks
            switch=0 # it becomes 1 when a peak starts to show  # the several lines below are tricky, they are supposed to find out the real number of shinings shown in the movie, remember, one position may shine more than one time
            num_peak=0 # record the number of shinings found
            accu=0  # sometimes the peaks of a shining may not be continueous
            temp=[] # store all pixels in a frame that have peaks, only store all positions of one shining
            all_peaks=[]
            frame_num=[]
            for i in range(len(movie.peak_in_frame)): # go through each frame in time order
                if len(movie.peak_in_frame[i])>=2 and switch==1: # there are more than 5 pixels in this frame that has a peak and the former one frame also has more than 5 pixels with peaks, this is the maintance of shining
                    temp.extend(movie.peak_in_frame[i]) # add more spots to this shining which already starts
                if len(movie.peak_in_frame[i])>=2 and switch==0: # there are more than 5 pixels in this frame that has a peak and the former one frame doesn't more than 5 pixels with peaks, this is the start of shining
                    frame_num.append(i) # add the starting frame of a release to this list
                    switch=1  # this is a new start of shining
                    num_peak+=1  # one more shining found
                    temp.extend(movie.peak_in_frame[i]) # add spots to the shining
                elif len(movie.peak_in_frame[i])<2 and switch==1 and accu<3: # doesn't have enough peaks of pixels, but I can still toletare, maybe the shining hasn't ended and will have enough peaks in the next frame
                    accu+=1
                elif len(movie.peak_in_frame[i])<2 and switch==1 and accu>=3: # doesn't have enough peaks of pixels, and it hasn't been shining for 3 frames and I think the shining comes to an end
                    switch=0 # the shining ends, turn off.
                    accu=0
                    all_peaks.append(temp) # store all the pixles of peaks to another list
                    temp=[] # remove all pixels in this shining as it ends.
            # for i in range(len(all_peaks)):
            #     print(all_peaks[i])
            print("number of release events detected:",num_peak)
            plt.figure(figsize=(4.85,10))
            center_of_gravity=numpy.zeros(shape=(0,2))
            for i in range(len(all_peaks)):  #calculate the center of each shining
                x=[]
                y=[]
                print ('release event:', i+1, 'frame:', frame_num[i])
                for j in range(len(all_peaks[i])):
                    x.append(all_peaks[i][j][0])
                    #print (x)
                    y.append(all_peaks[i][j][1])
                    #print (y)
                x_var=numpy.var(x)
                y_var=numpy.var(y)
                if x_var>10 or y_var>10:  # if the spots are too distant to each other, it means there may be more than one regions shining at the same time
                    x_temp = []
                    y_temp = [] 
                    if x_var>10:
                        while x_var>10:
                            x_max_position = x.index(max(x))
                            x_temp.append(x[x_max_position])
                            y_temp.append(y[x_max_position])
                            del x[x_max_position]
                            x_var=numpy.var(x)
                            del y[x_max_position]
                            y_var=numpy.var(y)
                    if x_var<10 and y_var>10:
                        while y_var>10:
                            y_max_position = y.index(max(y))
                            x_temp.append(x[y_max_position])
                            y_temp.append(y[y_max_position])
                            del x[y_max_position]
                            x_var=numpy.var(x)
                            del y[y_max_position]
                            y_var=numpy.var(y)
                    x_mean=numpy.mean(x)
                    y_mean=numpy.mean(y)
                    center_of_gravity=numpy.append(center_of_gravity,[x_mean,y_mean]) #calculate the center of each shining
                    plt.scatter(y_mean,200-x_mean,color="blue",alpha=0.5)
                    #plt.annotate(len(x),(y_mean,200-x_mean))
                    plt.annotate(i+1,(y_mean,200-x_mean)) # annotate the number of release events detected in this file
                    x_mean=numpy.mean(x_temp)
                    y_mean=numpy.mean(y_temp)    
                    center_of_gravity=numpy.append(center_of_gravity,[x_mean,y_mean]) #calculate the center of each shining
                    plt.scatter(y_mean,200-x_mean,color="blue",alpha=0.5)
                    #plt.annotate(len(x),(y_mean,200-x_mean))
                    plt.annotate(i+1,(y_mean,200-x_mean))
                else:
                    x_mean=numpy.mean(x)
                    y_mean=numpy.mean(y)
                    #print([x_mean,y_mean])
                    center_of_gravity=numpy.append(center_of_gravity,[x_mean,y_mean]) #calculate the center of each shining
                    plt.scatter(y_mean,200-x_mean,color="blue",alpha=0.5)
                    #plt.annotate(len(x),(y_mean,200-x_mean))
                    plt.annotate(i+1,(y_mean,200-x_mean))
            #plt.axis('off')
            plt.xlim([0,100])
            plt.ylim([0,200])
            plt.show()

            center_of_gravity=center_of_gravity.reshape(int(len(center_of_gravity)/2),2) # make the coordinate of shining more readable.
            #print(center_of_gravity)
            
            plt.figure(figsize=(4.85,10))
            ###### ## clustering without defined classes (mean-shift) # you don't need to know the positions that could shine in advance.
            labels = MeanShift(bandwidth=1.5).fit(center_of_gravity).labels_  # it cluster the neighboting shining centers according to the redius you tell it # this parameter is which position each shining belongs to
            centers = MeanShift(bandwidth=1.5).fit(center_of_gravity).cluster_centers_ # this parameter is the coordinate of each position that could shine
            #print(labels)
            print("AZ number:",len(centers))
            #plt.axis('off')
            plt.xlim([0,100])
            plt.ylim([0,200])
            colors=["red","orange","yellow","green","blue","purple","black","grey","brown","pink"]
            #for i in range(len(center_of_gravity)):
                #plt.scatter(centers[i][1],200-centers[i][0],color=colors[labels[i]],alpha=0.5)

            for i in range(len(centers)):
               plt.scatter(centers[i][1],200-centers[i][0],color="red",alpha=0.5)
            
            plt.show()



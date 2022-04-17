import os
import sys
from nd2reader import ND2Reader
import pickle
from class_pre_treatment import pre_treatment

working_path="C:/Users/Yupu Wang/Google Drive/GCaMP data/20201220-032"
in_movie_folder=working_path+"/"+"movie"

if not os.path.exists(in_movie_folder):  # if input folder not exist, stop the following step
    print("Input fast5 folder not found.")
    exit(10)

for item in os.listdir(in_movie_folder):
    file_name=in_movie_folder+"/"+item
    if os.path.isfile(file_name) and item.split(".")[-1]=="nd2": # don't have any other "." in the file name
        out_file=in_movie_folder+"/"+item.split(".")[0]+"_NMJ_PreSelect.pkl" # name the output file
        in_mask_file=in_movie_folder+"/"+item.split(".")[0]+"_NMJ_PreSelect_mask.pkl"   # find the mask file according to the name of nd2 file
        with open(out_file,"wb+") as output:
            print(file_name)
            with open(in_mask_file,"rb") as f:
                with ND2Reader(file_name) as this_file: # this_file contains every frame (754), each frame is 50*120 (it has more rows than columns)
                    movie=pickle.load(f)  # input the "movie" object with mask info
                    #movie.show_cruves_and_threshold(this_file) # use this function to draw figures, not for storing info
                    movie.show_peak_positions_and_store(this_file) # use this function to draw figures, and prepare data for storage
                    output.write(pickle.dumps(movie))  # when you want to store the parameters get from above, do this. when you only want to draw figures , don't do this
                    print("done")
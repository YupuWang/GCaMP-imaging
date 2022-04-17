import os
import sys
import pickle
from class_pre_treatment import pre_treatment

working_path="C:/Users/Yupu Wang/Google Drive/GCaMP data/20201220-032"
in_movie_folder=working_path+"/"+"movie"

if not os.path.exists(in_movie_folder):  # if input folder not exist, stop the following step
    print("Input folder not found.")
    exit(10)

for item in os.listdir(in_movie_folder):
    file_name=in_movie_folder+"/"+item
    if os.path.isfile(file_name) and item.split("_")[-1]=="ROI.jpg": # don't have any other "." in the file name
        print(file_name)
        movie=pre_treatment()  # make "movie" as a "pre_treatment" object
        movie.get_mask(file_name)   # run this function, see class_pre_treatment
        out_file=in_movie_folder+"/"+item.split("_")[0]+"_NMJ_PreSelect_mask.pkl"  # name the output file which store the "movie" object
        with open(out_file,"wb+") as output:
            output.write(pickle.dumps(movie))   # write info in the output file
        print("done")
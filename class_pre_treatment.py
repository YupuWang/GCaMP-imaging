class pre_treatment:
    def __init__(self):
        pass

    def show_cruves_and_threshold(self,this_file):
        import numpy
        import matplotlib.pyplot as plt
        self.n_frames=len(this_file)  #  number of frames in this movie
        for row_num in range(90,91,3):#120
            for col_num in range(24,25,3):#50
                if self.mask[row_num][col_num]==1: # only do the region of interest
                    x=[]
                    x_baseline=[]
                    for num_frame in range(len(this_file)):
                        print(this_file[num_frame][row_num][col_num])
                        add_sum=0
                        for i in range(row_num-1,row_num+2):
                            for j in range(col_num-1,col_num+2):
                                add_sum+=this_file[num_frame][i][j]
                        x.append(add_sum)
                    x_baseline=self.median_smooth(self.median_smooth(x,50),50)
                    smooth_x=self.smooth(self.smooth(x,15),15)  # smooth window size
                    smooth_x=[smooth_x[i]-x_baseline[i] for i in range(len(smooth_x))] # extract the baseline
                    threshold=400
        plt.plot(x,alpha=0.5) 
        plt.plot(x_baseline,alpha=1,color="red")
        plt.show()
        plt.plot(smooth_x,color="brown")
        plt.plot([0,754],[0,0],alpha=0.4)
        plt.plot([0,754],[threshold,threshold],alpha=0.8)
        plt.show()

    def show_peak_positions_and_store(self,this_file):
        import numpy
        import matplotlib.pyplot as plt
        self.n_frames=len(this_file)  #  number of frames in this movie
        self.peak_in_frame=[[] for i in range(len(this_file))]
        plt.figure(figsize=(5,10))#change fig size according to the ROI image size
        for row_num in range(2,200,1):#change the row and col number accordingly
            for col_num in range(2,100,1):#50
                if self.mask[row_num][col_num]==1: # only do the region of interest
                    x=[]
                    x_baseline=[]
                    for num_frame in range(len(this_file)):
                        #print(this_file[num_frame][row_num][col_num])
                        add_sum=0
                        for i in range(row_num-1,row_num+2):
                            for j in range(col_num-1,col_num+2):
                                add_sum+=this_file[num_frame][i][j]
                        x.append(add_sum)
                    x_baseline=self.median_smooth(self.median_smooth(x,50),50)
                    smooth_x=self.smooth(self.smooth(x,15),15)  # smooth window size
                    smooth_x=[smooth_x[i]-x_baseline[i] for i in range(len(smooth_x))] # extract the baseline
                    threshold=300
                    for i in range(1,len(smooth_x)-1):
                        if smooth_x[i]>threshold and smooth_x[i]>smooth_x[i-1] and smooth_x[i]>smooth_x[i+1]:
                            plt.scatter(col_num,200-row_num,alpha=0.2,color="black")#subscribe by total row number
                            self.peak_in_frame[i].append([row_num,col_num])
                            print([row_num,col_num])
        print(self.peak_in_frame)
        plt.xlim([0,100])
        plt.ylim([0,200])
        plt.axis('off')
        plt.show()

    def smooth(self,values,window_size):
        import numpy
        out_values=[]
        for i in range(len(values)):
            window_start=max(0,i-int(window_size/2))
            window_end=min(len(values),i+window_size-int(window_size/2)) # this number is the one after the last number in the window
            out_values.append(numpy.mean(values[window_start:window_end]))
        return out_values
    
    def median_smooth(self,values,window_size):
        import numpy
        out_values=[]
        for i in range(len(values)):
            window_start=max(0,i-int(window_size/2))
            window_end=min(len(values),i+window_size-int(window_size/2)) # this number is the one after the last number in the window
            out_values.append(numpy.median(values[window_start:window_end]))
        return out_values
    
    def find_peaks(self,values):
        local_max_pks=[]
        local_max_locs=[]
        for i in range(1,len(values)-1):
            if values[i]>values[i-1] and values[i]>values[i+1]:
                local_max_pks.append(values[i])
                local_max_locs.append(i)
        return [local_max_pks,local_max_locs]
    
    def get_mask(self,file_name):     # used in the read_ROI_from_jpg.py
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg
        img=mpimg.imread(file_name)   # read the jpg file
        # print(img.shape)
        # plt.imshow(img)
        # plt.show()
        # print(img[70][40]) # print a point RGB
        self.mask=[[0 for i in range(img.shape[1])] for j in range(img.shape[0])] # create and initialize a 2D matrix to store the mask
        # plt.figure(figsize=(4,8))
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i][j][0]>100 and img[i][j][1]>100 and img[i][j][2]>100:  # if the pixel is white, it has larger number in R,G,B
                    # print(img[i][j])
                    self.mask[i][j]=1  # in the mask, white region will be labeled as 1, black region is 0
                    # plt.scatter(j,120-i,color="black")  # show the mask in figure
        # plt.xlim([0,50])
        # plt.ylim([0,120])
        # plt.show()
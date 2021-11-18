import arcpy
import pathlib
from pathlib import Path
import os
import pandas as pd
import zipfile
from zipfile import ZipFile
from os.path import basename

counter = 0

#loop through files in the lidar folder
list_of_las = []
path = "M:/LIDAR/Results/Flagler/Lasd/"
files = os.listdir(path)
files

new_path = "M:/LIDAR/Results/AmazonBucket/FlaglerNew/"

#loop through main file folder
for file in files:
    if file.lower().endswith('.lasd'):

        counter = counter + 1
        file_name = "Flagler_"+str(counter)+".lasd"
        old_path = path+file_name
        folder = "Tile"+str(counter)
        aws = "M:/LIDAR/Results/AmazonBucket/FlaglerNew/"
        new_folder_path = aws+folder+"/"

        #make new folder
        os.mkdir(new_folder_path)

        move_location = aws+folder+"/"+file_name

        #move file to new folder
        Path(old_path).rename(move_location)


#loop through DEMs
counter = 0
dem_path = "M:/LIDAR/Results/Flagler/DEM/"
new_path = "M:/LIDAR/Results/AmazonBucket/FlaglerNew/"
all_dem_files = os.listdir(dem_path)
print(len(all_dem_files))
i=0


while i < len(all_dem_files):
    print("Iteration {}".format(i))
    dem_file = all_dem_files[i]
    print(dem_file)
    counter = counter + 1
    keyword = "Flagler_Elev_" + str(counter)
    print(keyword)
    i = i + 1
    if keyword in dem_file:
        print("Moving {}".format(dem_file))
        file_path = dem_path + dem_file
        tile = "Tile" + str(counter)
        out_path = new_path + tile + "/" + dem_file

        # move to folder
        Path(file_path).rename(out_path)
        print("Moved {}".format(dem_file))
    else:
        counter=counter-1
        continue




#loop through contours
counter = 0
contour_path = "M:/LIDAR/Results/Flagler/Contour/"
new_path = "M:/LIDAR/Results/AmazonBucket/FlaglerNew/"
all_contours = os.listdir(contour_path)
i=0

while i < len(all_contours):
    print("Iteration {}".format(i))
    contour_file = all_contours[i]
    print(contour_file)
    counter = counter + 1
    contour_keyword = "Contours_"+str(counter)
    print(contour_keyword)
    i = i + 1
    if contour_keyword in contour_file:
        print("Moving {}".format(contour_file))
        old_path = contour_path + contour_file
        tile = "Tile" + str(counter)
        out_path = new_path + tile + "/" + contour_file
        # move to folder
        Path(old_path).rename(out_path)
        print("Moved {}".format(contour_file))
    else:
        counter=counter-1
        continue


###     MAKING A ZIP FILE FROM A FOLDER THEN LOOPING THROUGH FOLDERS IN A DIRECTORY     ###
#loop through folders in AWS folder and make zipfiles
folders = os.listdir(new_path)

def zip_directory(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, mode='w') as zipf:
        len_dir_path = len(folder_path)
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path[len_dir_path:])

for folder in folders:
    in_path = new_path+folder
    out_path = in_path+".zip"
    print("Zipping {}".format(folder))
    zip_directory(in_path, out_path)
    print("Successfully zipped {}".format(folder))


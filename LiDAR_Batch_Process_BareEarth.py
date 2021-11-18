import arcpy
from arcpy import conversion
from arcpy import sa
from arcpy import management
import os
import pandas as pd

arcpy.env.overwriteOutput = True

#make new log file
log_file = open("C:/Users/madams/Desktop/Python Scripts/lidar_log2.txt", "w")

counter = 0
arcpy.env.Workspace = r"M:/LIDAR/Results/All_DEM/"

#generate list of las files
list_of_las = []
path = "M:/LIDAR/Results/Flagler/Las"
files = os.listdir(path)
files

#loop through las files
for file in files:
    if not file.lower().endswith('.las'):
        continue

    print(file)
    log_file.write(file+"\n")

    #if needing to convert from .laz, change the if statement above to .laz
    #uncomment this if needing to convert from .laz to .las
    in_laz = "M:/GIS on Drone Drive/LIDAR/Statewide Lidar/Raw Data/LAZ/" + file
    target_folder = "M:/LIDAR/Results/Flagler/Las/"
    convert_to_las = conversion.ConvertLas(in_laz, target_folder)
    print(convert_to_las.getMessages())
    log_file.write(convert_to_las + "\n")

    counter = counter + 1
    o_path = "M:/LIDAR/Results/All_DEM/"
    out_name = "Flagler_Elev_" + str(counter) + ".tif"
    out_path = o_path + out_name
    value_field = "ELEVATION"

    size = len(file)
    file_no_ext = file[:size-4]
    in_las = "M:/LIDAR/Results/Flagler/Las/"+file_no_ext +".las"

    lasd_path = "M:/LIDAR/Results/Flagler/Lasd/"
    lasd_name = "Flagler_"+str(counter)+".lasd"
    full_path = lasd_path+lasd_name

    las_to_lasd = management.CreateLasDataset(in_las, full_path)
    las_messages = las_to_lasd.getMessages()
    print(las_messages)
    log_file.write(las_messages+"\n")

    lasd = management.MakeLasDatasetLayer(full_path, lasd_name, class_code=[2])
    lasd_messages = lasd.getMessages()
    print(lasd_messages)
    log_file.write(lasd_messages+"\n")

    #generate DEM raster
    convert_las = conversion.LasDatasetToRaster(lasd, out_path, value_field)
    messages = convert_las.getMessages()
    print(messages)
    log_file.write(messages + "\n")

    #smooth DEM raster using focal statistics
    smoothed_path = o_path+"Smoothed"
    smooth_dem = sa.FocalStatistics(out_path, statistics_type="MEAN")
    smooth_dem.save(smoothed_path)

    # generate contours
    contour_folder = "M:/LIDAR/Results/Flagler/Contour/"
    contour_name = "Contours_" + str(counter)
    contour_path = contour_folder + contour_name+".shp"
    contour_interval = 1

    generate_contours = sa.Contour(smooth_dem, contour_path, contour_interval)
    cont_messages = generate_contours.getMessages()
    print(cont_messages)
    log_file.write(cont_messages + "\n")

#print(list_of_las)

#gdb_path = "M:/GIS on Drone Drive/LIDAR/Statewide Lidar/Results"
#gdb_name = "Contours.gdb"
#make_gdb = arcpy.CreateFileGDB_management(gdb_path, gdb_name)

#counter = 0






import numpy, types
import Nio
import Ngl
import os.path
#This script takes Grib Files from NAM simulations and converts them
#Into .dat format for  Newmanv3.1
t=0
Dates = ["20170904","20170905","20170906","20170907","20170908","20170909","20170910","20170911","20170912"]
Initials = ["00","06","12","18"]
Hours = ["00","01","02","03","04","05"]
fileDir = "/mnt/d/NAM_GRIBS_HUNTERFLIGHTS/"
#Domain Lat Lon
Lat = 37.208
Lon =-80.5803

#Domain origin
iorg = 195
jorg = 155

#Domain size
gridpointsI = 99
gridpointsJ = 101

#Height Level
z = 30 #800 milibar

#Calculate start and end points based on 
#domain size and origin
imin = int(numpy.floor(gridpointsI/2.0))
jmin = int(numpy.floor(gridpointsJ/2.0))
imax = int(numpy.ceil(gridpointsI/2.0))
jmax = int(numpy.ceil(gridpointsJ/2.0))

for day in Dates:
    for init in Initials:
        for hr in Hours:
            filename = fileDir+day+"_"+init+"_"+hr+".grib2"
            print filename
            
            file = Nio.open_file(filename,"r")
            names = file.variables.keys()

            uvar = file.variables["UGRD_P0_L100_GLC0"][:,:,:]
            uvar = numpy.squeeze(uvar[z,:,:])
            dim = numpy.shape(uvar)

            vvar = file.variables["VGRD_P0_L100_GLC0"][:,:,:]
            vvar = numpy.squeeze(vvar[z,:,:])

            #convert m/s to km/hr for consisency
            udesired = 3.6*uvar[(iorg-imin):(iorg+imax),(jorg-jmin):(jorg+jmax)]
            vdesired = 3.6*vvar[(iorg-imin):(iorg+imax),(jorg-jmin):(jorg+jmax)]
            dim =  udesired.shape

            f = open('roms%04d.dat' % t, 'w')
            f.write("Surface Velocity ROMS data (km/hr)\n")	
            #f.write("Domain Center 36.7964N,-120.822E\n")
            f.write("Domain Center "+str(Lat)+"N,"+str(Lon)+"E\n")
            f.write("#Data_XMin = "+str(-1*(dim[1]-1)/2*12.191)+"\n")
            f.write("#Data_XMax = "+str((dim[1]-1)/2*12.191)+"\n")
            f.write("#Data_XRes = "+str(dim[1])+"\n")
            f.write("#Data_YMin = "+str(-1*(dim[0]-1)/2*12.191)+"\n")
            f.write("#Data_YMax = "+str((dim[0]-1)/2*12.191)+"\n")
            f.write("#Data_YRes = "+str(dim[0])+"\n")
            f.write("ZONE T=\"%04d\" I=" % (t+1) +str(dim[1])+" J="+str(dim[0])+"\n")
            for i in range(dim[0]):
                for j in range(dim[1]):
                    f.write(str(udesired[i,j])+" "+str(vdesired[i,j])+"\n")

            f.close()
            t+=1
'''
filename = Dates[-1]+"_"+Initials[-1]+"_006.grb2"
print filename

file = Nio.open_file(filename,"r")
names = file.variables.keys()

# level 30 is the 800 millibar level
uvar = file.variables["UGRD_P0_L100_GLC0"][:,:,:]
uvar = numpy.squeeze(uvar[z,:,:])
dim = numpy.shape(uvar)

vvar = file.variables["VGRD_P0_L100_GLC0"][:,:,:]
vvar = numpy.squeeze(vvar[z,:,:])

udesired = 3.6*uvar[(iorg-imin):(iorg+imax),(jorg-jmin):(jorg+jmax)]
vdesired = 3.6*vvar[(iorg-imin):(iorg+imax),(jorg-jmin):(jorg+jmax)]
dim =  udesired.shape

f = open('roms%04d.dat' % t, 'w')
f.write("Surface Velocity ROMS data (km/hr)\n")	
#f.write("Domain Center 36.7964N,-120.822E\n")
f.write("Domain Center "+str(Lat)+"N,"+str(Lon)+"E\n")
f.write("#Data_XMin = "+str(-1*(dim[1]-1)/2*12.191)+"\n")
f.write("#Data_XMax = "+str((dim[1]-1)/2*12.191)+"\n")
f.write("#Data_XRes = "+str(dim[1])+"\n")
f.write("#Data_YMin = "+str(-1*(dim[0]-1)/2*12.191)+"\n")
f.write("#Data_YMax = "+str((dim[0]-1)/2*12.191)+"\n")
f.write("#Data_YRes = "+str(dim[0])+"\n")
f.write("ZONE T=\"%04d\" I=" % (t+1) +str(dim[1])+" J="+str(dim[0])+"\n")
for i in range(dim[0]):
    for j in range(dim[1]):
        f.write(str(udesired[i,j])+" "+str(vdesired[i,j])+"\n")

f.close()
t+=1
'''
Ngl.end()


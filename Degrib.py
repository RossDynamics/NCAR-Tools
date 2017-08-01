import numpy, types
import Nio
import Ngl
import os.path
#This script takes Grib Files from NAM simulations and converts them
#Into .dat format for  Newmanv3.1
t=0
Dates = ["20160609","20160610"]
Initials = ["0000","0600","1200","1800"]
Hours = ["000","001","002","003","004","005"]
for day in Dates:
    for init in Initials:
        for hr in Hours:
            filename = "../gribs/nam_218_"+day+"_"+init+"_"+hr+".grb2"
            print filename
            
            file = Nio.open_file(filename,"r")
            names = file.variables.keys()

            # level 30 is the 800 millibar level
            uvar = file.variables["UGRD_P0_L100_GLC0"][:,:,:]
            uvar = numpy.squeeze(uvar[30,:,:])
            dim = numpy.shape(uvar)

            vvar = file.variables["VGRD_P0_L100_GLC0"][:,:,:]
            vvar = numpy.squeeze(vvar[30,:,:])

            #hardcoded origin to save time
            iorg = 195
            jorg = 155
            #choose -102 +103, want 2000km domain, with 500km bufferzone 
            #(total velocity field defined on 2500km^2)  centered at (36.7964,-120.822), 
            #with 12.191km gridspacing, 103 is roughly 1250km
            #and convert m/s to km/hr for consisency
            udesired = 3.6*uvar[(iorg-103):(iorg+104),(jorg-103):(jorg+104)]
            vdesired = 3.6*vvar[(iorg-103):(iorg+104),(jorg-103):(jorg+104)]
            dim =  udesired.shape

            f = open('roms%04d.dat' % t, 'w')
            f.write("Surface Velocity ROMS data (km/hr)\n")	
            f.write("Domain Center 36.7964N,-120.822E\n")
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
            
Ngl.end()


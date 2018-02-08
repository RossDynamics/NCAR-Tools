import numpy, types
import Nio
import Ngl
"""
Script reads a Grib File and gets basic information about the file and the domain.
!!! REQUIRES PyNIO and PyNGL from NCAR !!!
"""
#Set Parameters
#Marthas Vinyard
#Latorg = 41.3209371228     #Desired Origin Lat
#Lonorg =-70.53690039    #Desired Origin Lon
#Kentland Farm
Latorg = 37.19636
Lonorg =-80.57834

tol = 0.0125         #How close to desired origin do you want to get
filename = "20170904_00_00.grib2"
gridspacing = 3

#gridpointsI = 317 #Chose odd number so you will have the desired origin
#gridpointsJ = 317 #Chose odd number so you will have the desired origin
gridpointsI = 99 #Chose odd number so you will have the desired origin
gridpointsJ = 101 #Chose odd number so you will have the desired origin
#Open Grib File
file = Nio.open_file(filename,"r")
names = file.variables.keys()


for i in range(len(names)):
	#print "\n" + names[i]
        if names[i][:8]=="lv_ISBL0":
	    print "\n" + names[i]
	    print file.variables[names[i]].dimensions
	    for attrib in file.variables[names[i]].attributes.keys():
		print attrib + " has value ",  getattr(file.variables[names[i]],attrib)
            a = file.variables[names[i]][:]
            print a[41]
                    
        if names[i]=="UGRD_P0_L100_GLC0":
	    print "\n" + names[i]
	    print file.variables[names[i]].dimensions
	    for attrib in file.variables[names[i]].attributes.keys():
    		print attrib + " has value ",  getattr(file.variables[names[i]],attrib)
            a = file.variables[names[i]][:]
            print a.shape
            #print a
                

uvar = file.variables["UGRD_P0_L100_GLC0"][:,:,:]
uvar = numpy.squeeze(uvar[-1,:,:])
dim = numpy.shape(uvar)
print dim
vvar = file.variables["VGRD_P0_L100_GLC0"][:,:,:]
vvar = numpy.squeeze(vvar[-1,:,:])

lat = file.variables["gridlat_0"][:,:]
lon = file.variables["gridlon_0"][:,:]
#Find the index of the origin
print "want lat lon", Latorg, Lonorg
for i in range(dim[0]):
	for j in range(dim[1]):
		if numpy.fabs(lat[i,j]-Latorg)<tol and numpy.fabs(lon[i,j]-Lonorg)<tol:
			print 'closest we can get is', lat[i,j], lon[i,j]
			print i,j
			iorg = i
			jorg = j

u = 3.6*uvar
v = 3.6*vvar

umax = numpy.max(u)
vmax = numpy.max(v)
print "Max u", umax
print "Max v", vmax

space0 = gridspacing*(dim[0]-iorg-1)
space1 = gridspacing*(dim[1]-jorg-1)
print "Have " + str(space0) + " kms of space from origin N/S"
print "Have " + str(space1) + " kms of space from origin E/W"
print (dim[0]-iorg)
print (dim[1]-jorg)

time0 = space0/vmax
time1 = space1/umax

print "Can integrate for " + str(numpy.min([time0,time1])) + "hrs"

mini = int(numpy.floor(gridpointsI/2.0))
minj = int(numpy.floor(gridpointsJ/2.0))
maxi = int(numpy.ceil(gridpointsI/2.0))
maxj = int(numpy.ceil(gridpointsJ/2.0))
print mini, minj, maxi, maxj
latdes = lat[(iorg-mini):(iorg+maxi),(jorg-minj):(jorg+maxj)]
londes = lon[(iorg-mini):(iorg+maxi),(jorg-minj):(jorg+maxj)]
print latdes[mini,minj],londes[mini,minj] #Confirm Origin is correct

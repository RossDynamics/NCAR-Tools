import numpy, types
import Nio
import Ngl
"""
Script reads a Grib File and gets basic information about the file and the domain.
!!! REQUIRES PyNIO and PyNGL from NCAR !!!
"""
#Set Parameters
Latorg = 36.75      #Desired Origin Lat
Lonorg =-120.875    #Desired Origin Lon
tol = 0.075         #How close to desired origin do you want to get
filename = "../gribs/nam_218_20160609_0000_000.grb2"
gridpointsI = 207 #Chose odd number so you will have the desired origin
gridpointsJ = 207 #Chose odd number so you will have the desired origin
#Open Grib File
file = Nio.open_file(filename,"r")
names = file.variables.keys()

'''
for i in range(len(names)):
	print "\n" + names[i]
	if names[i][:5]=="lv_IS":
		print "\n" + names[i]
		print file.variables[names[i]].dimensions
		for attrib in file.variables[names[i]].attributes.keys():
			print attrib + " has value ",  getattr(file.variables[names[i]],attrib)


'''

uvar = file.variables["UGRD_P0_L100_GLC0"][:,:,:]
uvar = numpy.squeeze(uvar[30,:,:])
dim = numpy.shape(uvar)
print dim
vvar = file.variables["VGRD_P0_L100_GLC0"][:,:,:]
vvar = numpy.squeeze(vvar[30,:,:])

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


mini = numpy.floor(gridpointsI/2.0)
mini = numpy.floor(gridpointsI/2.0)
maxj = numpy.ceil(gridpointsJ/2.0)
maxj = numpy.ceil(gridpointsJ/2.0)
print mini, minj, maxi, maxj
latdes = lat[(iorg-mini):(iorg+maxi),(jorg-minj):(jorg+maxj)]
londes = lon[(iorg-mini):(iorg+maxi),(jorg-minj):(jorg+maxj)]
print latdes[mini,minj],londes[mini,minj] #Confirm Origin is correct

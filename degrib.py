import numpy, types

import Nio
import Ngl
import os.path

t=0
while 1:
	filename = "../gribs/nam_218_20160609_0000_%03d.grb2" % t
	if not os.path.isfile(filename):
		break
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
	#choose -41 +42, want 1000km domain centered at (36.75,-120.875), with 12.191km gridspacing, 83 is roughly 1000km
	udesired = uvar[(iorg-41):(iorg+42),(jorg-41):(jorg+42)]
	vdesired = vvar[(iorg-41):(iorg+42),(jorg-41):(jorg+42)]
	dim =  udesired.shape

	f = open('roms%04d.dat' % t, 'w')
	f.write("Surface Velocity ROMS data (m/s)\n")
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


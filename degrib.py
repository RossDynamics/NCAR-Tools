import numpy, types

import Nio
import Ngl

def main():
	file = Nio.open_file("../gribs/nam_218_20160609_0000_000.grb2","r,")
	names = file.variables.keys()

	# level 30 is the 800 millibar level
	uvar = file.variables["UGRD_P0_L100_GLC0"][:,:,:]
	uvar = numpy.squeeze(uvar[30,:,:])
	dim = numpy.shape(uvar)
	print dim

	vvar = file.variables["VGRD_P0_L100_GLC0"][:,:,:]
	vvar = numpy.squeeze(vvar[30,:,:])


	lat = file.variables["gridlat_0"][:,:]
	lon = file.variables["gridlon_0"][:,:]

	#hardcoded origin to save time
	iorg = 195
	jorg = 155
	#choose -41 +42, want 1000km domain centered at (36.75,-120.875), with 12.191km gridspacing, 83 is roughly 1000km
	#latdes = lat[(iorg-41):(iorg+42),(jorg-41):(jorg+42)]
	#londes = lon[(iorg-41):(iorg+42),(jorg-41):(jorg+42)]
	#print latdes[83,41],londes[41,41]
	#print latdes.shape
	udesired = uvar[(iorg-41):(iorg+42),(jorg-41):(jorg+42)]
	vdesired = vvar[(iorg-41):(iorg+42),(jorg-41):(jorg+42)]
	dim =  udesired.shape
	#f = open('roms.dat','w')
	t=1

	#if t>=1000:
	#	break
	print(t)
	filenumber=determineNumber(t)
	zone=determineZone(t)
	f = open('roms'+filenumber+'.dat', 'w')
	f.write("Surface Velocity ROMS data (m/s)\n")
	f.write("#Data_XMin = "+str(-1*(dim[1]-1)/2*12.191)+"\n")
	f.write("#Data_XMax = "+str((dim[1]-1)/2*12.191)+"\n")
	f.write("#Data_XRes = "+str(dim[1])+"\n")
	f.write("#Data_YMin = "+str(-1*(dim[0]-1)/2*12.191)+"\n")
	f.write("#Data_YMax = "+str((dim[0]-1)/2*12.191)+"\n")
	f.write("#Data_YRes = "+str(dim[0])+"\n")
	f.write("ZONE T=\""+zone+"\" I="+str(dim[1])+" J="+str(dim[0])+"\n")
	for i in range(dim[0]):
		for j in range(dim[1]):
			f.write(str(udesired[i,j])+" "+str(vdesired[i,j])+"\n")

	f.close()
	Ngl.end()

def determineNumber(timestep):
	if timestep <10:
		w='000'+str(timestep)
	elif timestep>=10 and timestep<100:
		w='00'+str(timestep)
	elif timestep>=100 and timestep<1000:
		w='0'+str(timestep)
	return w;

def determineZone(timestep):
	if timestep <10:
		zone='000'+str(timestep+1)
	elif timestep>=10 and timestep<100:
		zone='00'+str(timestep+1)
	elif timestep>=100 and timestep<1000:
		zone='0'+str(timestep+1)
	return zone;

main()

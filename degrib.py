import numpy, types
from scipy.interpolate import SmoothSphereBivariateSpline as sinterp
#from scipy.interpolate import RectSphereBivariateSpline as sinterp
import Nio
import Ngl

file = Nio.open_file("nam_218_20160609_0000_000.grb2","r,")
names = file.variables.keys()

'''
for i in range(len(names)):
	print "\n" + names[i]
	if names[i][:5]=="lv_IS":
		print "\n" + names[i]
		print file.variables[names[i]].dimensions
		for attrib in file.variables[names[i]].attributes.keys():
			print attrib + " has value ",  getattr(file.variables[names[i]],attrib)


level = file.variables["lv_ISBL0"]
print numpy.shape(level)
print file.variables["lv_ISBL0"].dimensions
print level[30]
'''

uvar = file.variables["UGRD_P0_L100_GLC0"]
uvar = numpy.squeeze(uvar[30,:,:])
dim = numpy.shape(uvar)
#size = numpy.size(uvar)
vvar = file.variables["VGRD_P0_L100_GLC0"]
vvar = numpy.squeeze(vvar[30,:,:])

'''
xgrid = file.variables["xgrid_0"]
print numpy.shape(xgrid)
print xgrid

ygrid = file.variables["ygrid_0"]
print numpy.shape(ygrid)
print ygrid
'''
lat = file.variables["gridlat_0"]
lon = file.variables["gridlon_0"]

theta = (lat[:,:] + 90*numpy.ones(numpy.shape(lat)))*numpy.pi/180
phi = (lon[:,:] + 360*numpy.ones(numpy.shape(lon)))*numpy.pi/180

'''
Nlat =  max(lat[:,0])
Slat =  min(lat[:,-1])
Wlon =  min(lon[0,:])
Elon =  max(lon[0,:])
'''

Nth =  max(theta[:,0])
Sth =  min(theta[:,-1])
Wph =  min(phi[0,:])
Eph =  max(phi[0,:])
'''
print "%.5f" % Nth
print "%.5f" % Sth
print "%.5f" % Wph
print "%.5f" % Eph

print dim[0],dim[1]
'''
newtheta = numpy.linspace(Sth,Nth,dim[0])
newphi = numpy.linspace(Wph,Eph,dim[1])

newphi, newtheta = numpy.meshgrid(newphi,newtheta)


print numpy.shape(theta)
print numpy.shape(newtheta)

'''
theta = numpy.reshape(theta,size)
newtheta = numpy.reshape(newtheta,size)
phi = numpy.reshape(phi,size)
newphi = numpy.reshape(newphi,size)
uvar = numpy.reshape(uvar[:,:],size)
vvar = numpy.reshape(vvar[:,:],size)
'''

theta = numpy.ravel(theta)
newtheta = numpy.ravel(newtheta)
phi = numpy.ravel(phi)
newphi = numpy.ravel(newphi)
uvar = numpy.ravel(uvar[:,:])
vvar = numpy.ravel(vvar[:,:])

'''
import sys
sys.stdout.flush()
print "Interp"
uinterp = sinterp(theta,phi,uvar)
print "Set"
sys.stdout.flush()
newu = uinterp(newtheta,newphi)
print "Done"
'''

'''
print theta
print newtheta
print phi
print newphi
'''




'''
for i in range(100):
	for j in range(100):
		print uvar[i,j], vvar[i,j], lat[i,j], lon[i,j]
'''

Ngl.end()

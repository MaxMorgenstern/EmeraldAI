
import numpy as np
#from scipy.interpolate import interp2d, interp1d, interpnd

pixel = [0, 2, 6.5, 9.5, 12.5, 16, 27.5, 45.5, 98, 106, 160]
distance = [663, 440, 286, 222, 173, 136, 90, 57, 30, 22, 16]

x = 0
while x < 200:
	print x, np.interp(x, pixel, distance)
	x += 1

#interpol = interp1d(pixel, distance)


#mesh = np.linspace(0, 200, num=10)

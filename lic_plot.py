import lic
import matplotlib.pyplot as plt
import numpy
# ... get x and y arrays from somewhere ...
x = numpy.ndarray(shape=(200,200), dtype=float, order='F')
y = numpy.ndarray(shape=(200,200), dtype=float, order='F')
lic_result = lic.lic(x, y, length=30)
 
plt.imshow(lic_result, origin='lower', cmap='gray')
plt.show()
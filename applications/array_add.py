import sys
import numpy
import time
import datetime
start = datetime.datetime.today().strftime("%d-%b-%Y %H:%M:%S")
print("Start Time:", start)
if len(sys.argv) > 1:
    n_loops = int(sys.argv[-1])
else:
    n_loops = 500
matrix_size = 1000
print(matrix_size)
print(n_loops)
for n in range(n_loops):
    a = numpy.random.uniform(low=-1.0, high=1.0,size=(matrix_size, matrix_size))
    b = numpy.random.uniform(low=-1.0, high=1.0,size=(matrix_size, matrix_size))
    x = numpy.matmul(a,b)
print("End Time: ", datetime.datetime.today().strftime("%d-%b-%Y %H:%M:%S"))


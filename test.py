from timeit import timeit
from pygame import Vector3

a = Vector3(1, 2, 3)
print(timeit('Vector3(2 + a[0], 2 + a[1], 2 + a[2])', globals=globals()))
print(timeit('Vector3(2 , 2 , 2 ) + a', globals=globals()))

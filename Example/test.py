import numpy as np

posi_0=np.array([
                [1,2,3],
                [1,2,3],
                [1,2,3],
                [1,2,3],
                ])


posi_1=np.array([
                [1,3,3],
                [1,3,3],
                [1,3,3],
                [1,3,3],
                ])


u=(posi_1-posi_0)/0.1
r=np.array([[1,1,0.5,0.5]]).T

print(u*r)
import random

import numpy as np
import matplotlib.pyplot as plt

pts=100
t2 = np.linspace(0.0,5.0,pts)
t2=(t2/50)
tm=t2*(10**3)
nz=t2.size
tc=np.linspace(0.8,2.5,2)
nz=tc.size
for n in range (nz):
       print(tc[n])
       resp = 1 - np.exp(-tc[n]*tm*10**-3*50) * np.cos(2*np.pi*50*tm*10**-3)
       for m in range(pts):
           plt.xlim(0,100)
           plt.ylim(0,2)
           plt.xlabel('Time,in milliseconds',fontsize=12)
           plt.ylabel('Respose',fontsize=12)
           plt.title('Underdamped Second Order System Step Response',fontsize=14)
           line1,=plt.plot(tm[0:m+1],resp[0:m+1],color='black',linewidth=0.2)
           line2,=plt.plot(tm[m],resp[m],marker='o',color='red',markersize=0.2)
           ax = plt.gca()
           plt.pause(0.00001)
           ax.lines.remove(line2)
           plt.grid('on')
plt.show()


from pylab import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import seaborn as sns

N = 10000  
sigma = 10
r = 28
b = 8/3
t0 = 0     
tf = 50    
h = (tf-t0)/N

def f(v,t): 
    v0 = sigma*(v[1]-v[0])
    v1 = r*v[0]-v[1]-v[0]*v[2]
    v2 = v[0]*v[1]-b*v[2]
    return array([v0,v1,v2],float)

tpoints = linspace(t0,tf,N)
v = array([0.0,1.0,0.0],float) 
xpoints = []
ypoints = []
zpoints = []

# Runge Kutta 4
for t in tpoints: 
    xpoints.append(v[0])
    ypoints.append(v[1])
    zpoints.append(v[2])
    k1 = h*f(v,t)
    k2 = h*(f((v+0.5*k1),(t+0.5*h)))
    k3 = h*f((v+0.5*k2),(t+0.5*h))
    k4 = h*f((v+k3),(t+h))
    v += (1/6)*(k1+2*k2+2*k3+k4)

# --- GRAFİK AYARLARI ---
sns.set_style("darkgrid")

fig = plt.figure(figsize=(16, 9)) 

ax1 = plt.subplot(3,3,1)
ax2 = plt.subplot(3,3,2)
ax3 = plt.subplot(3,3,3)
axf = plt.subplot(3,3,(4,9), projection='3d') 


ax1.set_xlim(0, tf) 
ax1.set_ylim(min(xpoints), max(xpoints))
ax1.set_xlabel('Time')
ax1.set_ylabel('x(t)')
ax1.set_title('Graphical representation of x(t)')


ax2.set_xlim(0, tf)
ax2.set_ylim(min(ypoints), max(ypoints))
ax2.set_xlabel('Time')
ax2.set_ylabel('y(t)')
ax2.set_title('Graphical representation of y(t)')


ax3.set_xlim(0, tf)
ax3.set_ylim(min(zpoints), max(zpoints))
ax3.set_xlabel('Time')
ax3.set_ylabel('z(t)')
ax3.set_title('Graphical representation of z(t)')


axf.set_xlim(-20,23)
axf.set_ylim(-22,30)
axf.set_zlim(0,55)
axf.set_xlabel('x(t)')
axf.set_ylabel('y(t)')
axf.set_zlabel('z(t)')


txt_title = axf.set_title('')
line1, = ax1.plot([],[],'-r', lw=1.5)
pt1, = ax1.plot([],[],'.k', ms=10)

line2, = ax2.plot([],[],'-g', lw=1.5)
pt2, = ax2.plot([],[],'.k', ms=10)

line3, = ax3.plot([],[],'-m', lw=1.5)
pt3, = ax3.plot([],[],'.k', ms=10)

linef, = axf.plot3D([],[],[],'-b', lw=1)
ptf, = axf.plot3D([],[],[],'.k', ms=10)

# --- ANİMASYON FONKSİYONU ---
def drawframe(n):
    
    x = xpoints[n]
    y = ypoints[n]
    z = zpoints[n]
    t = tpoints[n]
    
    txt_title.set_text(f'Frame = {n}')
    
    # 3D 
    linef.set_data_3d(xpoints[:n], ypoints[:n], zpoints[:n])
    ptf.set_data_3d([x], [y], [z])
    
    # 2D 
    line1.set_data(tpoints[:n], xpoints[:n])
    pt1.set_data([t], [x])
    
    line2.set_data(tpoints[:n], ypoints[:n])
    pt2.set_data([t], [y])
    
    line3.set_data(tpoints[:n], zpoints[:n])
    pt3.set_data([t], [z])
    
    return (linef, ptf, line1, pt1, line2, pt2, line3, pt3, txt_title)

import cv2
import numpy as np

print("Video oluşturuluyor, lütfen bekleyiniz...")

fig.canvas.draw()

# Matplotlib 3.8+ için geçerli yöntem:
height, width = fig.canvas.get_width_height()
video = cv2.VideoWriter('lorenz_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

for n in range(0, 10000, 5):
    try:
        drawframe(n)
       
        fig.canvas.draw()
        
        img = np.array(fig.canvas.buffer_rgba())
        
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        
        video.write(img)
        
        if n % 100 == 0:
            print(f"Kare işleniyor: {n}")
            
    except Exception as e:
        print(f"Hata oluştu (Kare {n}): {e}")
        break

video.release()
plt.close() 

print("Video oluşturuluyor, lütfen bekleyiniz...")

fig.canvas.draw()
img_test = np.array(fig.canvas.buffer_rgba())

height, width, layers = img_test.shape

video = cv2.VideoWriter('lorenz_animasyon.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, (width, height))

for n in range(0, 10000, 5):
    try:

        drawframe(n)
        
        fig.canvas.draw()
        
        img = np.array(fig.canvas.buffer_rgba())
        
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        video.write(img)
        
        if n % 200 == 0:
            print(f"İşleniyor... Kare: {n}")
            
    except Exception as e:
        print(f"Hata: {e}")
        break

video.release()
plt.close()

print("Tamamlandı! Dosya adı: 'lorenz_animasyon.avi'")
plt.show()
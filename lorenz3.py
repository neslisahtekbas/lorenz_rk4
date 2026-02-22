from pylab import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import seaborn as sns

# --- SABİTLER VE HESAPLAMALAR ---
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

# Runge Kutta Hesabı
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
# Seaborn stilini aktif edelim (daha güzel görünür)
sns.set_style("darkgrid")

fig = plt.figure(figsize=(16, 9)) # Pencere boyutunu biraz optimize ettim

# Subplotları oluşturuyoruz
ax1 = plt.subplot(3,3,1)
ax2 = plt.subplot(3,3,2)
ax3 = plt.subplot(3,3,3)
axf = plt.subplot(3,3,(4,9), projection='3d') # projection='3d' burada doğru kullanım

# Gráfica 1 #
ax1.set_xlim(0, tf) # X ekseni zaman olduğu için 0-50 arası daha mantıklı
ax1.set_ylim(min(xpoints), max(xpoints))
ax1.set_xlabel('Time')
ax1.set_ylabel('x(t)')
ax1.set_title('Graphical representation of x(t)')

# Gráfica 2 #
ax2.set_xlim(0, tf)
ax2.set_ylim(min(ypoints), max(ypoints))
ax2.set_xlabel('Time')
ax2.set_ylabel('y(t)')
ax2.set_title('Graphical representation of y(t)')

# Gráfica 3 #
ax3.set_xlim(0, tf)
ax3.set_ylim(min(zpoints), max(zpoints))
ax3.set_xlabel('Time')
ax3.set_ylabel('z(t)')
ax3.set_title('Graphical representation of z(t)')

# Gráfica final (3D) #
axf.set_xlim(-20,23)
axf.set_ylim(-22,30)
axf.set_zlim(0,55)
axf.set_xlabel('x(t)')
axf.set_ylabel('y(t)')
axf.set_zlabel('z(t)')

# Başlık ve Çizgiler
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
    # Hızlandırmak için her frame'de değil, n. frame'e kadar çiziyoruz
    
    x = xpoints[n]
    y = ypoints[n]
    z = zpoints[n]
    t = tpoints[n]
    
    txt_title.set_text(f'Frame = {n}')
    
    # 3D Güncelleme
    linef.set_data_3d(xpoints[:n], ypoints[:n], zpoints[:n])
    ptf.set_data_3d([x], [y], [z])
    
    # 2D Güncellemeler
    line1.set_data(tpoints[:n], xpoints[:n])
    pt1.set_data([t], [x])
    
    line2.set_data(tpoints[:n], ypoints[:n])
    pt2.set_data([t], [y])
    
    line3.set_data(tpoints[:n], zpoints[:n])
    pt3.set_data([t], [z])
    
    return (linef, ptf, line1, pt1, line2, pt2, line3, pt3, txt_title)

import cv2
import numpy as np

# 1. Animasyon nesnesini iptal edelim, manuel döngü kuracağız.
# (Eski 'anim = ...' satırının silindiğinden emin ol)

print("Video oluşturuluyor, lütfen bekleyiniz...")

# Grafik penceresini bir kez çizdirip boyutlarını alalım
fig.canvas.draw()

# --- YENİ YÖNTEM (buffer_rgba kullanıyoruz) ---
# Matplotlib 3.8+ için geçerli yöntem:
height, width = fig.canvas.get_width_height()
video = cv2.VideoWriter('lorenz_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

# 2. Kareleri tek tek işle ve videoya ekle
# Hızlı bitmesi için 20'şer atlayarak 2000 kareye kadar gidiyoruz
for n in range(0, 10000, 5):
    try:
        # Senin yazdığın drawframe fonksiyonunu çağırıyoruz
        drawframe(n)
        
        # Grafiği güncelle
        fig.canvas.draw()
        
        # --- GÜNCELLEME BURADA YAPILDI ---
        # tostring_rgb yerine buffer_rgba kullanıyoruz
        img = np.array(fig.canvas.buffer_rgba())
        
        # OpenCV renkleri BGR (Mavi-Yeşil-Kırmızı) ister, Matplotlib ise RGBA verir.
        # Bu yüzden renkleri çeviriyoruz:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        
        # Videoya ekle
        video.write(img)
        
        # İlerleme durumunu göster
        if n % 100 == 0:
            print(f"Kare işleniyor: {n}")
            
    except Exception as e:
        print(f"Hata oluştu (Kare {n}): {e}")
        break

# 3. İşlem bitince videoyu kapat ve kaydet
video.release()
plt.close() # Pencereyi kapat

print("Video oluşturuluyor, lütfen bekleyiniz...")

# 1. Grafik penceresini bir kez çizdirip gerçek boyutları alalım
# (Bu yöntem ekran ölçekleme hatalarını kesin olarak çözer)
fig.canvas.draw()
img_test = np.array(fig.canvas.buffer_rgba())

# Boyutları doğrudan alınan resimden öğreniyoruz
height, width, layers = img_test.shape

# 2. Video oluşturucuyu hazırla
# '.avi' formatı ve 'DIVX' codec'i Windows'ta sorunsuz çalışır.
video = cv2.VideoWriter('lorenz_animasyon.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, (width, height))

# 3. Kareleri işle ve videoya ekle
# Hızlı sonuç almak için 2000 kareye kadar, 10'ar atlayarak gidiyoruz
for n in range(0, 10000, 5):
    try:
        # Çizim fonksiyonunu çağır
        drawframe(n)
        
        # Grafiği güncelle
        fig.canvas.draw()
        
        # Resmi al (RGBA formatında)
        img = np.array(fig.canvas.buffer_rgba())
        
        # Renkleri düzelt (RGBA -> BGR) ve videoya yaz
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        video.write(img)
        
        # İlerleme durumunu %10'da bir yazdır
        if n % 200 == 0:
            print(f"İşleniyor... Kare: {n}")
            
    except Exception as e:
        print(f"Hata: {e}")
        break

# 4. İşlemi bitir
video.release()
plt.close()

print("Tamamlandı! Dosya adı: 'lorenz_animasyon.avi'")
plt.show()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

# --- 1. Parametreler ---
x, y, z = 0.1, 1.0, 10.0
rho, sigma, beta = 28.0, 10.0, 8.0/3.0
t0, tf = 0, 60  # Süreyi animasyon için biraz kısalttım (çok uzun sürmesin diye)
dt = 0.01       # Adım aralığı
t = np.arange(t0, tf + dt, dt)
n = len(t)

# --- 2. Lorenz Denklemleri ve RK4 ---
def EDOs(t, r):
    x, y, z = r
    return np.array([sigma * (y - x), rho * x - y - x * z, x * y - beta * z])

def RK4(t, r, f, dt):
    k1 = dt * f(t, r)
    k2 = dt * f(t + dt/2, r + k1/2)
    k3 = dt * f(t + dt/2, r + k2/2)
    k4 = dt * f(t + dt, r + k3)
    return r + (k1 + 2*k2 + 2*k3 + k4) / 6

# --- 3. Hesaplama Döngüsü ---
evol = np.zeros((n, 3))
evol[0] = [x, y, z]

# Python'da döngüleri bu şekilde optimize edebilirsin ama senin yazdığın da doğru
for i in range(n - 1):
    evol[i + 1] = RK4(t[i], evol[i], EDOs, dt)

# --- 4. Görselleştirme (Eksik Olan Kısım Burasıydı) ---
fig = plt.figure(figsize=(10, 10), facecolor='black') # Siyah tema
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')

# Eksen ayarları
ax.set_xlim((-25, 25))
ax.set_ylim((-35, 35))
ax.set_zlim((5, 55))
ax.grid(False) # Izgaraları kapattım daha şık dursun diye
ax.axis('off') # Eksen çizgilerini gizle

# Çizgi ve nokta nesneleri
line, = ax.plot([], [], [], lw=1.5, color='#FFD700')
point, = ax.plot([], [], [], 'o', color='white')

# Başlangıç fonksiyonu (Animasyon için)
def init():
    line.set_data([], [])
    line.set_3d_properties([])
    point.set_data([], [])
    point.set_3d_properties([])
    return line, point

target_duration = 30 # saniye
fps = 50
interval_ms = int(1000 / fps) # 20 ms
total_frames = target_duration * fps
speed_up = int(n / total_frames) 

def init():
    line.set_data([], [])
    line.set_3d_properties([])
    point.set_data([], [])
    point.set_3d_properties([])
    return line, point 

def update(frame):
    i = frame * speed_up
    if i >= n: return line, point # Dizi sınırını aşmasın
    
    # Şu ana kadar olan tüm yolu çiz (iz bırakarak)
    line.set_data(evol[:i, 0], evol[:i, 1])
    line.set_3d_properties(evol[:i, 2])
    
    # En uçtaki noktayı çiz
    point.set_data([evol[i, 0]], [evol[i, 1]]) # Liste içine almazsak hata verir
    point.set_3d_properties([evol[i, 2]])
    
    # Kamerayı hafifçe döndür (Estetik dokunuş)
    ax.view_init(elev=10, azim=i*0.25)
    
    return line, point

# Animasyonu oluştur
ani = animation.FuncAnimation(fig, update, frames=total_frames + 1, init_func=init, 
                              interval=interval_ms, blit=False)

plt.show()

function lorenz_rk4
    clc; close all;

    sigma = 10;
    beta  = 8/3;
    rho   = 28;

    T_bitis = 50;     % Simülasyon süresi
    dt = 0.005;       % Adım aralığı (RK4 için 0.01 bile yeterlidir ama 0.005 çok hassas hesaplama yapmamızı sağlar)
    N = floor(T_bitis / dt); % Adım sayısı

    altin_rengi = [0.85, 0.65, 0.15];

    % --- 2. Ön Hazırlık (Preallocation) ---
    x = zeros(N, 1);
    y = zeros(N, 1);
    z = zeros(N, 1);
    
    % Başlangıç Koşulları
    x(1) = 1;
    y(1) = 1;
    z(1) = 1;

    % --- 3. Runge-Kutta 4 Döngüsü ---
    % Bu döngüdeki her adımda 4 eğim hesabı yapılır.
    for i = 1 : N-1
        % Mevcut durum
        xi = x(i); yi = y(i); zi = z(i);

        % -- K1 Adımı (Başlangıç eğimi) --
        [k1x, k1y, k1z] = lorenz_turevleri(xi, yi, zi, sigma, beta, rho);

        % -- K2 Adımı (Yarım adım ilerideki eğim, K1'i kullanarak) --
        [k2x, k2y, k2z] = lorenz_turevleri(xi + dt*k1x/2, yi + dt*k1y/2, zi + dt*k1z/2, sigma, beta, rho);

        % -- K3 Adımı (Yarım adım ilerideki eğim, K2'yi kullanarak) --
        [k3x, k3y, k3z] = lorenz_turevleri(xi + dt*k2x/2, yi + dt*k2y/2, zi + dt*k2z/2, sigma, beta, rho);

        % -- K4 Adımı (Tam adım ilerideki eğim, K3'ü kullanarak) --
        [k4x, k4y, k4z] = lorenz_turevleri(xi + dt*k3x, yi + dt*k3y, zi + dt*k3z, sigma, beta, rho);

        % -- Ağırlıklı Ortalama ile Yeni Değeri Bulma --
        % Formül: y_yeni = y_eski + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)
        x(i+1) = xi + (dt/6) * (k1x + 2*k2x + 2*k3x + k4x);
        y(i+1) = yi + (dt/6) * (k1y + 2*k2y + 2*k3y + k4y);
        z(i+1) = zi + (dt/6) * (k1z + 2*k2z + 2*k3z + k4z);
    end

    % --- 4. Çizim  ---
    figure('Color', 'w', 'Name', 'Lorenz RK4');
    
    plot3(x, y, z, 'Color', altin_rengi, 'LineWidth', 1.5);
    
    title({'Lorenz Attractor';'Runge-Kutta 4 Method'}, 'FontSize', 12);
    xlabel('x axis'); ylabel('y axis'); zlabel('z axis');
    grid on;
    
    view(45, 20); 
    
    box on; 
end

% --- YARDIMCI FONKSİYON: Lorenz Türevleri ---
% Bu fonksiyon, ana döngünün içini temiz tutmak için sadece o anki noktadaki dx, dy, dz değerlerini hesaplar.
function [dx, dy, dz] = lorenz_turevleri(x, y, z, s, b, r)
    dx = s * (y - x);
    dy = x * (r - z) - y;
    dz = x * y - b * z;

end

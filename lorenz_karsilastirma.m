function lorenz_karsilastirma
    clc; close all;

    sigma = 10; beta = 8/3; rho = 28;
    t_son = 20;     
    dt = 0.01;      
    N = floor(t_son / dt);
    baslangic = [1; 1; 1];

    % --- 2. HESAPLAMALAR ---
    
    % A) ODE45
    options = odeset('RelTol',1e-8, 'AbsTol',1e-8);
    [t_ode, sonuc_ode] = ode45(@(t,y) lorenz_func(t,y,sigma,beta,rho), [0 t_son], baslangic, options);
    
    % *** DÜZELTME 1: Değişkenleri burada tanımlıyoruz ***
    x_ode = sonuc_ode(:,1); 
    y_ode = sonuc_ode(:,2); 
    z_ode = sonuc_ode(:,3);

    % B) Euler Metodu
    xe = zeros(N,1); ye = zeros(N,1); ze = zeros(N,1);
    xe(1)=baslangic(1); ye(1)=baslangic(2); ze(1)=baslangic(3);
    for i=1:N-1
        dx = sigma * (ye(i) - xe(i));
        dy = xe(i) * (rho - ze(i)) - ye(i);
        dz = xe(i) * ye(i) - beta * ze(i);
        xe(i+1) = xe(i) + dx*dt; ye(i+1) = ye(i) + dy*dt; ze(i+1) = ze(i) + dz*dt;
    end

    % C) RK4 Metodu
    xr = zeros(N,1); yr = zeros(N,1); zr = zeros(N,1);
    xr(1)=baslangic(1); yr(1)=baslangic(2); zr(1)=baslangic(3);
    for i=1:N-1
        xi=xr(i); yi=yr(i); zi=zr(i);
        [k1x, k1y, k1z] = lorenz_vals(xi, yi, zi, sigma, beta, rho);
        [k2x, k2y, k2z] = lorenz_vals(xi+dt*k1x/2, yi+dt*k1y/2, zi+dt*k1z/2, sigma, beta, rho);
        [k3x, k3y, k3z] = lorenz_vals(xi+dt*k2x/2, yi+dt*k2y/2, zi+dt*k2z/2, sigma, beta, rho);
        [k4x, k4y, k4z] = lorenz_vals(xi+dt*k3x,   yi+dt*k3y,   zi+dt*k3z,   sigma, beta, rho);
        xr(i+1) = xi + (dt/6)*(k1x+2*k2x+2*k3x+k4x);
        yr(i+1) = yi + (dt/6)*(k1y+2*k2y+2*k3y+k4y);
        zr(i+1) = zi + (dt/6)*(k1z+2*k2z+2*k3z+k4z);
    end

    % --- 3. GÖRSELLEŞTİRME  ---
    fig = figure('Color','w');
    set(fig, 'Position', [0, 0, 1400, 800]); 
    movegui(fig, 'center');

    t_man = (0:N-1)*dt; 
    
    % SOL TARAFI KAPLAYAN BÜYÜK 3D GRAFİK
    subplot(3, 2, [1, 3, 5]); 
    plot3(x_ode, y_ode, z_ode, 'b', 'LineWidth', 2.5); hold on;
    plot3(xr, yr, zr, 'Color', [0.85, 0.65, 0.15], 'LineWidth', 2, 'LineStyle','--');
    plot3(xe, ye, ze, 'r', 'LineWidth', 1.5, 'LineStyle', ':');
    title('3D Phase Plane');
    xlabel('x axis'); ylabel('y axis'); zlabel('z axis');
    legend('ODE45', 'RK4', 'Euler', 'Location', 'northwest');
    grid on; view(45, 20); axis equal;

    % SAĞ ÜST (X Zaman Serisi) -> 2. Kutu
    subplot(3, 2, 2);
    plot(t_ode, x_ode, 'b', 'LineWidth', 1.5); hold on;
    plot(t_man, xr, 'Color', [0.85, 0.65, 0.15], 'LineWidth', 1.5, 'LineStyle','--');
    plot(t_man, xe, 'r', 'LineWidth', 1.5, 'LineStyle', ':');
    title('x - Time Graph'); ylabel('x axis'); grid on; xlim([0 15]);

    % SAĞ ORTA (Y Zaman Serisi) -> 4. Kutu
    subplot(3, 2, 4);
    plot(t_ode, y_ode, 'b', 'LineWidth', 1.5); hold on;
    plot(t_man, yr, 'Color', [0.85, 0.65, 0.15], 'LineWidth', 1.5, 'LineStyle','--');
    plot(t_man, ye, 'r', 'LineWidth', 1.5, 'LineStyle', ':');
    title('y - Time Graph'); ylabel('y axis'); grid on; xlim([0 15]);

    % SAĞ ALT (Z Zaman Serisi) -> 6. Kutu
    subplot(3, 2, 6);
    plot(t_ode, z_ode, 'b', 'LineWidth', 1.5); hold on;
    plot(t_man, zr, 'Color', [0.85, 0.65, 0.15], 'LineWidth', 1.5, 'LineStyle','--');
    plot(t_man, ze, 'r', 'LineWidth', 1.5, 'LineStyle', ':');
    title('z - Time Graph'); xlabel('Time (t)'); ylabel('z axis'); grid on; xlim([0 15]);
end

% --- YARDIMCI FONKSİYONLAR ---
function dydt = lorenz_func(~, y, s, b, r)
    dydt = [s*(y(2)-y(1)); y(1)*(r-y(3))-y(2); y(1)*y(2)-b*y(3)];
end

function [dx, dy, dz] = lorenz_vals(x, y, z, s, b, r)
    dx = s * (y - x);
    dy = x * (r - z) - y;
    dz = x * y - b * z;
end
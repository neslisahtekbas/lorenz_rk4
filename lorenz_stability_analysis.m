sigma = 10;
beta  = 8/3;
rho   = 28;  % Try 0.5, 1, 13.926, 24.06, 24.736, 28, 30

fprintf('--------------------------------------------------\n');
fprintf('LORENZ SYSTEM STABILITY ANALYSIS (rho = %.3f)\n', rho);
fprintf('sigma = %.2f, beta = %.4f\n', sigma, beta);
fprintf('--------------------------------------------------\n\n');

% Charasteristic Equation: (lambda + beta) * (lambda^2 + (sigma+1)lambda + sigma(1-rho)) = 0 

fprintf('--- 1. ORIJIN (0,0,0) ---\n');

L1_origin = -beta;

% coefficients: [1, (sigma+1), sigma*(1-rho)]
p_origin = [1, (sigma+1), sigma*(1-rho)];
roots_origin_quad = roots(p_origin);

eigenvalues_origin = [L1_origin; roots_origin_quad];

for i = 1:3
    fprintf('lambda_%d = %.4f + %.4fi\n', i, real(eigenvalues_origin(i)), imag(eigenvalues_origin(i)));
end

if any(real(eigenvalues_origin) > 0)
    fprintf('>> RESULT: ORIJIN IS UNSTABLE - Saddle Point\n\n');
else
    fprintf('>> RESULT: ORIJIN IS STABLE\n\n');
end

if rho > 1
    fprintf('--- 2. (C_1 ve C_2) ---\n');
    
    z_star = rho - 1;
    x_star = sqrt(beta * z_star);
    fprintf('C_1: (%.2f, %.2f, %.2f)\n', x_star, x_star, z_star);
    
    % CHARASTERISTIC EQUATION COEFFICIENTS (CUBIC)
    % P(lambda) = lambda^3 + a1*lambda^2 + a2*lambda + a3 = 0
    
    a1 = sigma + beta + 1;
    a2 = beta * (sigma + rho);
    a3 = 2 * sigma * beta * (rho - 1);
    
    coeff_sym = [1, a1, a2, a3];
    eigenvalues_sym = roots(coeff_sym);
    
    for i = 1:3
        fprintf('lambda_%d = %.4f + %.4fi\n', i, real(eigenvalues_sym(i)), imag(eigenvalues_sym(i)));
    end
    
    reals = real(eigenvalues_sym);
    imags = imag(eigenvalues_sym);
    
sifir_sayisi = sum(abs(reals) < 0);
pozitif_var = any(reals > 0);

if pozitif_var
    stability = 'UNSTABLE';

elseif sifir_sayisi == 0
    stability = 'STABLE';

elseif sifir_sayisi == 2
    stability = 'HOPF BIFURCATION';
end
    
    fprintf('>> RESULT: %s %s\n', stability);
    
    rhc = 470/19; 

if rho < 1.3456
    fprintf('(EXP: Diskriminant > 0, Real Roots)\n');

elseif abs(rho - rhc) < 0.0001
    fprintf('HOPF BIFURCATION\n');

elseif rho < rhc
    fprintf('(EXP: Diskriminant < 0, Routh-Hurwitz provided -> Damped Oscilation)\n');

else
    fprintf('(EXP: Routh-Hurwitz not provided -> Chaos)\n');
end
    
else
    fprintf('--- (C_1 ve C_1) ---\n');
    fprintf('These fixed points do not exist because of rho < 1.\n');
end
fprintf('--------------------------------------------------\n');



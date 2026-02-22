# 3D Simulation of the Lorenz System using Runge-Kutta 4 (RK4)

This project contains Python and MATLAB implementations for the numerical solution and visualization of the **Lorenz System**, an advanced model in chaos theory and dynamical systems.

## 📌 Project Overview
The simulation investigates the sensitive dependence on initial conditions and the formation of the "Lorenz Attractor." The system is defined by the following set of nonlinear ordinary differential equations (ODEs):

$$
\huge
\begin{aligned}
\frac{dx}{dt} &= \sigma(y - x) \\
\frac{dy}{dt} &= x(\rho - z) - y \\
\frac{dz}{dt} &= xy - \beta z
\end{aligned}
$$

## 🚀 Key Features
* **Numerical Solver:** Implemented using the **4th Order Runge-Kutta (RK4)** method for high precision.
* **Visualization:** 3D phase space plotting of the butterfly-shaped attractor.
* **Technical Background:** Includes stability, quantitative and qualitative theory concepts.

## ⚙️ Parameters & Dynamics
* **Default Values:** $$σ = 10$$, $$β = \frac{8}{3}$$, and $$ρ = 28$$.
* **Control Parameter:** In this simulation, ρ is the main changeable parameter used to observe significant changes in the system's behavior.
* **Observations:** Therefore, this simulation shows that varying ρ leads to different bifurcation points, illustrating the transition from stability to chaos.

## 🎓 Academic Context
This work was developed during my undergraduate studies in Mathematics at **Dokuz Eylul University**. It represents my interest in qualitative and quantitative analysis of nonlinear dynamics.

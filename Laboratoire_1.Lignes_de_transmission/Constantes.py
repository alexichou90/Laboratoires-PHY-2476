import numpy as np

#Constantes Physiques
c = 2.99792458e8                    #Vitesse de la lumiere dans le vide (m s^-1)

e = 1.6021766208e-19                #Charge elementaire (C)

k_B = 1.38064852e-23                #Constante de Boltzmann (J K^-1)

R = 8.3144598                       #Constante de gaz parfait (J K^-1)

G = 6.67408e-11                     #Constante gravitationelle (m^3 kg^-1 s^-2)

h = 6.626070040e-31                 #Constante de planck (J s)
hbar = h/(2*np.pi)

alpha = e**2 / (4*np.pi*hbar*c)     #Constante de structure fine
alpha_inverse = alpha**-1

m_e = 9.10938356e-31                #Masse d'un electron (kg)

m_p = 1.672621898e-27               #Masse d'un proton (kg)

N_A = 6.022140857e23                #Nombre d'Avogadro

mu_0 = 4*np.pi*1e-7                 #Permeabilite du vide (H m^-1) ou (N A^2)

epsilon_0 = 1/(mu_0*c**2)           #Permittivite du vide (F m^-1) ou (C^2 N^-1 m)

F = N_A*e                           #Constante de Faraday (C mol^-1)

amu = 1.660539040e-27               #Unite de masse atomique
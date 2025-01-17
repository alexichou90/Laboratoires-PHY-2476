"""
Fonctions.py
Ce fichier contient les differentes fonctions utilisees dans le programme.
"""
import numpy as np
import scipy as sc
import Constantes as cst
import matplotlib.pyplot as plt
import math
import random



# Function to generate sigma within ±1% of sigma_c
def generate_random_sigma():
    min_sigma = sigma_c - sigma_c_incertitude  # Lower bound (1% less)
    max_sigma = sigma_c + sigma_c_incertitude  # Upper bound (1% more)
    
    # Generate a random value within the range
    sigma_random = random.uniform(min_sigma, max_sigma)
    
    return sigma_random

#Modele de ligne de transmission: R, L, C et G
class modeleTransmission:

    def ResistanceR(omega,b,a):         #Resistance par unite de longeur Ω/m
        return 0.5*np.sqrt((cst.mu_0*omega)/(2*np.pi**2*6e7))*((1/a)+(1/b))
    
    def InductanceL(b,a):               #Inductance par unite de longeur H/m
        return ((cst.mu_0)/(2*np.pi))*np.log(b/a)
    
    def CapacitanceC():                 #Capacitance par unite de longeur F/m
        return cst.CapacitanceCable
    
    def ConductanceG(sigma,b,a):        #Conductance par unite de longeur S/m
        return (2*np.pi*sigma)/(np.log(b/a))
#Parametres de ligne de transmission: Z, Y, et Z_0
class paramTransmission:

    def ImpedanceZ(omega, R, L):        #Impendance par unite de longeur
        return R + 1j*omega*L
   
   
    def AdmitanceY(omega, C, G):        #Admitance par unite de longeur
        return G + 1j*omega*C
    

    def ImpedanceZ_0(b,a):              #Impedance caracteristique
        return (1/(2*np.pi)) * np.sqrt(cst.mu_0/cst.e) * np.log(b/a) 
#Parametres de propagation: alpha, beta, gamma et vitesse de groupe
class paramPropagation:

    def Alpha(R,L,C):                   #Parametre Alpha
        return (R/2)*np.sqrt(C/L)

    def Beta(omega,L,C):                #Parametre Beta
        return omega*np.sqrt(L*C)

    def Gamma(Y,Z):                     #Parametre Gamma
        return np.sqrt(Y*Z)

    def VitesseGroupe(L,C):             #La vitesse de groupe de l'onde
        return 1/np.sqrt(L*C)
    


#Methode de navigation de menu
class Menu:

    #Fonctions display
    def PrincipalDisp():            #Affichage du menu principal
        print("\nMenu Principal:")
        print("===============")
        print("1. Stocker donnees du laboratoire")
        print("2. Produire des graphiques")
        print("3. Trouver alpha, Z_0 et vg")
        print("4. Quitter")
    def StockageDisp():             #Affichage du menu pour stocker de l'information
        print("\nStocker de l'information:")
        print("=========================")
        print("1. Le cas ou: Z_L -> infini")
        print("2. Le cas ou: Z_L = Z_0")
        print("3. Retour au menu principal")
    def GraphiqueDisp():             #Affichage du menu pour graphiques
        print("\nProduire des graphiques:")
        print("=========================")
        print("1. Le cas ou: Z_L -> infini")
        print("2. Le cas ou: Z_L = Z_0")
        print("3. Retour au menu principal")
    def PropDisp():                  #Affichage du menu les parametres de propagation
        print("\nProduire des graphiques:")
        print("=========================")
        print("1. Le cas ou: Z_L -> infini")
        print("2. Le cas ou: Z_L = Z_0")
        print("3. Retour au menu principal")



#Methode pour stocker de l'information dans un fichier txt
def ecrireData(option):
    try:

        if option == "1":
            fichier = "CasZLinfini.txt"
        else:
            fichier = "CasZLZ0.txt"

        with open(fichier, "a") as file:
            #Cas1 ZL tend vers l'infini
            if option == "1":
                while True:

                    print("\nLe Format: [CH1 pic (ns), VCH1, CH2 pic (ns), VCH2]")
                    CH1 = input("> ")
                    VCH1 = input("> ")
                    CH2 = input("> ")
                    VCH2 = input("> ")

                    file.write(CH1 + ";" + VCH1 + ";" + CH2 + ";" + VCH2 + "\n")
                    print("Ajouter un autre pic? [Y/N]")
                    choix_1 = input("> ")
                    if choix_1.lower() == "y":
                        pass
                    elif choix_1.lower() == "n":
                        break
                    else:
                        print("Choix Invalide")
            #Cas2 ZL = Z0
            else:
                while True:

                    print("\nLe Format: [Z0]")
                    Z0 = input("> ")

                    file.write(Z0 + "\n")
                    print("Ajouter un autre pic? [Y/N]")
                    choix_1 = input("> ")
                    if choix_1.lower() == "y":
                        pass
                    elif choix_1.lower() == "n":
                        break
                    else:
                        print("Choix Invalide")
    
    except IOError as e:
        print(f"Une Erreur a eu lieu l'or de l'ecriture au fichier.")

#Methode pour extrarie de l'information dans un fichiertxt
def lireData(option):
    try:
        if option == "1":
            fichier = "CasZLinfini.txt"
        else:
            fichier = "CasZLZ0.txt"

        dataArray = []

        with open(fichier, "r") as file:
            print("\nLes Données du Fichier:")
           
            if option == "1":
                for line in file:
                    data = line.strip().split(";")
                    if len(data) != 4:
                        raise ValueError(f"Invalid line format: {line.strip()}")
                    dataArray.append([float(value) for value in data])

            else:
                for line in file:
                    data = line.strip().split(";")
                    if len(data) != 1:
                        raise ValueError(f"Invalid line format: {line.strip()}")
                    dataArray.append([float(data[0])])

        return dataArray  # Return the two-dimensional array
    
    except FileNotFoundError:
        print("Erreur: Le fichier " + fichier + " n'existe pas.")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")

#Méthode principale pour gérer les menus
def Interact():  
        while True:
            Menu.PrincipalDisp()
            choice = input("Choisissez une option (1-4): ")

            if choice == "1":  # Menu Stockage
                while True:
                    Menu.StockageDisp()
                    sub_choice = input("Choisissez une option (1-3): ")
                    if sub_choice == "3":  # Retour au menu principal
                        break
                    elif sub_choice == "1":
                        ecrireData(sub_choice)
                    elif sub_choice == "2":
                        ecrireData(sub_choice)
                    else:
                        print(f"Action pour Stockage option {sub_choice}...")

            elif choice == "2":  # Menu Graphiques
                while True:
                    Menu.GraphiqueDisp()
                    sub_choice = input("Choisissez une option (1-3): ")
                    if sub_choice == "3":  # Retour au menu principal
                        break
                    elif sub_choice == "1":
                        array = lireData(sub_choice)
                        PlotData(array)
                        print(array)
                    elif sub_choice == "2":
                        array = lireData(sub_choice)
                        print(array)
                    else:
                        print(f"Action pour Graphique option {sub_choice}...")

            elif choice == "3":  # Menu Propagation
                while True:
                    Menu.PropDisp()
                    sub_choice = input("Choisissez une option (1-3): ")
                    if sub_choice == "4":  # Retour au menu principal
                        break
                    else:
                        print(f"Action pour Propagation option {sub_choice}...")

            elif choice == "4":  # Quitter
                print("Merci d'avoir utilisé le menu. Au revoir!")
                break
            else:
                print("Option invalide, veuillez réessayer.")


#Methode pour produire un graphique de mon data
def PlotData(dataArray):
    # Prepare data for two sets of peaks
    time_set_1 = []
    tension_set_1 = []
    time_set_2 = []
    tension_set_2 = []

    TimeRANGE = np.linspace(0, 7000e-9, 14000)
    tensions = [TensionSurTemps(1,t) for t in TimeRANGE]

    real_tensions = [np.real(tension) for tension in tensions]
    imag_tensions = [np.imag(tension) for tension in tensions]

    # Loop through the data array and separate the times and tensions for both sets
    for data in dataArray:
        time_set_1.append(data[0])
        tension_set_1.append(data[1])
        time_set_2.append(data[2])
        tension_set_2.append(data[3])

    # Plotting the first set of peaks (Time vs Tension)
    plt.plot(time_set_1, tension_set_1, 'ro-', label="Set 1 (Peaks)", markersize=8)  # Red color, circles, solid line
    # Plotting the second set of peaks (Time vs Tension)
    plt.plot(time_set_2, tension_set_2, 'bo-', label="Set 2 (Peaks)", markersize=8)  # Blue color, circles, solid line

    plt.plot(TimeRANGE, real_tensions)

    # Labeling the axes
    plt.xlabel("Time (ns)")
    plt.ylabel("Tension (V)")

    # Adding title
    plt.title("Graph of Tension vs Time (Peaks)")

    # Adding a legend
    plt.legend()

    # Show the graph
    plt.show()




#Calcul de V1 et V2, pour les fonction V(z,t) et i(z,t)
def TensionSurTemps(option, t):
    rsigma = generate_random_sigma()
    
    G = modeleTransmission.ConductanceG(rsigma, cst.rayonB, cst.rayonA)
    Y = paramTransmission.AdmitanceY(omega, C, G)
    
    if option == "1":  # ZL tends to infinity
        C_RV = 1
        C_TV = 2
    else:  # ZL = Z0
        C_RV = 0
        C_TV = 1
        
    V_1 = cst.potentielIncident * C_TV
    V_2 = cst.potentielIncident * C_RV
    
    


    # Calculate the exponential factors
    exp_factor_1 = alpha_exp * np.exp(1j * omega * t + beta * cst.LongeurCable)
    exp_factor_2 = alpha_neg * np.exp(1j * omega * t - beta * cst.LongeurCable)

    return V_1 * exp_factor_1 + V_2 * exp_factor_2  














sigma_c = 6e7                           #Conductivite du conducteur de cuivre en (S m^-1)
sigma_c_incertitude = 0.01*sigma_c      #Marge d'erreur de 1%
omega = 2 * np.pi * cst.Frequence       #OMEGA



R = modeleTransmission.ResistanceR(omega,cst.rayonB,cst.rayonA)
L = modeleTransmission.InductanceL(cst.rayonB,cst.rayonA)
C = modeleTransmission.CapacitanceC()
alpha = paramPropagation.Alpha(R,L,C)
beta = paramPropagation.Beta(omega,L,C)

alpha_exp = np.exp(alpha * cst.LongeurCable)
alpha_neg = np.exp(-alpha * cst.LongeurCable)

print(beta)


Interact()
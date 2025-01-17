"""
Laboratoire 1 - Lignes de transmission
"""
#Importation des libraries
import matplotlib as plt
import numpy as np
import scipy as sc
import math
import Constantes as cst


#variables importates
mu = cst.mu_0                           #Tant que pour les conducteurs que pour le dielectrique, on peut consciderer  que mu = mu_0
sigma_c = 6e7                           #Conductivite du conducteur de cuivre en (S m^-1)
sigma_c_incertitude = 0.01*sigma_c      #Marge d'erreur de 1%
sigma_p_max = 1e-7                      #Conductivite du blindage
b_a_ratio = cst.rayonB/cst.rayonA       #ratio b/a 
impCarZ0 = (1/2*np.pi)*np.sqrt(mu/cst.e)*np.log(b_a_ratio)

#Calcul de R, L, C et G
def calculInductance():
    #Calcul de L par unite de longeur H/m.
    return ((mu)/(2*np.pi))*np.log(b_a_ratio)
def calculResistance(omega):
    #Calcul de R par unite de longeur en Ω/m.
    return 0.5*np.sqrt((mu*omega)/(2*np.pi**2*sigma_c))*((1/cst.rayonA)+(1/cst.rayonB))
def calculCapacitance():
    #Calcul de C par unite de longeur F/m.
    return cst.CapacitanceCable
def calculConductance(sigma):
    #Calcul de G par unite de longeur S/m.
    return (2*np.pi*sigma)/(np.log(b_a_ratio))


#Calcul de Z et Y base sur R, L, C, G et omega
def calculImpedanceZ(omega, R, L):
    #calcul de l'impendace par unite de longeur Z
    return R + 1j*omega*L
def calculAdmitanceY(omega, C, G):
    #calcul de l'admitance par unite de longeur Y
    return G + 1j*omega*C


#Calcul de Alpha, Beta et Gamma
def calculGamma(Y,Z):
    #calcul de gamma 
    return np.sqrt(Y*Z)
def calculAlpha(R,L,C):
    #calcul de alpha
    return (R/2)*np.sqrt(C/L)
def calculBeta(omega,L,C):
    #calcul de beta
    return omega*np.sqrt(L*C)


#Calcul de la vitessge de groupe
def calculVg(L,C):
    #calcul de la vitesse de groupe
    return 1/np.sqrt(L*C)


#Calcul de V1 et V2, pour les fonction V(z,t) et i(z,t)
def calculer_V1_V2(V_incident, Z_0, Z_L):
    C_RV = (Z_L-Z_0)/(Z_L+Z_0)
    C_TV = 1 + C_RV
    V_1 = V_incident*C_TV
    V_2 = V_incident*C_RV
    return V_1, V_2


#Calcul de V(z,t) et i(z,t)
def calculTension(V_1,V_2,z,t,alpha,beta,omega):
    return V_1*math.exp(alpha*z)*math.exp(1j*omega*t + beta*z) + V_2*math.exp(-alpha*z)*math.exp(1j*omega*t - beta*z)
def calculCourant(V_1,V_2,Z,Y,z,t,alpha,beta,omega):
    return (-V_1/np.sqrt(Z/Y))*math.exp(alpha*z)*math.exp(1j*omega*t + beta*z) + (V_2/np.sqrt(Z/Y))*math.exp(-alpha*z)*math.exp(1j*omega*t - beta*z)


#Calcul de Z_0
def calculZ_0():
    return (1/(2*np.pi)) * np.sqrt(mu/cst.e) * np.log(b_a_ratio)


#Lire et ecrire Data a un fichier.
def ecrireData():
    try:
        with open("LaboratoireData.txt", "a") as file:
            while True:
                print("\n Le format: [omega; V_I; C]")
                omega = input("> ")
                V_I = input("> ")
                C = input("> ")
                file.write(omega + ";" + V_I + ";" + C)
                choix_1 = input("Ajouter un autre point de data? [Y/N]: ")
                if choix_1.lower() == "y":
                    pass
                elif choix_1.lower() == "n":
                    break
                else:
                    print("Choix Invalide")
                    break
    except IOError as e:
        print(f"Une Erreur a eu lieu l'or de l'ecriture au fichier.")
def lireData():
    try:
        with open("LaboratoireData.txt", "r") as file:
            print("\nLes Données du Fichier:")
            for line in file:
                data = line.strip().split(";")
                if len(data) != 4:
                    raise ValueError(f"Invalid line format: {line.strip()}")
                yield float(data[0]), float(data[1]), float(data[2]), float(data[3])
    except FileNotFoundError:
        print("Erreur: Le fichier 'LaboratoireData.txt' n'existe pas.")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")


#Le menu principal
def menu():
        print("\nMenu Principal:")
        print("1. Ajoute de l'information")
        print("2. Produit des graphiques")
        print("3. Trouve alpha, Z_0 et vg")
        print("4. Quitter")


def main():
    while True:
        menu()
        choix = int(input("> "))

        #ajouter du data a un document
        if choix == 1:
            ecrireData()

        #lire l'information du document et produit des graphiques
        elif choix == 2:
            try:
                # Create plots
                fig, axs = plt.subplots(2, 1, figsize=(10, 8))
                for O, V, a, b in lireData():
                    #calculs de base
                    b_a_ratio = b / a
                    L = calculInductance(b_a_ratio)
                    R = calculResistance(O, a, b)
                    C = calculCapacitance(b_a_ratio)
                    G = calculConductance(sigma_c, b_a_ratio)
                    
                    #calcul impedances
                    Z = calculImpedanceZ(O,R,L)
                    Y = calculAdmitanceY(O,C,G)

                    #calcul de alpha, beta et gamma
                    gamma = calculGamma(Y,Z)
                    alpha = calculAlpha(R,L,C)
                    beta = calculBeta(O,L,C)

                    #calcul de la vitesse de groupe et de V1 et V2
                    vg = calculVg(L,C)
                    Z_0 = calculZ_0(L,C)


                    #A faire
                    Z_L = calculZ_L()
                    V_1, V_2 = calculer_V1_V2(V,Z_0,Z_L)

                # End of data processing
                print("Fin de la lecture du fichier.")
            except Exception as e:
                print(f"Une erreur s'est produite: {e}")




        elif choix == 3:
            pass


        elif choix == 4:
            break

        else:
            print("Choix invalide")



if __name__ == "__main__":
    main()







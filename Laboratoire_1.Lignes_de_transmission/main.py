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


#Calcul de R, L, C et G
def calculInductance(b_a_ratio):
    #Calcul de L par unite de longeur H/m.
    return ((mu)/(2*np.pi))*np.log(b_a_ratio)
def calculResistance(omega, a, b):
    #Calcul de R par unite de longeur en Ω/m.
    return 0.5*np.sqrt((mu*omega)/(2*np.pi**2*sigma_c))*((1/a)+(1/b))
def calculCapacitance(b_a_ratio):
    #Calcul de C par unite de longeur F/m.
    return (2*np.pi*cst.epsilon_0)/(np.log(b_a_ratio))
def calculConductance(sigma, b_a_ratio):
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
def calculZ_0(L,C):
    return np.sqrt(L/C)


#Lire et ecrire Data a un fichier.
def ecrireData():
    try:
        with open("LaboratoireData.txt", "a") as file:
            while True:
                print("\n Le format: [omega; V_I; a; b]")
                omega = input("> ")
                V_I = input("> ")
                a = input("> ")
                b = input("> ")
                file.write(omega + ";" + V_I + ";" + a + ";" + b + "\n")
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






#Methode pour le programme:

"""
Le programme commence avec un menu avec 3 options:

1. Ajouter de l'information
2. faire des calculs pour chaque test et produit un graphique de l'evolution dans le temps, a differentente longeurs z.
3. quitter


==========
Option 1.

a) le programme va demander l'information en sequence comme pour la classe si dessous, pour l'inputter

Classe Data
[Frequence angulaire de l'onde: omega; Amplitude de l'onde/Voltage incident: V; Rayon du cuivre: a; Rayon du blindage: b]

b) le programme ecrit l'information dans le fichier "LaboratoireData.txt"
c) le programme demande si on ajoute un autre data ou non
    i) si oui, retourne a a)
    ii) si non retourne au menu principal

==========
Option 2.

a) le programme lit ligne par ligne le fichier "LaboratoireData"
    i) pour une ligne, trouve V(z,t) et i(z,t)
        1) produit des graphiques qui les representes dans 3 dimensions:     axe des x, V(z,t) ou i(z,t);  axe des y, t;  axe des z, z.
        2) produit des graphiques en 2 dimensions:    axe des x, t;  axe des y, V(z,t) ou i(z,t) avec des valeurs de z discretes.
b) passe a la prochaine ligne, tant que tout les tests ne sont pas sur le graphique
c) renderer les graphiques et retourner au menu principal.



                #calcul des fonctions:
                b_a_ratio = data[3]/data[2]
                L = calculInductance(b_a_ratio)
                R = calculResistance(data[0],data[2],data[3])
                C = calculCapacitance(b_a_ratio)
                G = calculConductance(sigma_c, b_a_ratio)

                #calcul impedances
                Z = calculImpedanceZ(data[0],R,L)
                Y = calculAdmitanceY(data[0],C,G)

                #calcul de alpha, beta et gamma
                gamma = calculGamma(Y,Z)
                alpha = calculAlpha(R,L,C)
                beta = calculBeta(data[0],L,C)

                #calcul de la vitesse de groupe et de V1 et V2
                vg = calculVg(L,C)
                Z_0 = calculZ_0(L,C)


                #A faire
                Z_L = calculZ_L()
                V_1, V_2 = calculer_V1_V2(data[1],Z_0,Z_L)









==========
Option 3.

Fermeture du programme.

"""






















"""
---------------------------
impedance characteristique:

on definit l'impedance charactersitique Z_0 du cable coaxial comme:
Z_0 = V_I(z,t)/i_I(z,t)

ou I denote l'onde incidente.
ce qui est approximativement:
Z_0 approx sqrt[L/C] = (1/2*np.pi) * sqrt(mu/epsilon) * ln(b/a)

Quand on veut transmettre un signal sur une ligne, deux problèmes principaux se posent :
d'une part, on veut que la ligne présente le moins de pertes possibles, et d'autre part, si on veut
transmettre des puissances élevées, on aimerait que la tension de claquage dans le diélectrique
soit la plus grande possible. On peut montrer que l'atténuation dans le câble est minimale pour
un rapport b/a égal à 3.59 ce qui conduit à une impédance caractéristique de 77 Ω. Par ailleurs,
le rapport b/a pour lequel on peut faire passer un maximum de puissance est de 1.65, ce qui
donne une impédance de 30 Ω environ. L'industrie a donc choisi une valeur moyenne de 50 Ω, qui
est un compromis entre pertes minimales et puissance transmissible maximale. Les installations
TV travaillent à 75 Ω car on cherche à minimiser les pertes pour une ligne donnée, mais il n'est
pas nécessaire de transmettre de grandes puissances.


--------------------------------------
Coeffs de reflexion et de transmission

coeff de reflexion est donne par:
C_RV = V_R(z,t)/V_I(z,t) = (Z_L-Z_0)/(Z_L+Z_0)

celui pour le courant est:
C_RI = -C_RV

quant au coeff de transmission de charge s'ecrit
C_TV = 1 + C_RV

Notons 3 cas limites:
Z_L -> infini, C_RV = 1, C_TV = 2
Z_L = 0, C_RV = -1, C_TV = 0
Z_L -> -infini, C_RV = 0, C_TV = 1
"""


"""
Questions preparatoires:

Comment fait-on pour produire des impulsions à partir d'un générateur de fonction ?
Comment fait-on pour obtenir les cas limites ZL → ∞, ZL → 0 et ZL → Z0 à la sortie
d'un câble coaxial ?
Quel instrument pourrait-on utiliser pour caractériser la propagation et l'atténuation
d'impulsions dans une ligne à transmission ?

"""

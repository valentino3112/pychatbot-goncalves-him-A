import os
import math


#Fonction qui permet de renvoyer une liste contenant le nom des fichiers et son extension choisi
def list_of_files(directory, extension): #on prends une entrée (directory) ainsi que l'extension d'un fichier (extension)
    files_names = []
    for filename in os.listdir(directory): #boucle qui recommence dans tous les fichiers présent dans le répertoire choisi
        if filename.endswith(extension): #verifie si le nom du fichier se finit par la même extension
            files_names.append(filename) #si oui, il l'ajoute au fichier "files_names"
    return files_names

#On récupère le nom du président et nous retourne le resultat
def extraire_nom_president(nom: str):
    result = nom[11:-4].rstrip("1234567890") #on prends le nom qui se trouve à l'indice 11 jusqu'à l'indice -4 en supprimant les chiffres allant de 0 à 9
    return result

#On prends les noms des présidents sans doublons et le retourne dans la liste
def liste_des_pres():
    resultat = []
    for txt in list_of_files("speeches", "txt"): #on choisie l'entrée ainsi que l'extension du fichier
        if extraire_nom_president(txt) not in resultat: #si le nom du président n'est pas déjà dans le résultat, on le rajoute à la fin de la list
            resultat.append(extraire_nom_president(txt))
    return resultat

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

#permet d'associer un prénom à chaque nom de famille d'un président
def fullname_liste_pres():
    resultat = []
    for i in range(len(liste_nom_pres)):
        resultat.append((prenoms[i], liste_nom_pres[i]))
    return resultat

#On nettoie le fichier texte "speeches" et on l'enregistre dans un nouveau répertoire "cleaned"
def clean_text():
    for txt in list_of_files("speeches", "txt"): #on ouvre tous les fichiers dans "speeches" avec l'extension "txt"
        with open("speeches/" + txt, 'r') as f: #on ouvre les fichiers en mode lecture
            contents = f.read().casefold().replace(".","").replace(",","").replace("!", "").replace("'"," ").replace("-", " ").replace("`","").replace("\n", " ").replace("   ", " ").replace("  ", " ") #On remplace les lettres majuscules par des minuscules, on supprime les ".",",","!" et on remplace les "'","-" par des espaces
        with open('cleaned/' + txt, 'w') as f: #on ouvre un noveau fichier en mode ecriture
            f.write(contents) #Toutes les modifications apportées vont être dans le fichiers "cleaned"

def everywordonce(corpus):
    words = []
    result = []
    for i in corpus:
        for j in i.split():
            if j not in words:
                result.append(j)
            words.append(j)
    return result

#Fonction qui écrit le nombre d'occurences de chaque mots présent dans les discours des présidents
def tf(texte: str):
    corpus = []
    for nom in list_of_files("cleaned","txt"):
        with open("cleaned/"+nom) as f:
            corpus.append(f.read())
    everyword = everywordonce(corpus)
    liste_mots = texte.split()
    result = {}
    words = []
    occurence = 0
    for mot in everyword:
        occurence = 0
        for mot_dans_doc in liste_mots:
            if mot == mot_dans_doc:
                occurence = occurence + 1
        if mot not in words:
            result[mot] = occurence / len(liste_mots)
        words.append(mot)
    return result

#a
def idf(repertoire: str) :
    corpus = []
    tf_du_corpus = []
    for nom in list_of_files(repertoire,"txt"):
        with open(repertoire +"/"+nom) as f:
            corpus.append(f.read())
    for txt in corpus:
        tf_du_corpus.append(tf(txt))
    occurence = 0
    idf = {}
    mots_parcouru = []
    for tfdoc in tf_du_corpus:
        for mot in tfdoc:
            occurence = 0
            for texte in corpus:
                if mot in texte:
                    occurence = occurence + 1  #si le mot apparait dans un des texte du corpus on fait +1
            if mot not in mots_parcouru: #pour eviter doublons
                idf[mot] = math.log10(len(corpus) / occurence)
            mots_parcouru.append(mot)
    return idf

def score_tfidf(repertoire):
    corpus = []
    for nom in list_of_files(repertoire, "txt"):
        with open(repertoire + "/" + nom) as f:
            corpus.append(f.read())

    tf_du_corpus = []
    for txt in corpus:
        tf_du_corpus.append(tf(txt))

    idf_corpus = idf(repertoire)

    matrice = [[0 for k in range(len(corpus))] for i in range(len(idf_corpus))]

    for i, v in zip(range(len(idf_corpus)), idf_corpus):        #chaque ligne correspond à un mot
        for j in range(len(tf_du_corpus)):                      #chaque colonnes correspond à un doc
            matrice[i][j] = idf_corpus[v]*tf_du_corpus[j][v]    #idf*tf

    return matrice




prenoms = ["Jacques", "Valéry", "François", "Emmanuel", "François", "Nicolas"]
liste_nom_pres = liste_des_pres()
liste_nom_pres.sort()


liste_pres = fullname_liste_pres()
print(liste_pres)

clean_text()
idf_corpus = idf("cleaned")
print(len(idf_corpus))
matrice_score_tf_idf =  score_tfidf("cleaned")
print(len(matrice_score_tf_idf))
print("done")
for i,k in zip(matrice_score_tf_idf, idf_corpus):
    if i == [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]:
        print("mot moins utiliser:", k)

# print(len(score_tfidf("cleaned")))
#
# for i in score_tfidf("cleaned"):
#     print(i)



# while True:
#     print("\nMenu :")
#     print("1. Afficher les mots les moins importants")
#     print("2. Afficher les mots ayant le score TF-IDF le plus élevé")
#     print("3. Indiquer les mots les plus répétés par le président Chirac")
#     print("4. Indiquer le président ayant le plus parlé de la 'Nation' et le nombre de répétitions")
#     print("5. Indiquer le premier président à parler du climat ou de l'écologie")
#     print("6. Trouver les mots évoqués par tous les présidents")
#
#
#     choix = input("Choisissez une option : ")
#
#     if choix == '1':
#         print("Les mots les moins importants sont :")
#         for i in matrice_score_tf_idf:
#
#     elif choix == '2':
#         print("Les mots les plus importants sont :")
#     elif choix == '3':
#         print("Les mots les plus répétés de Chirac sont :")
#     elif choix == '4':
#         print("Les noms des présidents qui ont parlé de la Nation sont et celui qui la dis le plus de fois est :")
#     elif choix == '5':
#         print("Le premier président qui a parlé d'écologie est :")
#     elif choix == '6':
#         print("Les mots que tous les présidents ont évoqués sont :")
#     else:
#         print("le chiffre n'est pas valide")



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
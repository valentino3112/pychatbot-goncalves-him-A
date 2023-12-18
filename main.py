#matrice_score_tf_idf -> MATRICE/VECTEUR TF-IDF DU CORPUS
#matrice_score_tf_idf_question -> MATRICE/VECTEUR TF-IDF DE LA QUESTION
import os
import math


#Fonction qui permet de renvoyer une liste contenant le nom des fichiers et son extension choisi
def list_of_files(directory, extension): #on prends une entrée (directory) ainsi que l'extension d'un fichier (extension)
    files_names = []

    for filename in os.listdir(directory): #boucle qui recommence dans tous les fichiers présent dans le répertoire choisi
        if filename.endswith(extension): #verifie si le nom du fichier se finit par la même extension
            files_names.append(filename) #si oui, il l'ajoute au fichier "files_names"

    return files_names

print(list_of_files("cleaned", "txt"))

#On récupère le nom du président et nous retourne le resultat
def extraire_nom_president(nom: str):
    result = nom[11:-4].rstrip("1234567890").replace(" ","_") #on prends le nom qui se trouve à l'indice 11 jusqu'à l'indice -4 en supprimant les chiffres allant de 0 à 9

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
            contents = f.read().casefold().replace(".","").replace(",","").replace("!", "").replace("'"," ").replace("-", " ").replace("`","").replace("\"","").replace("\n", " ").replace(";", "").replace(":", "").replace("?", "").replace("   ", " ").replace("  ", " ")#On remplace les lettres majuscules par des minuscules, on supprime les ".",",","!",";",":","?" et on remplace les "'","-" par des espaces
        with open('cleaned/' + txt, 'w') as f: #on ouvre un noveau fichier en mode ecriture
            f.write(contents) #Toutes les modifications apportées vont être dans le fichiers "cleaned"

def everywordonce(corpus): #tout les mot du corpus seulement 1 seul fois
    words = []
    result = []

    for i in corpus:
        for j in i.split():
            if j not in words:
                result.append(j)
            words.append(j)

    return result

#Fonction qui calcule le TF de chaque mot dans les discors des présidents
def tf(texte: str):
    corpus = []

    for nom in list_of_files("cleaned","txt"): # On parcourt les fichier qui sont dans le répertoire "cleaned"
        with open("cleaned/"+nom) as f: # On ouvre chaque fichier du corpus
            corpus.append(f.read())

    everyword = everywordonce(corpus) #On appelle la fonction everywordonce qui nous donne tous les mots de tous le corpus en un seul exemplaire
    liste_mots = texte.split()
    result = {}
    words = []
    occurence = 0

    for mot in everyword: #On parcourt tous les mots
        occurence = 0

        for mot_dans_doc in liste_mots: #On parcourt cette fois ci chaque mot dans un texte
            if mot == mot_dans_doc:
                occurence = occurence + 1 #Si on retrouve le même on ajoute 1 pour connaitre le nombre de fois que le mot apparait

        if mot not in words: #Si le mot n'as pas été ajoute dans la liste alors :
            result[mot] = occurence / len(liste_mots) #On calcule son TF en divisant son notre d'occurence par le nombre de mots dans liste_mots
        words.append(mot) #Puis on l'ajoute a la liste words

    return result

#Fonction qui calcule l'IDF de chaque mot dans les textes des présidents
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

    for tfdoc in tf_du_corpus: #On parcourt le TF document par document du corpus
        for mot in tfdoc: #Puis on parcourt tous les mots dans le TF du document
            occurence = 0
            for texte in corpus:
                if mot in texte:
                    occurence = occurence + 1  #si le mot apparait dans un des texte du corpus on fait +1
            if mot not in mots_parcouru: #pour eviter doublons
                idf[mot] = math.log10(len(corpus) / occurence) #On calcule l'IDF en utilisant le log10
            mots_parcouru.append(mot) #Puis on l'ajoute a la liste mots_parcouru

    return idf
#On va maintenant calcule le score TF-IDF
def score_tfidf(repertoire):
    corpus = []

    for nom in list_of_files(repertoire, "txt"):
        with open(repertoire + "/" + nom) as f:
            corpus.append(f.read())

    tf_du_corpus = []

    for txt in corpus:
        tf_du_corpus.append(tf(txt)) #On calcule le TF de chaque document dans le corpus avec la fonction TF

    idf_corpus = idf(repertoire) #On calcule les valeurs IDF pour le corpus  avec la fonction IDF

    matrice = [[0 for k in range(len(idf_corpus))] for i in range(len(corpus))] #On initialise une matrice de dimension "nombre de document" et "nombre de mots dans le corpus

    for i, v in zip(range(len(idf_corpus)), idf_corpus):        #chaque ligne correspond à un mot
        for j in range(len(tf_du_corpus)):                      #chaque colonnes correspond à un doc
            matrice[j][i] = idf_corpus[v]*tf_du_corpus[j][v]    #idf*tf

    return matrice




#prenoms = ["Jacques", "Valéry", "François", "Emmanuel", "François", "Nicolas"]
prenoms = ["Valéry", "Emmanuel", "François", "Nicolas", "Jacques", "François"]
liste_nom_pres = liste_des_pres()
#liste_nom_pres.sort()


liste_pres = fullname_liste_pres()
print(liste_pres)

clean_text()
idf_corpus = idf("cleaned")
#print(len(idf_corpus))
matrice_score_tf_idf =  score_tfidf("cleaned")
#print(len(matrice_score_tf_idf))
print("chargement....")

#-----mot moins important-----
mots_moins_important = []
for i,k in zip(matrice_score_tf_idf, idf_corpus):
    if i == [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]: #On prend tous les mots qui possède un TF-IDF dans chaque document de 0.0
        mots_moins_important.append(k)

#----------------------------

#----mots_plus_important-----
mots_plus_important = []
somme_tfidf = {}
for i,k in zip(matrice_score_tf_idf, idf_corpus): #On parcourt deux matrice en meme temps
    somme_tfidf[k] = sum(i) #On fait la somme des valeurs TF-IDF pour chaque mot qu'on met dans un dictionnaire

somme_tfidf_decroissant = sorted(somme_tfidf.items(), key=lambda x:x[1])[::-1] #On va trier en ordonnant les éléments du dictionnaire par valeur


#----------------------------

#----mots_plus_répété_par_x-----
mots_plus_répété_par_x = []
discours_de_x = []
tf_du_discours_de_x = {}
for nom in list_of_files("cleaned", "txt"):
    if "Chirac" in nom:
        with open("cleaned/" + nom) as f: #On ouvre les document qui ont le mot "Chirac" dans leur titre
            discours_de_x.append(f.read())

tf_du_discours_de_x = tf(' '.join(discours_de_x)) #On calcule le tf des mots des discours de Chirac
tf_decroissant = sorted(tf_du_discours_de_x.items(), key=lambda x:x[1])[::-1] #Puis on tri en fonction de leur fréquence

#----------------------------

#----nom_des_pres_qui_parle_de_x-----
tout_les_discours = {}
for nom in list_of_files("cleaned", "txt"):
    tout_les_discours[extraire_nom_president(nom)] = [] #On utiluse une fonction pour prendre le nom du président grâce au nom du fichier et on le met en clé

for nom in list_of_files("cleaned", "txt"):
    with open("cleaned/" + nom) as f:
        tout_les_discours[extraire_nom_president(nom)].append(f.read())

pres_qui_parle_de_nation = {}
for i in tout_les_discours:
    pres_qui_parle_de_nation[i] = 0
    for j in tout_les_discours[i]: #on parcourt les discours pour le président 'i'
        if tf(j)["nation"] != 0.0: #Si le tf de nation est différent de 0 dans le discours alors
            pres_qui_parle_de_nation[i] = pres_qui_parle_de_nation[i] + tf(j)["nation"] #On incrémente la fréquence du mot Nation dans le discours
            #print((i,tf(j)["nation"]))

#----------------------------

#----premier_president_qui_parle-----
pres_qui_parle_de_eco = {}
for i in tout_les_discours:
    pres_qui_parle_de_eco[i] = 0
    for j in tout_les_discours[i]:
        if "climat" in j or "écolo" in j: #Si le mot "climat" ou "écolo" sont dans le discours alors
            pres_qui_parle_de_eco[i] = pres_qui_parle_de_eco[i] + 1 #On incrémente le compteur du présient 'i'


#----------------------------

#----mot_que_tout_pres_ont_évoqué-----
THECORPUS = []
for nom in list_of_files("cleaned", "txt"):
    with open("cleaned/" + nom) as f:
        THECORPUS.append(f.read())

CORPUSDICT = everywordonce(THECORPUS) #On crée un dictionnaire avec tous les mots du corpus

mot_que_pres_ont_dit = {}

for i in CORPUSDICT:
    mot_que_pres_ont_dit[i] = []

    for j in tout_les_discours:
        for k in tout_les_discours[j]:
            if i in k and idf_corpus[i] != 0.0: #on vérifie sir le mot 'i' est présent dans les discours et si son IDF est non nul
                #print(j,"le dit")
                mot_que_pres_ont_dit[i].append(j)
                break

mot_dit_par_tout_president_mais_pas_non_important = []

for i in mot_que_pres_ont_dit:
    if len(mot_que_pres_ont_dit[i]) == 6: #On vérifie si mot a été par les présidents (donc 6)
        mot_dit_par_tout_president_mais_pas_non_important.append(i)

#----------------------------
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
#         print(mots_moins_important)
#
#     elif choix == '2':
#         print("Les mots les plus importants sont :")
#         print(somme_tfidf_decroissant)
#
#     elif choix == '3':
#         print("Les mots les plus répétés de Chirac sont :")
#         print(tf_decroissant)
#
#     elif choix == '4':
#         print("Les noms des présidents qui ont parlé de la Nation sont:")
#         for i in pres_qui_parle_de_nation:
#             if pres_qui_parle_de_nation[i] != 0:
#                 print(i, end=" ")
#         print("\net celui qui la dis le plus de fois est :", end="")
#         print(max(pres_qui_parle_de_nation, key=pres_qui_parle_de_nation.get))
#
#     elif choix == '5':
#         print("Presidents qui parlent de ecologie et/ou climat:")
#         for i in pres_qui_parle_de_eco:
#             if pres_qui_parle_de_eco[i] != 0:
#                 print(i, end=" ")
#         print("\nPresident qui parle le plus d'ecologie et/ou climat est: ", end="")
#         print(max(pres_qui_parle_de_eco, key=pres_qui_parle_de_eco.get))
#
#     elif choix == '6':
#         print("Les mots que tous les présidents ont évoqués sont :")
#         print(mot_dit_par_tout_president_mais_pas_non_important)
#
#     else:
#         print("le chiffre n'est pas valide")


def clean_question():
    question = input("Veuillez saisir une question :")

    question = "".join(chr(ord(c) + 32) if 65 <= ord(c) <= 90 else c for c in question) # on remplace les majuscules par des minuscules en utilisant la valeur ASCII
    punctuations = [".", ",", "!", "'", "-", "`", "\"", "\n", "?", ":", ";"] # on enleve les ponctuations

    for punctuation in punctuations:
        question = question.replace(punctuation, " ")

    while "  " in question: # on enleve les espaces multiples
        question = question.replace("  ", " ")

    question = question.strip() # on supprime les espaces au début et à la fin de la chaîne
    separation_mot = question.split()# on sépare les mots et on les place dans une liste

    return separation_mot

def mot_question_corpus(question):
    mot_commun = []
    for i in question:
        if i in CORPUSDICT:
            if i in mot_commun :
                print(i, "est déjà dans le corpus")
            else :
                mot_commun.append(i)
    return mot_commun
#print(mot_question_corpus(CORPUSDICT))

#Fonction qui calcule le TF-IDF de la question posé par l'utilisateur
def tfidf_question(question_cleaned):
    matrice = []

    mot_question_et_corpus = mot_question_corpus(question_cleaned)

    tf_question = {}
    for i in question_cleaned:
        occurence = 0
        for j in question_cleaned:
            if i == j:
                occurence += 1 #On compte de nombre de fois que le mot 'i' apparait dans la question et on l'incrémente
        if i in mot_question_et_corpus:
            tf_question[i] = occurence/len(question_cleaned) #On calcule son TF

    for i in CORPUSDICT: #On prend les mots qui ne sont pas dans la question et on les ajoute dans le dictionnaire
        if not i in tf_question:
            tf_question[i] = 0.0 #On mets leur TF égal à 0.0
        else:
            print(i)

    print(tf_question)

    matrice = [[0] for i in range(len(idf_corpus))]

    for i, v in zip(range(len(idf_corpus)), idf_corpus):
        #if v == 'ceci':
        #    print("tf:",tf_question[v], "idf:", idf_corpus[v], "tfidf:", tf_question[v]*idf_corpus[v])
        matrice[i][0] = tf_question[v]*idf_corpus[v] #On calcule et on donne un TF-IDF a chaque mot dans la matrice
    return matrice

#fonction qui calcule le produit scalaire de deux vecteurs
def produit_scalaire(a, b):
    assert(len(a) == len(b))
    res = sum(i * j for i,j in zip(a, b))
    return res

#fonction qui calcule la longueur d'un vecteurs
def norme_vecteur(a):
    return math.sqrt(sum(i**2 for i in a))  #sqrt(x² + y²)

#fonction qui calcule la similarité cosinus de deux vecteurs
def similarite_cosinus(a, b):
    return (produit_scalaire(a,b))/(norme_vecteur(a)*norme_vecteur(b))




testquest = clean_question()
print(testquest)
matrice_score_tf_idf_question = tfidf_question(testquest)
print(len(matrice_score_tf_idf_question))

#print(matrice_score_tf_idf)

#fonction qui calcule le document le plus pertinent grâce a la similarité cosinus
def document_le_plus_pertinent(tfidf_du_corpus, tfidf_de_la_question, liste_des_fichiers):
    #transforme matrice tf idf de la question en vecteur
    temp = []
    for i in tfidf_de_la_question:
        for j in i:
            temp.append(j)
    #------------------------------------------------------
    similarite = []
    for i in tfidf_du_corpus:
        similarite.append(similarite_cosinus(i, temp))
    # normalement len(similarite) == 8 et numéro le plus haut veux dire similarité plus haute avec doc correspondant

    #recup du document le plus similaire
    max = 0.0
    for i in similarite:
        if i >= max:
            max = i
    return liste_des_fichiers[similarite.index(max)]


print(document_le_plus_pertinent(matrice_score_tf_idf, matrice_score_tf_idf_question, list_of_files("speeches", "txt")))

temp = []
for i in matrice_score_tf_idf_question:
    for j in i:
        temp.append(j)

print(list(idf_corpus)[temp.index(max(temp))]) #les dictionnaires conservent l'ordre, ici on cherche tf-idf le plus élevé de la question et on retourne le mot

DA_word = list(idf_corpus)[temp.index(max(temp))]

ptexter = ""
with open("speeches/"+document_le_plus_pertinent(matrice_score_tf_idf, matrice_score_tf_idf_question, list_of_files("speeches", "txt")), "r") as f:
    ptexter = f.read()


for i in ptexter.split("."):
    if DA_word in i:
        print(i)
        break


question_starters = {
    "Comment": "Après analyse, ",
    "Pourquoi": "Car, ",
    "Peux-tu": "Oui, bien sûr!"
}
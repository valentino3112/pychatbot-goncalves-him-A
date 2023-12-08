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
            contents = f.read().casefold().replace(".","").replace(",","").replace("!", "").replace("'"," ").replace("-", " ").replace("`","").replace("\"","").replace("\n", " ").replace("   ", " ").replace("  ", " ") #On remplace les lettres majuscules par des minuscules, on supprime les ".",",","!" et on remplace les "'","-" par des espaces
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
#print(liste_pres)

clean_text()
idf_corpus = idf("cleaned")
#print(len(idf_corpus))
matrice_score_tf_idf =  score_tfidf("cleaned")
#print(len(matrice_score_tf_idf))
print("chargement....")

#-----mot moins important-----
mots_moins_important = []
for i,k in zip(matrice_score_tf_idf, idf_corpus):
    if i == [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]:
        mots_moins_important.append(k)

#----------------------------

#----mots_plus_important-----
mots_plus_important = []
somme_tfidf = {}
for i,k in zip(matrice_score_tf_idf, idf_corpus):
    somme_tfidf[k] = sum(i)

somme_tfidf_decroissant = sorted(somme_tfidf.items(), key=lambda x:x[1])[::-1]


#----------------------------

#----mots_plus_répété_par_x-----
mots_plus_répété_par_x = []
discours_de_x = []
tf_du_discours_de_x = {}
for nom in list_of_files("cleaned", "txt"):
    if "Chirac" in nom:
        with open("cleaned/" + nom) as f:
            discours_de_x.append(f.read())

tf_du_discours_de_x = tf(' '.join(discours_de_x))
tf_decroissant = sorted(tf_du_discours_de_x.items(), key=lambda x:x[1])[::-1]

#----------------------------

#----nom_des_pres_qui_parle_de_x-----
tout_les_discours = {}
for nom in list_of_files("cleaned", "txt"):
    tout_les_discours[extraire_nom_president(nom)] = []

for nom in list_of_files("cleaned", "txt"):
    with open("cleaned/" + nom) as f:
        tout_les_discours[extraire_nom_president(nom)].append(f.read())

pres_qui_parle_de_nation = {}
for i in tout_les_discours:
    pres_qui_parle_de_nation[i] = 0
    for j in tout_les_discours[i]:
        if tf(j)["nation"] != 0.0:
            pres_qui_parle_de_nation[i] = pres_qui_parle_de_nation[i] + tf(j)["nation"]
            #print((i,tf(j)["nation"]))

#----------------------------

#----premier_president_qui_parle-----
pres_qui_parle_de_eco = {}
for i in tout_les_discours:
    pres_qui_parle_de_eco[i] = 0
    for j in tout_les_discours[i]:
        if "climat" in j or "écolo" in j:
            pres_qui_parle_de_eco[i] = pres_qui_parle_de_eco[i] + 1


#----------------------------

#----mot_que_tout_pres_ont_évoqué-----
THECORPUS = []
for nom in list_of_files("cleaned", "txt"):
    with open("cleaned/" + nom) as f:
        THECORPUS.append(f.read())

CORPUSDICT = everywordonce(THECORPUS)

mot_que_pres_ont_dit = {}

for i in CORPUSDICT:
    mot_que_pres_ont_dit[i] = []
    for j in tout_les_discours:
        for k in tout_les_discours[j]:
            if i in k and idf_corpus[i] != 0.0:
                #print(j,"le dit")
                mot_que_pres_ont_dit[i].append(j)
                break

mot_dit_par_tout_president_mais_pas_non_important = []

for i in mot_que_pres_ont_dit:
    if len(mot_que_pres_ont_dit[i]) == 6:
        mot_dit_par_tout_president_mais_pas_non_important.append(i)

#----------------------------
# print(len(score_tfidf("cleaned")))
#
# for i in score_tfidf("cleaned"):
#     print(i)



while True:
    print("\nMenu :")
    print("1. Afficher les mots les moins importants")
    print("2. Afficher les mots ayant le score TF-IDF le plus élevé")
    print("3. Indiquer les mots les plus répétés par le président Chirac")
    print("4. Indiquer le président ayant le plus parlé de la 'Nation' et le nombre de répétitions")
    print("5. Indiquer le premier président à parler du climat ou de l'écologie")
    print("6. Trouver les mots évoqués par tous les présidents")


    choix = input("Choisissez une option : ")

    if choix == '1':
        print("Les mots les moins importants sont :")
        print(mots_moins_important)

    elif choix == '2':
        print("Les mots les plus importants sont :")
        print(somme_tfidf_decroissant)

    elif choix == '3':
        print("Les mots les plus répétés de Chirac sont :")
        print(tf_decroissant)

    elif choix == '4':
        print("Les noms des présidents qui ont parlé de la Nation sont:")
        for i in pres_qui_parle_de_nation:
            if pres_qui_parle_de_nation[i] != 0:
                print(i, end=" ")
        print("\net celui qui la dis le plus de fois est :", end="")
        print(max(pres_qui_parle_de_nation, key=pres_qui_parle_de_nation.get))

    elif choix == '5':
        print("Presidents qui parlent de ecologie et/ou climat:")
        for i in pres_qui_parle_de_eco:
            if pres_qui_parle_de_eco[i] != 0:
                print(i, end=" ")
        print("\nPresident qui parle le plus d'ecologie et/ou climat est: ", end="")
        print(max(pres_qui_parle_de_eco, key=pres_qui_parle_de_eco.get))

    elif choix == '6':
        print("Les mots que tous les présidents ont évoqués sont :")
        print(mot_dit_par_tout_president_mais_pas_non_important)

    else:
        print("le chiffre n'est pas valide")


def clean_question():
    question = input("Veuillez saisir une question :")

    question = "".join(chr(ord(c) + 32) if 65 <= ord(c) <= 90 else c for c in question) # on remplace les majuscules par des minuscules en utilisant la valeur ASCII
    punctuations = [".", ",", "!", "'", "-", "`", "\"", "\n"] # on enleve les ponctuations

    for punctuation in punctuations:
        question = question.replace(punctuation, " ")

    while "  " in question: # on enleve les espaces multiples
        question = question.replace("  ", " ")

    question = question.strip() # on supprime les espaces au début et à la fin de la chaîne
    separation_mot = question.split()# on sépare les mots et on les place dans une liste

    return separation_mot

def mot_question_corpus :
    for filename in os.listdir("cleaned"): # on parcourt les fichiers du dossier "cleaned"
        mot_garde = []
        file_content = ""   # Lecture du contenu de chaque fichier

        with open(os.path.join("cleaned", filename), "r") as file:
            for line in file:
                file_content += line

        for mot in separation_mot:  # on verifie les mots similaires entre la question et le contenu du fichier
            if mot in file_words and mot not in mots_garde:
                mots_garde.append(mot)

    return mots_garde
def vecteur_tfidf_question(repertoire: str, mot_garde: list): # Fonction pour calculer le vecteur TF-IDF de la question
    scores_idf = idf(repertoire) # on appelle les fonctions scores IDF et la matrice TF-IDF du corpus
    matrice_tfidf = score_tfidf(repertoire)

    vecteur_tf_question = [0] * len(matrice_tfidf[0]) # on initalise d'un vecteur TF pour la question

    for mot in mot_garde: # on calcule du score TF pour chaque mot de la question
        if mot in matrice_tfidf[1]: # on vérifie si le mot de la question est présent dans la matrice TF-IDF du corpus
            indice_mot = matrice_tfidf[1].index(mot) # on obtenient l'indice du mot dans la matrice TF-IDF
            tf_mot = mot_garde.count(mot) / len(mot_garde) # on calcule le TF pour le mot dans la question
            tfidf_mot = tf_mot * scores_idf[indice_mot] # on calcule du TF-IDF pour le mot dans la question en utilisant le score IDF du corpus
            vecteur_tf_question[indice_mot] = tfidf_mot # on donne le score TF-IDF au vecteur TF-IDF de la question

    return vecteur_tf_question




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
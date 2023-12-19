import math
import os



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
def fullname_liste_pres(prenoms,liste_nom_pres):
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

    for nom in list_of_files("cleaned", "txt"): # On parcourt les fichier qui sont dans le répertoire "cleaned"
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

    for nom in list_of_files(repertoire, "txt"):
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

#On va maintenant calculer le score TF-IDF
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


def mot_question_corpus(question, CORPUSDICT):
    mot_commun = []
    for i in question:
        if i in CORPUSDICT:
            if i in mot_commun :
                print(i, "est déjà dans le corpus")
            else :
                mot_commun.append(i)
    return mot_commun


#Fonction qui calcule le TF-IDF de la question posé par l'utilisateur
def tfidf_question(question_cleaned, CORPUSDICT, idf_corpus):
    matrice = []

    mot_question_et_corpus = mot_question_corpus(question_cleaned, CORPUSDICT)

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

#fonction qui calcule la longueur d'un vecteur
def norme_vecteur(a):
    return math.sqrt(sum(i**2 for i in a))  #sqrt(x² + y²)


#fonction qui calcule la similarité cosinus de deux vecteurs
def similarite_cosinus(a, b):
    try:
        return (produit_scalaire(a,b))/(norme_vecteur(a)*norme_vecteur(b))
    except:
        return "Erreur division par 0"


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
        if similarite_cosinus(i, temp) != "Erreur division par 0":
            similarite.append(similarite_cosinus(i, temp))
        else:
            print("Le chatbot comprends pas votre question!")
            exit()
    # normalement len(similarite) == 8 et numéro le plus haut veux dire similarité plus haute avec doc correspondant

    #recup du document le plus similaire
    max = 0.0
    for i in similarite:
        if i >= max:
            max = i
    return liste_des_fichiers[similarite.index(max)]

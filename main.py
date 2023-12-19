#matrice_score_tf_idf -> MATRICE/VECTEUR TF-IDF DU CORPUS
#matrice_score_tf_idf_question -> MATRICE/VECTEUR TF-IDF DE LA QUESTION

from functions import list_of_files, extraire_nom_president, liste_des_pres, fullname_liste_pres, clean_text, \
    everywordonce, tf, idf, score_tfidf, clean_question, tfidf_question, document_le_plus_pertinent



prenoms = ["Valéry", "Emmanuel", "François", "Nicolas", "Jacques", "François"] #ordre arbitraire de list_of_files
liste_nom_pres = liste_des_pres()
liste_pres = fullname_liste_pres(prenoms,liste_nom_pres)

clean_text()

idf_corpus = idf("cleaned")
matrice_score_tf_idf =  score_tfidf("cleaned")

print("chargement....")

#-----mot moins important-----
mots_moins_important = []
for i,k in zip(matrice_score_tf_idf, idf_corpus):
    if i == [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]: #On prend tous les mots qui possède un TF-IDF dans chaque document de 0.0
        mots_moins_important.append(k)
#----------------------------

#----mots_plus_important-----
mot_plus_important = []
somme_tfidf = {}
for i,k in zip(matrice_score_tf_idf, idf_corpus): #On parcourt deux matrice en meme temps
    somme_tfidf[k] = sum(i) #On fait la somme des valeurs TF-IDF pour chaque mot qu'on met dans un dictionnaire

# somme_tfidf_decroissant = sorted(somme_tfidf.items(), key=lambda x:x[1])[::-1]
# print(somme_tfidf)
# print(somme_tfidf_decroissant)

#compréhensions de liste python:
#mettre i quand on parcours somme_tfidf et que on remarque que v == au max des valeurs de somme_tfidf

mot_plus_important = [i for i,v in somme_tfidf.items() if v == max(somme_tfidf.values())]

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

#tf_decroissant = sorted(tf_du_discours_de_x.items(), key=lambda x:x[1])[::-1] #Puis on tri en fonction de leur fréquence
#print(tf_decroissant)

mots_plus_répété_par_x = [i for i,v in tf_du_discours_de_x.items() if v == max(tf_du_discours_de_x.values())]

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



while True:
    print("\nMenu :")
    print("1. Afficher les mots les moins importants")
    print("2. Afficher les mots ayant le score TF-IDF le plus élevé")
    print("3. Indiquer les mots les plus répétés par le président Chirac")
    print("4. Indiquer le président ayant le plus parlé de la 'Nation' et le nombre de répétitions")
    print("5. Indiquer le premier président à parler du climat ou de l'écologie")
    print("6. Trouver les mots évoqués par tous les présidents")
    print("7. Poser une question au chatbot")


    choix = input("Choisissez une option : ")

    if choix == '1':
        print("Les mots les moins importants sont :")
        print(mots_moins_important)

    elif choix == '2':
        print("Les mots les plus importants sont :")
        print(mot_plus_important)

    elif choix == '3':
        print("Les mots les plus répétés de Chirac sont :")
        print(mots_plus_répété_par_x)

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

    elif choix == '7':
        break

    else:
        print("le chiffre n'est pas valide")




LA_QUESTION = clean_question()

matrice_score_tf_idf_question = tfidf_question(LA_QUESTION, CORPUSDICT, idf_corpus)

#convertir la matrice de (1681,1) en liste de taille 1681
temp = []
for i in matrice_score_tf_idf_question:
    for j in i:
        temp.append(j)


Mot_Question_Avec_IDF_haut = list(idf_corpus)[temp.index(max(temp))] #les dictionnaires conservent l'ordre, ici on cherche tf-idf le plus élevé de la question et on retourne le mot

text_du_doc_le_plus_pertinent = ""
with open("speeches/" + document_le_plus_pertinent(matrice_score_tf_idf, matrice_score_tf_idf_question, list_of_files("speeches", "txt")), "r") as f:
    text_du_doc_le_plus_pertinent = f.read()

Reponse_Du_ChatBOT = ""
for i in text_du_doc_le_plus_pertinent.split("."):
    if Mot_Question_Avec_IDF_haut in i or Mot_Question_Avec_IDF_haut in i.casefold(): #fix pour nation et tt
        Reponse_Du_ChatBOT = i
        break


question_starters = {
    "comment": "Après analyse, ",
    "pourquoi": "Car, ",
    "peux-tu": "Oui, bien sûr!"
}

for i in LA_QUESTION:
    if i in question_starters:
        Reponse_Du_ChatBOT = question_starters[i] + Reponse_Du_ChatBOT
        break #éviter "Après analyse, Car,"

print(Reponse_Du_ChatBOT.replace("\n",""))

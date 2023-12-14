# -*- coding: utf-8 -*-

import psycopg2


def affichageSelect(colonnes:tuple, result:tuple):

    len_colonnes = [max(len(colonnes[i]), max((len(str(result[j][i])) for j in range(len(result))))) for i in range(len(colonnes))]
    print(len_colonnes)


    print(f" {'Ligne':{max(5, len(str(len(result))))}s} |" ,end="")
    for i in range(len(colonnes)):
        print(f" {colonnes[i]:{len_colonnes[i]}s} |" ,end="")
    print("\n")

    for j in range(len(result)):
        print(f" {str(j):{max(5, len(str(len(result))))}s} |" ,end="")
        for i in range(len(result[j])):
            print(f" {str(result[j][i]):{len_colonnes[i]}s} |" ,end="")
        print("\n")

def afficherDossierMedical(dossier, cur):
    #On récupère le nom de l'animal associé au Dossier
    cur.execute('''SELECT nom FROM Animal
    WHERE Animal.idAnimal = %d''', (dossier[9],))
    nomAnimal = cur.fetchone()

    #il faut trouver le vétérinaire prescripteur pour l'afficher
    cur.execute('''SELECT nom FROM Veterinaire V
                WHERE V.idVet = %d''', (dossier[8],))
    nomVet = cur.fetchone()

    print(f'''
    --------------------
    Dossier {dossier[0]} :
    \tDate de saisie : {dossier[7]}
    \tNom de l'animal : {nomAnimal}\n
    \tMesure de la taille : {dossier[1]}\n
    \tMesure du poids : {dossier[2]}\n
    \tDébut du traitement: {dossier[3]}\n
    \tDurée du traitement: {dossier[4]}\n
    \tObservation générale:\n
    \t\t{dossier[5]}\n
    \tDescription Procédure :\n
    \t\t{dossier[6]}\n
    \tVétérinaire Prescripteur : {nomVet}
    --------------------
    ''')


def connexionUtilisateur(cur) :
    succes = False
    while(succes != True):
        print("---Connexion Utilisateur---")
        username = input("Nom d'utilisateur : ")
        password = input("Mot de passe : ")
        cur.execute(
        "SELECT idUser, type FROM Users WHERE login = %s AND motDePasse = %s",
        (username, password)
        )
        res = cur.fetchone()
        succes = (res[1] in ["client","veterinaire","assistant"])
    return res

def connexionAdministrateur(cur) :
    succes = False
    while(succes != True):
        print("---Connexion Administrateur---")
        username = input("Nom d'utilisateur : ")
        password = input("Mot de passe : ")
        cur.execute(
        "SELECT COUNT(*) FROM Admins WHERE login = %s AND motDePasse = %s",
        (username, password)
        )
        res = cur.fetchone()
        succes = (res != 0)
    return succes

def afficherInfosAnimal(cur, idUtilisateur, typeUtilisateur):
    #affichage client
    if (typeUtilisateur == "client"):
        #Le client n'a le choix de regarder les informations que de ses animaux
        cur.execute('''SELECT A.idAnimal, A.nom, A.numPuceId, A.numPasseport, A.taille, E.typeEspece, E.intitulePrecis
        FROM Animal A
        JOIN EstPossedePar EPP ON EPP.animal = A.idAnimal
        JOIN Espece E ON A.espece = E.idEspece
        WHERE EPP.client = %s''', (idUtilisateur,))
        animaux = cur.fetchall()
        if (len(animaux) == 0) :
            print("Vous ne possédez aucun animal")
            return
        if (len(animaux) == 1) :
            animalChoisi = animaux[0]
        else :
            #Si le client possède plusieurs animaux, alors on lui demande d'en choisir un
            colonnes  = ("idAnimal", "nom", "numPuceId", "numPasseport", "taille", "type espece", "intitulé précis")
            affichageSelect(colonnes, animaux)
            numAnimalChoisi = int(input("Entrez le numéro de la ligne de l'animal choisi :"))
            animalChoisi=animaux[numAnimalChoisi]


    #Affichage Personnel
    else :
        #On propose au personnel de rechercher un animal soit par nom, soit par id.
        choixTypeRecherche = -1
        while(choixTypeRecherche != 1 and choixTypeRecherche != 2):
            choixTypeRecherche = int(input("Rechercher un animal par :\n1) Nom\n2) Id\n"))
        if (choixTypeRecherche == 1):
            #On demande le nom de l'animal
            nomAnimal = input("Entrez le nom de l'animal : ")
            cur.execute('''SELECT A.idAnimal, A.nom, A.numPuceId, A.numPasseport, A.taille, E.typeEspece, E.intitulePrecis
            FROM Animal A
            JOIN Espece E ON A.espece = E.idEspece
            WHERE A.nom = %s''', (nomAnimal,))
            animaux = cur.fetchall()
            if (len(animaux) == 0) :
                print("Aucun animal ne correspond à ce nom")
                return
            if (len(animaux) == 1) :
                animalChoisi = animaux[0]
            else :
                #Si Plusieurs animaux ont le même nom, on demande au personnel de choisir
                colonnes  = ("idAnimal", "nom", "numPuceId", "numPasseport", "taille", "type espèce", "intitulé précis")
                affichageSelect(colonnes, animaux)
                numAnimalChoisi = int(input("Entrez le numéro de la ligne de l'animal choisi :"))
                animalChoisi=animaux[numAnimalChoisi]
        else :
            #On demande l'id de l'animal
            idAnimal = int(input("Entrez l'id de l'animal : "))
            cur.execute('''SELECT A.id, A.nom, A.numPuceId, A.numPasseport, A.taille, E.typeEspece, E.intitulePrecis
            FROM Animal A
            JOIN Espece E ON A.espece = E.idEspece
            WHERE A.idAnimal = %s''', (idAnimal,))
            animalChoisi = cur.fetchone()

    #À ce stade on connait l'animal dont on doit afficher les dossier médicaux, dans animalChoisi
    #Affichons les :
    print(f"Dossiers médicaux de {animalChoisi[1]}: ")
    cur.execute('''SELECT dm.* FROM DossierMedical dm
    JOIN Animal a ON dm.animal = a.idAnimal
    WHERE a.idAnimal = %d
    ORDER BY saisie DESC''',(animalChoisi[0],))
    dossiersMedicaux = cur.fetchall()
    for dossier in dossiersMedicaux :
        afficherDossierMedical(dossier, cur)

def ajouterClient(cur) :
    print("Il faut créer un compte pour le client")
    username = input("Entrer le nom d'utilisateur du client")
    password = input("Entrer le mot de passe du client")
    succes = cur.execute('''
                INSERT INTO Users (idUser, login, motDePasse, type)
                VALUES (NULL, %s, %s, 'client') RETURNING idClient''',
                (username, password))
    if succes == None :
        return
    print(f"Création avec succès du compte client, id : {succes}" )
    nom = input("Entrer le nom du client : ")
    prenom = input("Entrer le prénom du client : ")
    dateNaissance = input("Entrer la date de naissance du client ( format YYYY-MM-DD): ")
    adresse = input("Entrer l'adresse du client : ")
    tel = input("Entrer le numéro de téléphone du client : ")
    #On tente d'insérer le client :
    succes = cur.execute('''
                INSERT INTO Client (idClient, nom, prenom, dateNaissance, adresse, tel)
                VALUES (NULL, %s, %s, %s, %s, %s) RETURNING idClient''',
                (nom, prenom, dateNaissance, adresse, tel))
    if (succes == None) :
        print("Echec de l'insertion, le client semble déjà exister")
    else :
        print("Client ajouté avec succès.")

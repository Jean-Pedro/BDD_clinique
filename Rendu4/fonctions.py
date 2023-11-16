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



def connexionUtilisateur(cur) :
    succes = false
    while(succes != true):
        print("---Connexion Utilisateur---")
        username = input("Nom d'utilisateur : ")
        password = input("Mot de passe : ")
        cur.execute(
        "SELECT id, type FROM Users WHERE username = %s AND password = %s",
        (username, password)
        )
        res = cur.fetchone()
        succes = (res[1] in ["client","veterinaire","assistant"])
    return res

def connexionAdministrateur(cur) :
    succes = false
    while(succes != true):
        print("---Connexion Administrateur---")
        username = input("Nom d'utilisateur : ")
        password = input("Mot de passe : ")
        cur.execute(
        "SELECT COUNT(*) FROM Admins WHERE username = %s AND password = %s",
        (username, password)
        )
        res = cur.fetchone()
        succes = (res != 0)
    return succes

def afficherInfosAnimal(cur, idUtilisateur, typeUtilisateur):
    #affichage client
    if (typeUtilisateur == "client"):
        cur.execute('''SELECT A.id, A.nom, A.numPuceId, A.numPasseport, A.taille, E.typeEspece, E.intitulePrecis
        FROM Animal A
        JOIN EstPossedePar EPP ON EPP.animal = A.idAnimal
        JOIN Espece E ON A.espece = E.idEspece
        WHERE EPP.client = %d''', (idUtilisateur,))
        animaux = cur.fetchall()
        if (len(animaux) == 0) :
            print("Vous ne possédez aucun animal")
            return
        if (len(animaux) == 1) :
            animalChoisi = animaux[0]
        else :
            #Si le client possède plusieurs animaux, alors on lui demande d'en choisir un
            colonnes  = ("idAnimal", "nom", "numPuceId", "numPasseport", "taille", "espece")
            affichageSelect(colonnes, animaux)
            numAnimalChoisi = int(input("Entrez le numéro de la ligne de l'animal choisi :"))
            animalChoisi=animaux[numAnimalChoisi]
        #À ce stade on connait l'animal dont on doit afficher le dossier médical, dans animalChoisi
        #Affichons son dossier médical
        print(f"Dossiers médicaux de {animalChoisi[1]}: ")
        cur.execute('''SELECT dm.* FROM DossierMedical dm
        JOIN Animal a ON dm.animal = a.idAnimal
        WHERE a.idAnimal = %d
        ORDER BY saisie DESC''',(animalChoisi[0],))
        dossierMedicaux = cur.fetchall()
        colonnes = ("idDossier", "mesureTaille", "mesurePoids", "debut traitement", "durée Traitement", "observation générale", "description Procédure", "Date Saisie", "animal=>", "veterinairePrescripteur=> NULL")

def afficherDossierMedical(dossier):
    #On récupère le nom de l'animal associé au Dossier
    cursor.execute('''SELECT nom FROM Animal
    WHERE Animal.idAnimal =''')
    print(
    f'''
    Dossier {idDossier} :
    \tanimal
    ''')

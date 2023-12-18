# -*- coding: utf-8 -*-

import psycopg2
import datetime

def id_suivant(cur, table:str, id:str):
    # Cette fonctin permet de récupérer le prochain id à utiliser pour une table donnée
    cur.execute("(SELECT MAX("+id+") FROM "+ table +")")
    last_id = cur.fetchone()
    if last_id == None:
        return 1
    return last_id[0]+1

def affichageSelect(colonnes:tuple, result:tuple):


    len_colonnes = [max(len(colonnes[i]), max((len(str(result[j][i])) for j in range(len(result))))) for i in range(len(colonnes))]
    #print(len_colonnes)


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
    WHERE Animal.idAnimal = %s''', (dossier[9],))
    nomAnimal = cur.fetchone()

    #il faut trouver le vétérinaire prescripteur pour l'afficher
    cur.execute('''SELECT nom FROM Veterinaire V
                WHERE V.idVet = %s''', (dossier[8],))
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
        #print(res)
        if (res) :
            succes = True
    return res

def connexionAdministrateur(cur) :
    succes = False
    while(succes != True):
        print("---Connexion Administrateur---")
        username = input("Nom d'utilisateur : ")
        password = input("Mot de passe : ")

        cur.execute(
        "SELECT idAdmin FROM Admin WHERE login = %s AND motDePasse = %s",
        (username, password)
        )
        #cur.execute("select idAdmin from Admin where login='admin' AND motDePasse='123'")
        # cur.execute(
        # "SELECT idUser, type FROM Users WHERE login = %s AND motDePasse = %s",
        # (username, password)
        # )
        res = cur.fetchone()
        #print("res :",res)
        #succes = True # en attendant de comprendre pourquoi ça renvoie none
        if (res) :
            succes = True        # (username, password)

    return True

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
        elif choixTypeRecherche == 2:
            #On demande l'id de l'animal
            idAnimal = int(input("Entrez l'id de l'animal : "))
            cur.execute('''SELECT A.idAnimal, A.nom, A.numPuceId, A.numPasseport, A.taille, E.typeEspece, E.intitulePrecis
            FROM Animal A
            JOIN Espece E ON A.espece = E.idEspece
            WHERE A.idAnimal = %s''', (idAnimal,))
            animalChoisi = cur.fetchone()

    #À ce stade on connait l'animal dont on doit afficher les dossier médicaux, dans animalChoisi
    #Affichons les :
    if(animalChoisi != None):
        print(f"Dossiers médicaux de {animalChoisi[1]}: ")
        cur.execute('''SELECT dm.* FROM DossierMedical dm
        JOIN Animal a ON dm.animal = a.idAnimal
        WHERE a.idAnimal = %s
        ORDER BY saisie DESC''',(animalChoisi[0],))
        dossiersMedicaux = cur.fetchall()
        for dossier in dossiersMedicaux :
            afficherDossierMedical(dossier, cur)
    else:
        print("Animal inexistant")

def ajouterUser(cur, conn, typeUtilisateur) :
    print(f"Il faut créer un compte pour le {typeUtilisateur}")
    username = input(f"Entrer le login du {typeUtilisateur} : ")
    password = input(f"Entrer le mot de passe du {typeUtilisateur} : ")
    id_user = id_suivant(cur, "Users", "idUser")
    #On tente d'insérer le client comme utilisateur
    try:
        cur.execute('''
                INSERT INTO Users (idUser, login, motDePasse, type)
                VALUES (%s, %s, %s, %s)''',
                (id_user, username, password, typeUtilisateur))
        print(f"Création avec succès du compte {typeUtilisateur}, id : {id_user}\n " )
        print("Veuillez desormais entrer ses informations : " )
    except psycopg2.errors:
        print("Attention, erreur lors de l'insertion ! Un utilisateur avec le meme nom existe peut etre.")
        return

    nom = input(f"Entrer le nom du {typeUtilisateur} : ")
    prenom = input(f"Entrer le prénom du {typeUtilisateur} : ")
    dateNaissance = input(f"Entrer la date de naissance du {typeUtilisateur} ( format YYYY-MM-DD): ")
    adresse = input(f"Entrer l'adresse du {typeUtilisateur} : ")
    tel = input(f"Entrer le numéro de téléphone du {typeUtilisateur} : ")

    if (typeUtilisateur == "veterinaire" or typeUtilisateur =="assistant"):
        print("Choix de la specialite : ")
        #gestion des espèces : on affiche celles qui existent déjà, si l'animal n'appartient à aucune d'elles, on propose à l'utilisateur de créer une nouvelle espèce
        cur.execute('''SELECT * FROM Espece''')
        res = cur.fetchall()
        #print(res)
        nombreEspecesTotal = len(res)
        colonnesEspeces = ["idEspece", "typeEspece", "intitulePrecis"]
        affichageSelect(colonnesEspeces, res)
        estDedans= ""
        idEspeceChoisie = -1
        while(estDedans != "oui" and estDedans!= "non") :
            estDedans = input("L'espèce d'animal qui est votre specialite apparaît-elle dans la liste ? (oui | non) : ")
        if (estDedans == "oui") :
            idEspeceChoisie = int(input("Entrez le numéro de ligne de l'espèce de votre animal : "))
            while (idEspeceChoisie < 0 or idEspeceChoisie > nombreEspecesTotal) :
                print("id choisi incorrect, réessayez.")
                idEspeceChoisie = int(input("Entrez le numéro de ligne de l'espèce de votre animal : "))
            idEspeceChoisie = res[idEspeceChoisie][0]
        else :
            #On doit créer une nouvelle espèce
            idEspeceChoisie = ajouterEspece(cur, conn)


    #On tente d'insérer le client :
    try:
        if (typeUtilisateur == "client"):
            cur.execute('''
                INSERT INTO Client (idClient, nom, prenom, dateNaissance, adresse, tel)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING idClient''',
                (id_user, nom, prenom, dateNaissance, adresse, tel))
        elif (typeUtilisateur == "assistant"):
            cur.execute('''
                INSERT INTO Assistant (idAssist, nom, prenom, dateNaissance, adresse, tel, specialite)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING idAssist''',
            (id_user, nom, prenom, dateNaissance, adresse, tel, idEspeceChoisie))
        elif (typeUtilisateur == "veterinaire"):
            cur.execute('''
                INSERT INTO Veterinaire (idVet, nom, prenom, dateNaissance, adresse, tel, specialite)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING idVet''',
                (id_user, nom, prenom, dateNaissance, adresse, tel, idEspeceChoisie))

        print(f"{typeUtilisateur} ajouté avec succès.")
    except psycopg2.errors:
        print(f"Echec de l'insertion, le {typeUtilisateur} pourrait déjà exister")
        return
    conn.commit()


def updateUser(cur, conn, typeUtilisateur):
    print(f"Voici tous les {typeUtilisateur}s : ")

    if (typeUtilisateur == 'client'):
        cur.execute('''SELECT * FROM Client''')
        colonnes = ('idClient', 'nom', 'prenom', 'dateNaissance', 'adresse', 'tel')
    elif (typeUtilisateur == 'assistant'):
        cur.execute('''SELECT * FROM Assistant''')
        colonnes = ('idClient', 'nom', 'prenom', 'dateNaissance', 'adresse', 'tel', 'specialite')
    else:
        cur.execute('''SELECT * FROM Veterinaire''')
        colonnes = ('idClient', 'nom', 'prenom', 'dateNaissance', 'adresse', 'tel', 'specialite')

    res = cur.fetchall()
    affichageSelect(colonnes, res)
    ligneUtilisateurChoisie = int(input(f"Entrez le numéro de ligne du {typeUtilisateur} a mettre a jour : "))
    idUtilisateurChoisie = res[ligneUtilisateurChoisie][0]


    nom = input(f"Entrer le nom du {typeUtilisateur} : ")
    prenom = input(f"Entrer le prénom du {typeUtilisateur} : ")
    dateNaissance = input(f"Entrer la date de naissance du {typeUtilisateur} ( format YYYY-MM-DD): ")
    adresse = input(f"Entrer l'adresse du {typeUtilisateur} : ")
    tel = input(f"Entrer le numéro de téléphone du {typeUtilisateur} : ")

    if (typeUtilisateur == "veterinaire" or typeUtilisateur =="assistant"):
        print("Choix de la specialite : ")
        #gestion des espèces : on affiche celles qui existent déjà, si l'animal n'appartient à aucune d'elles, on propose à l'utilisateur de créer une nouvelle espèce
        cur.execute('''SELECT * FROM Espece''')
        res = cur.fetchall()
        #print(res)
        nombreEspecesTotal = len(res)
        colonnesEspeces = ["idEspece", "typeEspece", "intitulePrecis"]
        affichageSelect(colonnesEspeces, res)
        estDedans= ""
        idEspeceChoisie = -1
        while(estDedans != "oui" and estDedans!= "non") :
            estDedans = input("L'espèce d'animal qui est votre specialite apparaît-elle dans la liste ? (oui | non) : ")
        if (estDedans == "oui") :
            idEspeceChoisie = int(input("Entrez le numéro de ligne de l'espèce de votre animal : "))
            while (idEspeceChoisie < 0 or idEspeceChoisie > nombreEspecesTotal) :
                print("id choisi incorrect, réessayez.")
                idEspeceChoisie = int(input("Entrez le numéro de ligne de l'espèce de votre animal : "))
            idEspeceChoisie = res[idEspeceChoisie][0]
        else :
            #On doit créer une nouvelle espèce
            idEspeceChoisie = ajouterEspece(cur, conn)


    #On tente de mettre à jour le client :
    try:
        if (typeUtilisateur == "client"):
            cur.execute('''
                UPDATE Client SET nom = %s, prenom = %s, dateNaissance = %s, adresse = %s, tel = %s WHERE idClient = %s''',
                (nom, prenom, dateNaissance, adresse, tel, idUtilisateurChoisie))
        elif (typeUtilisateur == "assistant"):
            cur.execute('''
                UPDATE Assistant SET nom = %s, prenom = %s, dateNaissance = %s, adresse = %s, tel = %s, specialite = %s WHERE idAssist = %s''',
                (nom, prenom, dateNaissance, adresse, tel, idEspeceChoisie, idUtilisateurChoisie))

        elif (typeUtilisateur == "veterinaire"):
            cur.execute('''
                UPDATE Veterinaire SET nom = %s, prenom = %s, dateNaissance = %s, adresse = %s, tel = %s, specialite = %s WHERE idVet = %s''',
                (nom, prenom, dateNaissance, adresse, tel, idEspeceChoisie, idUtilisateurChoisie))

        print(f"{typeUtilisateur} mis a jour avec succès.")
    except psycopg2.errors:
        print(f"Echec de l'update")
        return
    conn.commit()

def deleteUser(cur, conn, typeUtilisateur):
    print(f"Voici tous les {typeUtilisateur}s : ")

    if (typeUtilisateur == 'client'):
        cur.execute('''SELECT * FROM Client''')
        colonnes = ('idClient', 'nom', 'prenom', 'dateNaissance', 'adresse', 'tel')
    elif (typeUtilisateur == 'assistant'):
        cur.execute('''SELECT * FROM Assistant''')
        colonnes = ('idClient', 'nom', 'prenom', 'dateNaissance', 'adresse', 'tel', 'specialite')
    else:
        cur.execute('''SELECT * FROM Veterinaire''')
        colonnes = ('idClient', 'nom', 'prenom', 'dateNaissance', 'adresse', 'tel', 'specialite')

    res = cur.fetchall()
    affichageSelect(colonnes, res)
    ligneUtilisateurChoisie = int(input(f"Entrez le numéro de ligne du {typeUtilisateur} a supprimer : "))
    idUtilisateurChoisie = res[ligneUtilisateurChoisie][0]



    #On tente de supprimer le client et le user associé dans la table users :
    try:
        if (typeUtilisateur == "client"):
            cur.execute('''DELETE FROM Client WHERE idClient = %s''', (idUtilisateurChoisie))
            cur.execute('''DELETE FROM Users WHERE idClient = %s''', (idUtilisateurChoisie))

        elif (typeUtilisateur == "assistant"):
            cur.execute('''DELETE FROM Assistant WHERE idClient = %s''', (idUtilisateurChoisie))
            cur.execute('''DELETE FROM Users WHERE idClient = %s''', (idUtilisateurChoisie))

        elif (typeUtilisateur == "veterinaire"):
            cur.execute('''DELETE FROM Veterinaire WHERE idClient = %s''', (idUtilisateurChoisie))
            cur.execute('''DELETE FROM Users WHERE idClient = %s''', (idUtilisateurChoisie))

        print(f"{typeUtilisateur} mis a jour avec succès.")
    except psycopg2.errors:
        print(f"Echec de l'update")
        return
    conn.commit()


def ajoutMedicament(cur, conn) :
    print(f" Veuillez entrer les informations du medicament ")
    nomMol = input(f"Entrer le nom de la molecule  : ")
    description = input(f"Entrer la description du medicament : ")
    quantiteMedicamentJour = int(input(f"Entrer la quantite de medicament a consommer par jour sous la forme d'un entier : "))

    #On tente d'insérer le medicament :
    try:

        cur.execute('''
            INSERT INTO Medicament (nomMol, description, quantiteMedicamentJour)
            VALUES (%s, %s, %s) ''',
            (nomMol, description, quantiteMedicamentJour))

        print(f"Médicament ajouté avec succès.\n")
    except psycopg2.errors:
        print(f"Echec de l'insertion")
        return
    conn.commit()



def statistiques_clinique(cur) :
    #On veut un affichage du nombre de clients, d'animaux, de vétérinaires et d'assistants enregistrés dans la base de données.
    cur.execute('''SELECT COUNT(*) FROM Client''')
    nbClients = cur.fetchone()[0]
    cur.execute('''SELECT COUNT(*) FROM Animal''')
    nbAnimaux = cur.fetchone()[0]
    cur.execute('''SELECT COUNT(*) FROM Veterinaire''')
    nbVeterinaires = cur.fetchone()[0]
    cur.execute('''SELECT COUNT(*) FROM Assistant''')
    nbAssistants = cur.fetchone()[0]
    print(f''' La base de donnée contient exactement :\n
          - {nbClients} Clients\n
          - {nbAnimaux} Animaux\n
          - {nbVeterinaires} Vétérinaires\n
          - {nbAssistants} Assistants\n
    ''')

def statistiques_medicament(cur) :
    #On veut récupérer pour chaque médicament, le nombre de médicaments consommés (medic.quantiteMedicamentJour * dm.dureeTraitement)
    #On utilise pour cela une vue : quantiteMedicamentConsommee
    cur.execute('''SELECT * FROM quantiteMedicamentConsommee''')
    res = cur.fetchall()
    if (not res) :
        print("echec de la requête pour les statistiques des médicaments")
    colonnes = ("Nom médicament", "Quantité totale consommée")
    affichageSelect(colonnes, res)


def ajouterAnimal(cur, conn):
    idAnimal = id_suivant(cur, "Animal", "idAnimal")
    nomAnimal = input("Entrez le nom de l'animal : ")
    numPuceId = input("Entrez le numéro de puce de l'animal (opt. entrez 'non' pour ne pas spécifier)")
    if (numPuceId == "non") :
        numPuceId = None
    numPasseport = input("Entrez le numéro de passport de l'animal (opt. entrez 'non' pour ne pas spécifier)")
    if (numPasseport == "non") :
        numPasseport = None
    listeTailles = ["petite","moyenne","autre"]
    choixTaille = -1
    print('''Tailles possibles de l'animal :\n
          0. petite\n
          1. moyenne\n
          2. autre''')
    while(choixTaille <0 and choixTaille>2):
        choixTaille = int(input("Votre choix ? (0,1,2)"))
        if (choixTaille <0 and choixTaille>2) :
            print("choix incorrect, reessayez.")
    tailleAnimal = listeTailles[choixTaille]
    #gestion des espèces : on affiche celles qui existent déjà, si l'animal n'appartient à aucune d'elles, on propose à l'utilisateur de créer une nouvelle espèce
    cur.execute('''SELECT * FROM Espece''')
    res = cur.fetchall()
    nombreEspecesTotal = len(res)
    colonnesEspeces = ["idEspece", "typeEspece", "intitulePrecis"]
    affichageSelect(colonnesEspeces, res)
    estDedans= ""
    idEspeceChoisie = -1
    while(estDedans != "oui" and estDedans!= "non") :
        estDedans = input("L'espèce de votre animal apparaît-elle dans la liste ? (oui | non)")
    if (estDedans == "oui") :
        idEspeceChoisie = int(input("Entrez l'id de l'espèce de votre animal"))
        while (idEspeceChoisie < 0 or idEspeceChoisie > nombreEspecesTotal) :
            print("id choisi incorrect, réessayez.")
            idEspeceChoisie = int(input("Entrez l'id de l'espèce de votre animal"))
    else :
        #On doit créer une nouvelle espèce
        idEspeceChoisie = ajouterEspece(cur, conn)
    #À ce stade, on connaît l'id de l'espèce choisie, on peut donc insérer l'animal dans la table Animal
    try :
        cur.execute('''INSERT INTO Animal VALUES (%s, %s, %s, %s, %s, %s) ''',
                    (idAnimal, nomAnimal, numPuceId, numPasseport, tailleAnimal, idEspeceChoisie))
        print(f"Insertion de l'animal {nomAnimal} avec succès.")
        conn.commit()
    except psycopg2.errors :
        print("Attention ! Erreur lors de l'insertion de l'animal.")
        return

def modifierAnimal(cur, conn):
    #On veut proposer à l'utilisateur de rechercher un animal par nom ou par id, puis lui proposer de le modifier
    choixTypeRecherche = 0
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
        elif choixTypeRecherche == 2:
            #On demande l'id de l'animal
            idAnimal = int(input("Entrez l'id de l'animal : "))
            cur.execute('''SELECT A.idAnimal, A.nom, A.numPuceId, A.numPasseport, A.taille, E.typeEspece, E.intitulePrecis
            FROM Animal A
            JOIN Espece E ON A.espece = E.idEspece
            WHERE A.idAnimal = %s''', (idAnimal,))
            animalChoisi = cur.fetchone()
    #On connaît l'animal choisi, on l'affiche à nouveau avant de proposer de le modifier
    print(("idAnimal", "nom", "numPuceId", "numPasseport", "taille", "type espèce", "intitulé précis"), animalChoisi)
    affichageSelect(("idAnimal", "nom", "numPuceId", "numPasseport", "taille", "type espèce", "intitulé précis"), (animalChoisi,))
    nouveauNom = animalChoisi[1]
    nouveauNumPuceId = animalChoisi[2]
    nouveauNumPasseport = animalChoisi[3]
    nouvelleTaille = animalChoisi[4]
    #Il faut récupérer l'id de l'espèce actuelle
    cur.execute("SELECT espece FROM Animal WHERE idAnimal = %s", (animalChoisi[0],))
    nouvelIdEspece= cur.fetchone()[0]
    choixModifAnimal = -1
    while (choixModifAnimal != 0):
        print('''\n---Menu Modification Animal---\n
          0. Arrêter les modifications et enregistrer l'animal\n
          1. Modifier le nom\n
          2. Modifier le numéro de la puce\n
          3. Modifier le numéro du passeport\n
          4. Modifier la taille\n
          5. Modifier le type d'espèce''')
        choixModifAnimal = int(input("Votre choix ? : "))
        if (choixModifAnimal == 1) :
            nouveauNom = input("Entrez le nouveau nom de l'animal : ")
            print(f"Le nom sera désormais : {nouveauNom}")
        elif (choixModifAnimal == 2) :
            nouveauNumPuceId = int(input("Entrez le nouveau numéro de puce d'identification de l'animal : "))
            print(f"Le numéro de puce sera désormais : {nouveauNumPuceId}")
        elif (choixModifAnimal == 3) :
            nouveauNumPasseport = int(input("Entrez le nouveau numéro de passeport de l'animal : "))
            print(f"Le numéro de passeport sera désormais : {nouveauNumPasseport}")
        elif (choixModifAnimal == 4) :
            nouvelleTaille = input("Entrez la nouvelle taille de l'animal : ")
            print(f"La nouvelle taille sera désormais : {nouvelleTaille}")
        elif (choixModifAnimal == 5) :
            #Ce cas est plus complexe, il faut vérifier que l'espèce que l'utilisateur veut existe déjà, et si ce n'est pas le cas, il faut qu'il la crée
            cur.execute('''SELECT * FROM Espece''')
            res = cur.fetchall()
            nombreEspecesTotal = len(res)
            colonnesEspeces = ["idEspece", "typeEspece", "intitulePrecis"]
            affichageSelect(colonnesEspeces, res)
            estDedans= ""
            while(estDedans != "oui" and estDedans!= "non") :
                estDedans = input("L'espèce de votre animal apparaît-elle dans la liste ? (oui | non)")
            if (estDedans == "oui") :
                nouvelIdEspece = int(input("Entrez l'id de l'espèce de votre animal"))
                while (nouvelIdEspece < 0 or nouvelIdEspece > nombreEspecesTotal) :
                    print("id choisi incorrect, réessayez.")
                    nouvelIdEspece = int(input("Entrez l'id de l'espèce de votre animal"))
            else :
                #On doit créer une nouvelle espèce
                nouvelIdEspece = ajouterEspece(cur, conn)
    #L'utilisateur a arrêté les modifications, on peut faire la requête update
    try :
        cur.execute('''UPDATE Animal SET nom=%s, numPuceId=%s, numPasseport=%s, taille=%s, espece=%s WHERE idAnimal=%s''', (nouveauNom, nouveauNumPuceId, nouveauNumPasseport, nouvelleTaille, nouvelIdEspece, animalChoisi[0]))
        conn.commit()
    except psycopg2.errors :
        print("Attention ! Erreur lors de la modification de l'animal.")
        return

def ajouterEspece(cur, conn) :
    idEspece = id_suivant(cur, "Espece","idEspece")
    typesEspeces = ["félin", "canidé", "reptile", "rongeur", "oiseau", "autre"]
    print('''Voici les types d'especes possibles :\n
          0. félin\n
          1. canidé\n
          2. reptile\n
          3. rongeur\n
          4. oiseau\n
          5. autre''')
    choixType=  int(input("Votre choix ? (0...5) :"))
    while (choixType < 0 or choixType > 5) :
        print("Saisie incorrecte. Réessayez")
        choixType=  int(input("Votre choix ? (0...5) :"))
    typeEspece = typesEspeces[choixType]
    intitulePrecisEspece = input("Entrez l'intitulé précis de l'espèce : ")
    try :
        cur.execute('''INSERT INTO Espece VALUES (%s, %s, %s)''',
                    (idEspece, typeEspece, intitulePrecisEspece))
    except psycopg2.errors :
        print("Attention ! Erreur lors de l'insertion de l'espèce.")
        return
    conn.commit()
    print(f"Espèce d'id {idEspece} insérée avec succes")
    #On retourne l'id de l'espèce nouvellement insérée
    return idEspece

def creerDossierMedical(cur, conn):
    idDossier = id_suivant(cur, "DossierMedical", "idDossier")

    tailleAnimal = input("Entrez la taille mesurée de l'animal (opt. entrez 'non' pour ne pas spécifier) : ")
    if (tailleAnimal == "non") :
        tailleAnimal = None
    else:
        tailleAnimal = int(tailleAnimal)
    poidsAnimal = input("Entrez le poids mesuré de l'animal (opt. entrez 'non' pour ne pas spécifier) : ")
    if (poidsAnimal == "non") :
        poidsAnimal = None
    else:
        poidsAnimal = int(poidsAnimal)
    while ((tailleAnimal == None) and (poidsAnimal == None)):
        print("La taille et le poids ne peuvent être tous les deux nuls !")
        tailleAnimal = input("Entrez la taille mesurée de l'animal (opt. entrez 'non' pour ne pas spécifier) : ")
        if (tailleAnimal == "non") :
            tailleAnimal = None
        else:
            tailleAnimal = int(tailleAnimal)
        poidsAnimal = input("Entrez le poids mesuré de l'animal (opt. entrez 'non' pour ne pas spécifier) : ")
        if (poidsAnimal == "non") :
            poidsAnimal = None
        else:
            poidsAnimal = int(poidsAnimal)

    debutTraitement = input("Entrez la date de début du traitement prescrit (aaaa-mm-jj) : ")
    dureeTraitement = int(input("Entrez la durée du traitement prescrit : "))
    observationGenerale = input("Entrez l'observation générale rédigée : ")
    descriptionProcedure = input("Décrivez la procédure effectuée : ")
    dateSaisie = str(datetime.date.today())

    #Gestion de l'animal traité : on affiche ceux qui existent
    cur.execute('''SELECT idAnimal, nom, numPuceId, numPasseport FROM Animal''')
    res = cur.fetchall()
    nombreAnimauxTotal = len(res)
    affichageSelect(("id", "Nom", "Numéro de puce", "Numéro de passeport"), res)
    animalChoisi = int(input("Entrez la ligne de l'animal traité : "))
    while (animalChoisi < 0 or animalChoisi > nombreAnimauxTotal) :
        print("Ligne choisie incorrect, réessayez.")
        animalChoisi = int(input("Entrez la ligne de l'animal traité : "))
    idAnimalChoisi = res[animalChoisi][0]

    #Gestion du vétérinaire prescripteur : on affiche ceux qui existent
    cur.execute('''SELECT idVet, nom, prenom FROM Veterinaire''')
    res = cur.fetchall()
    nombreVetoTotal = len(res)
    affichageSelect(("id", "Nom", "Prénom"), res)
    vetoChoisi = int(input("Entrez la ligne du vétérinaire prescripteur : "))
    while (vetoChoisi < 0 or vetoChoisi > nombreVetoTotal) :
        print("Ligne choisie incorrect, réessayez.")
        vetoChoisi = int(input("Entrez la ligne du vétérinaire prescripteur : "))
    idVetoChoisi = res[vetoChoisi][0]

    #Ajout du dossier en lui-même à la base de données
    try :
        cur.execute('''INSERT INTO DossierMedical VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ''',
                    (idDossier, tailleAnimal, poidsAnimal, debutTraitement, dureeTraitement, observationGenerale, descriptionProcedure, dateSaisie, idAnimalChoisi, idVetoChoisi))
        print(f"Insertion de l'animal numéro {idDossier} avec succès.")
    except psycopg2.errors :
        print("Attention ! Erreur lors de l'insertion du dossier.")
        return

    #Gestion des vétérinaires ayant participé : on affiche ceux qui existent
    cur.execute('''SELECT idVet, nom, prenom FROM Veterinaire''')
    res = cur.fetchall()
    nombreVetoTotal = len(res)
    affichageSelect(("id", "Nom", "Prénom"), res)
    choisi = int(input("Entrez la ligne d'un vétérinaire s'il a participé à la procédure ou entrez -1 si tous les vétérinaires ayant participé ont été ajoutés : "))
    while (choisi < -1 or choisi > nombreVetoTotal) :
        print("id choisi incorrect, réessayez avec une autre ligne ou entrez -1.")
        choisi = int(input("Entrez la ligne d'un vétérinaire s'il a participé à la procédure ou entrez -1 si tous les vétérinaires ayant participé ont été ajoutés : "))
    idChoisi = res[choisi][0] if choisi != -1 else -1
    while (idChoisi != -1):
        #Insertion du vétérinaire choisi
        try :
            cur.execute('''INSERT INTO AFaitVet VALUES (%s, %s) ''',
                        (idChoisi, idDossier))
            print(f"Insertion du vétérinaire numéro {idChoisi} avec succès.")
        except psycopg2.errors :
            print("Attention ! Erreur lors de l'insertion de la prise en compte du vétérinaire.")
            return
        #Nouveau vétérinaire
        choisi = int(input("Entrez la ligne d'un vétérinaire s'il a participé à la procédure ou entrez -1 si tous les vétérinaires ayant participé ont été ajoutés : "))
        while (choisi < -1 or choisi > nombreVetoTotal) :
            print("id choisi incorrect, réessayez avec une autre ligne ou entrez -1.")
            choisi = int(input("Entrez la ligne d'un vétérinaire s'il a participé à la procédure ou entrez -1 si tous les vétérinaires ayant participé ont été ajoutés : "))
        idChoisi = res[choisi][0] if choisi != -1 else -1

    #Gestion des assistants ayant participé : on affiche ceux qui existent
    cur.execute('''SELECT idAssist, nom, prenom FROM Assistant''')
    res = cur.fetchall()
    nombreAssistTotal = len(res)
    affichageSelect(("id", "Nom", "Prénom"), res)
    choisi = int(input("Entrez la ligne d'un assistant s'il a participé à la procédure ou entrez -1 si tous les assistants ayant participé ont été ajoutés : "))
    while (choisi < -1 or choisi > nombreAssistTotal) :
        print("Ligne choisie incorrect, réessayez avec une autre ligne ou entrez -1.")
        choisi = int(input("Entrez la ligne d'un assistant s'il a participé à la procédure ou entrez -1 si tous les assistants ayant participé ont été ajoutés : "))
    idChoisi = res[choisi][0] if choisi != -1 else -1
    while (idChoisi != -1):
        #Insertion de l'assistant choisi
        try :
            cur.execute('''INSERT INTO AFaitAssist VALUES (%s, %s) ''',
                        (idChoisi, idDossier))
            print(f"Insertion de l'assistant numéro {idChoisi} avec succès.")
        except psycopg2.errors :
            print("Attention ! Erreur lors de l'insertion de la prise en compte de l'assistant.")
            return
        #Nouvel assistant
        choisi = int(input("Entrez la ligne d'un assistant s'il a participé à la procédure ou entrez -1 si tous les assistants ayant participé ont été ajoutés : "))
        while (choisi < -1 or choisi > nombreAssistTotal) :
            print("id choisi incorrect, réessayez avec une autre ligne ou entrez -1.")
            choisi = int(input("Entrez la ligne d'un assistant s'il a participé à la procédure ou entrez -1 si tous les assistants ayant participé ont été ajoutés : "))
        idChoisi = res[choisi][0] if choisi != -1 else -1

    #Gestion des médicaments prescrits : on affiche ceux qui existent
    cur.execute('''SELECT nomMol, description FROM Medicament''')
    res = cur.fetchall()
    nombreMedocTotal = len(res)
    affichageSelect(("Nom", "Description"), res)
    choisi = int(input("Entrez la ligne d'un médicament s'il est prescrit ou entrez -1 si tous les médicament prescrits ont été ajoutés : "))
    while (choisi < -1 or choisi > nombreMedocTotal) :
        print("Ligne choisi incorrect, réessayez avec une autre ligne ou entrez -1.")
        choisi = int(input("Entrez la ligne d'un médicament s'il est prescrit ou entrez -1 si tous les médicament prescrits ont été ajoutés : "))
    idChoisi = res[choisi][0] if choisi != -1 else -1 #N'est pas à proprement parler un id mais nommé comme ça pour garder une cohérence dans le code
    while (idChoisi != -1):
        #Insertion du médicament choisi
        try :
            cur.execute('''INSERT INTO ContientMedicDoss VALUES (%s, %s) ''',
                        (idChoisi, idDossier))
            print(f"Insertion du médicament {idChoisi} avec succès.")
        except psycopg2.errors :
            print("Attention ! Erreur lors de l'insertion du médicament prescrit.")
            return
        #Nouveau médicament
        choisi = int(input("Entrez la ligne d'un médicament s'il est prescrit ou entrez -1 si tous les médicament prescrits ont été ajoutés : "))
        while (choisi < -1 or choisi > nombreMedocTotal) :
            print("Ligne choisi incorrect, réessayez avec une autre ligne ou entrez -1.")
            choisi = int(input("Entrez la ligne d'un médicament s'il est prescrit ou entrez -1 si tous les médicament prescrits ont été ajoutés : "))
        idChoisi = res[choisi][0] if choisi != -1 else -1 #N'est pas à proprement parler un id mais nommé comme ça pour garder une cohérence dans le code

    #Gestion des résulats d'analyses réalisées durant la procédure : on affiche ceux qui existent déjà, si le résultat n'est pas parmi eux, on propose à l'utilisateur de le rajouter
    cur.execute('''SELECT idResultat , lien FROM ResultatAnalyse ''')
    res = cur.fetchall()
    nombreResultTotal = len(res)
    affichageSelect(("id", "Lien des résultats d'analyse"), res)
    idChoisi = -1
    while (idChoisi != -1):
        estPasDedans= ""
        while(estPasDedans != "oui" and estPasDedans!= "non") :
            estPasDedans = input("Voulez-vous ajouter au dossier un résultat d'analyse qui n'apparaît pas dans la liste ? (oui | non)")
        if (estPasDedans == "non") :
            choisi = int(input("Entrez la ligne d'un résultat d'analyse s'il a été réalisé durant la procédure ou entrez -1 si tous les résulats d'analyses réalisées ont été ajoutés : "))
            while (choisi < -1 or choisi > nombreResultTotal) :
                print("Ligne choisie incorrect, réessayez avec une autre ligne ou entrez -1.")
                choisi = int(input("Entrez la ligne d'un résultat d'analyse s'il a été réalisé durant la procédure ou entrez -1 si tous les résulats d'analyses réalisées ont été ajoutés : "))
            idChoisi = res[choisi][0] if choisi != -1 else -1
            #Insertion du résultat d'analyse choisi
            if(idChoisi != 1):
                try :
                    cur.execute('''INSERT INTO ContientResultDoss VALUES (%s, %s) ''',
                                (idChoisi, idDossier))
                    print(f"Insertion du résultat d'analyse numéro {idChoisi} avec succès.")
                except psycopg2.errors :
                    print("Attention ! Erreur lors de l'insertion du résultat d'analyse.")
                    return
                #Nouveau résultat d'analyse
                choisi = int(input("Entrez la ligne d'un résultat d'analyse s'il a été réalisé durant la procédure ou entrez -1 si tous les résulats d'analyses réalisées ont été ajoutés : "))
                while (choisi < -1 or choisi > nombreResultTotal) :
                    print("Ligne choisie incorrect, réessayez avec une autre ligne ou entrez -1.")
                    choisi = int(input("Entrez la ligne d'un résultat d'analyse s'il a été réalisé durant la procédure ou entrez -1 si tous les résulats d'analyses réalisées ont été ajoutés : "))
                idChoisi = res[choisi][0] if choisi != -1 else -1
        else :
            #On doit créer un nouveau résultat d'analyse
            idChoisi = ajouterResultatAnalyse(cur, conn)
    conn.commit()



def ajouterResultatAnalyse(cur, conn) :
    idResultat = id_suivant(cur, "ResultatAnalyse ","idResultat")
    lienResultat = input("Entrez le lien du résultat d'analyse à ajouter : ")
    try :
        cur.execute('''INSERT INTO ResultatAnalyse  VALUES (%s, %s)''',
                    (idResultat, lienResultat))
    except psycopg2.errors :
        print("Attention ! Erreur lors de l'insertion du résultat d'analyse.")
        return
    conn.commit()
    print(f"Le résultat d'analyse d'id {idResultat} correspondant au lien {lienResultat} a été inséré avec succes")
    #On retourne l'id du résultat d'analyse nouvellement inséré
    return idResultat

def statistiques_traitement(cur) :
    cur.execute('''SELECT idDossier, debutTraitement, dureeTraitement FROM DossierMedical
                WHERE debutTraitement + interval '1' day * dureeTraitement < current_date;''')
    res = cur.fetchall()
    if (not res) :
        print("echec de la requête pour les statistiques des traitements encore en cours")
    colonnes = ("idDossier", "debutTraitement", "dureeTraitement")
    affichageSelect(colonnes, res)

def ajouterAdmin(cur, conn) :
    username = input(f"Entrer le login du nouvel Administrateur : ")
    password = input(f"Entrer le mot de passe du nouvel Administrateur : ")
    id_admin = id_suivant(cur, "Admin", "idAdmin")
    try:
        cur.execute('''
                INSERT INTO Admin (idAdmin, login, motDePasse)
                VALUES (%s, %s, %s)''',
                (id_admin, username, password))
        print(f"Création avec succès du compte Administrateur, id : {id_admin}\n " )
    except psycopg2.errors:
        print("Attention, erreur lors de l'insertion ! Un administrateur avec le meme nom existe peut etre.")
        return
    conn.commit()


def afficherRapportActiviteVeto(cur):
    cur.execute('''SELECT idVet, nom, prenom FROM Veterinaire''')
    res = cur.fetchall()
    nombreVetoTotal = len(res)
    affichageSelect(("id", "Nom", "Prénom"), res)
    vetoChoisi = int(input("Entrez la ligne du vétérinaire recherché : "))
    while (vetoChoisi < 0 or vetoChoisi > nombreVetoTotal) :
        print("Ligne choisie incorrect, réessayez.")
        vetoChoisi = int(input("Entrez la ligne du vétérinaire recherché : "))
    idVetoChoisi = res[vetoChoisi][0]
    cur.execute("SELECT animal, debut FROM EstSuiviPar WHERE veterinaire=%s AND fin IS NULL", (idVetoChoisi,))
    #Affichage des patients en cours de suivi
    res = cur.fetchall()
    for animal, debut in res:
        print(f"Suit le patient numéro {animal} depuis le {debut}")
    #Affichage des patients précedemment suivi
    cur.execute("SELECT animal, debut, fin FROM EstSuiviPar WHERE veterinaire=%s AND fin IS NOT NULL", (idVetoChoisi,))
    res = cur.fetchall()
    for animal, debut, fin in res:
        print(f"A suivi le patient numéro {animal} du {debut} au {fin}")
    #Affichage des dossiers où le vétérinaire a été vétérinaire prescripteur
    cur.execute("SELECT idDossier, saisie, animal FROM DossierMedical WHERE veterinairePrescripteur=%s", (idVetoChoisi,))
    res = cur.fetchall()
    for idDossier, saisie, animal in res:
        print(f"A été le vétérinaire prescripteur du traitement lors de la procédure concernant le patient numéro {animal} et inscrite le {saisie} dans le dossier médical numéro {idDossier}")
    #Affichage des numéros de dossiers où le vétérinaire a participé
    cur.execute("SELECT AFaitVet.dossier, DossierMedical.saisie, DossierMedical.animal FROM AFaitVet JOIN DossierMedical ON AFaitVet.dossier = DossierMedical.idDossier WHERE veterinaire=%s", (idVetoChoisi,))
    res = cur.fetchall()
    for idDossier, saisie, animal in res:
        print(f"A participé à la procédure concernant le patient numéro {animal} et inscrite le {saisie} dans le dossier médical numéro {idDossier}")

def afficherRapportActiviteAssistant(cur):
    cur.execute('''SELECT idAssist, nom, prenom FROM Assistant''')
    res = cur.fetchall()
    nombreAssistTotal = len(res)
    affichageSelect(("id", "Nom", "Prénom"), res)
    assistChoisi = int(input("Entrez la ligne de l'assistant recherché : "))
    while (assistChoisi < 0 or assistChoisi > nombreAssistTotal) :
        print("Ligne choisie incorrect, réessayez.")
        assistChoisi = int(input("Entrez la ligne de l'assistant recherché : "))
    idAssistChoisi = res[assistChoisi][0]
    cur.execute("SELECT animal, debut FROM EstSuiviPar WHERE assistant=%s AND fin IS NULL", (idAssistChoisi,))
    #Affichage des numéros de dossiers où l'assistant a participé
    cur.execute("SELECT AFaitAssist.dossier, DossierMedical.saisie, DossierMedical.animal FROM AFaitAssist JOIN DossierMedical ON AFaitAssist.dossier = DossierMedical.idDossier WHERE assistant=%s", (idAssistChoisi,))
    res = cur.fetchall()
    for idDossier, saisie, animal in res:
        print(f"A participé à la procédure concernant le patient numéro {animal} et inscrite le {saisie} dans le dossier médical numéro {idDossier}")

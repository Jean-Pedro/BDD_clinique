# -*- coding: utf-8 -*-

import psycopg2

def id_suivant(cur, table:str):
    cur.execute("(SELECT MAX(idUser) FROM "+ table +")")
    last_id = cur.fetchone()
    if last_id == None:
        return 1
    return last_id[0]+1

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
        elif choixTypeRecherche == 2:
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
    WHERE a.idAnimal = %s
    ORDER BY saisie DESC''',(animalChoisi[0],))
    dossiersMedicaux = cur.fetchall()
    for dossier in dossiersMedicaux :
        afficherDossierMedical(dossier, cur)

def ajouterClient(cur, conn) :
    print("Il faut créer un compte pour le client")
    username = input("Entrer le nom d'utilisateur du client")
    password = input("Entrer le mot de passe du client")
    id_user = id_suivant(cur, "Users")
    #On tente d'insérer le client comme utilisateur
    try:    
        cur.execute('''
                INSERT INTO Users (idUser, login, motDePasse, type)
                VALUES (%s, %s, %s, 'client')''',
                (id_user, username, password))
        print(f"Création avec succès du compte client, id : {id_user}" )
    except psycopg2.errors:
        print("Attention, erreur lors de l'insertion !")
        return
    
    nom = input("Entrer le nom du client : ")
    prenom = input("Entrer le prénom du client : ")
    dateNaissance = input("Entrer la date de naissance du client ( format YYYY-MM-DD): ")
    adresse = input("Entrer l'adresse du client : ")
    tel = input("Entrer le numéro de téléphone du client : ")
    #On tente d'insérer le client :
    try:
        cur.execute('''
                INSERT INTO Client (idClient, nom, prenom, dateNaissance, adresse, tel)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING idClient''',
                (id_suivant(cur, "Client"), nom, prenom, dateNaissance, adresse, tel))

        print("Client ajouté avec succès.")
    except psycopg2.errors:
        print("Echec de l'insertion, le client pourrait déjà exister")
        return
    conn.commit()


def statistiques_clinique(cur) :
    #On veut un affichage du nombre de clients, d'animaux, de vétérinaires et d'assistants enregistrés dans la base de données.
    cur.execute('''SELECT COUNT(*) FROM Client''')
    nbClients = cur.fetchone()
    cur.execute('''SELECT COUNT(*) FROM Animal''')
    nbAnimaux = cur.fetchone()
    cur.execute('''SELECT COUNT(*) FROM Veterinaire''')
    nbVeterinaires = cur.fetchone()
    cur.execute('''SELECT COUNT(*) FROM Assistant''')
    nbAssistants = cur.fetchone()
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
    idAnimal = id_suivant(cur, "Animal")
    nomAnimal = input("Entrez le nom de l'animal : ")
    numPuceId = input("Entrez le numéro de puce de l'animal (opt. entrez 'non' pour ne pas spécifier)")
    if (numPuceId == "non") :
        numPuceId = "NULL"
    numPasseport = input("Entrez le numéro de passport de l'animal (opt. entrez 'non' pour ne pas spécifier)")
    if (numPasseport == "non") :
        numPasseport = "NULL"
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
            cur.execute('''SELECT A.id, A.nom, A.numPuceId, A.numPasseport, A.taille, E.typeEspece, E.intitulePrecis
            FROM Animal A
            JOIN Espece E ON A.espece = E.idEspece
            WHERE A.idAnimal = %s''', (idAnimal,))
            animalChoisi = cur.fetchone()
    #On connaît l'animal choisi, on l'affiche à nouveau avant de proposer de le modifier 
    affichageSelect(("idAnimal", "nom", "numPuceId", "numPasseport", "taille", "type espèce", "intitulé précis"), animalChoisi)
    nouveauNom = animalChoisi[1]
    nouveauNumPuceId = animalChoisi[2]
    nouveauNumPasseport = animalChoisi[3]
    nouvelleTaille = animalChoisi[4]
    #Il faut récupérer l'id de l'espèce actuelle
    cur.execute("SELECT espece FROM Animal WHERE idAnimal = %s", (animalChoisi[0]))
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
            nouvelleTaille = int(input("Entrez la nouvelle taille de l'animal : "))
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
    except psycopg2.errors :
        print("Attention ! Erreur lors de la modification de l'animal.")
        return     

def ajouterEspece(cur, conn) :
    idEspece = id_suivant(cur, "Espece")
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
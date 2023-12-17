import psycopg2
from fonctions import *

conn = psycopg2.connect(
      user = "nf18a068",
      password = "Lm0mhUpSY50v",
      host = "tuxa.sme.utc",
      database = "dbnf18a068"
)
cur = conn.cursor()



choixModeConnexion = -1
succesConnexionAdministrateur = False
typeUtilisateur =""
while (choixModeConnexion != 0 and choixModeConnexion != 1 and choixModeConnexion != 2) :
    print(
    '''------Menu Connexion------\n
    0 : Quitter\n
    1 : Connexion Utilisateur\n
    2 : Connexion Administrateur\n''')
    choixModeConnexion = int(input("Votre choix ? : "))
    if ( choixModeConnexion == 0) :
        exit()
    elif (choixModeConnexion == 1) :
        idUtilisateur, typeUtilisateur = connexionUtilisateur(cur)
    elif (choixModeConnexion == 2) :
        succesConnexionAdministrateur = connexionAdministrateur(cur)



#Modes Utilisateurs
if (typeUtilisateur == "client"):
    print("Connexion Client réussie")
    #Voir le dossier de ses animaux dans la clinique
    choixClient = -1
    while(choixClient != 0):
        print(
        '''------Menu Client------\n
        0. Quitter\n
        1. Consulter les infos de mon animal\n''')
        choixClient = int(input("Votre choix ? : "))
        if (choixClient == 0) :
            exit()
        elif (choixClient == 1) :
            afficherInfosAnimal(cur, idUtilisateur, typeUtilisateur)


if (typeUtilisateur == "veterinaire"):
    print("Connexion Vétérinaire réussie")
    choixVet = -1
    while(choixVet != 0):
        print(
        '''------Menu Vétérinaire------\n
        0. Quitter\n
        1. Consulter les infos d'un animal\n
        2. Ajouter un dossier médical\n
        3. Ajouter un client\n
        4. Ajouter un animal\n
        5. Modifier un animal''')
        choixVet = int(input("Votre choix ? : "))
        if (choixVet == 0) :
            exit()
        elif (choixVet == 1) :
            afficherInfosAnimal(cur, idUtilisateur, typeUtilisateur)
        elif (choixVet == 2) :
            creerDossierMedical(cur, conn)
        elif (choixVet == 3) :
            ajouterClient(cur, conn)
        elif (choixVet == 4) :
            ajouterAnimal(cur, conn)
        elif (choixVet == 5) :
            modifierAnimal(cur, conn)

    #creer dossier medicaux
    #acceder aux données des patients, clients

    #peut rajouter des animaux et des clients

if (typeUtilisateur == "assistant"):
    print("Connexion assistant réussie")
    choixVet = -1
    while(choixAssist != 0):
        print(
        '''------Menu Assistant------\n
        0. Quitter\n
        1. Consulter les infos d'un animal\n
        2. Ajouter un dossier médical''')
        choixVet = int(input("Votre choix ? : "))
        if (choixVet == 0) :
            exit()
        elif (choixVet == 1) :
            afficherInfosAnimal(cur, idUtilisateur, typeUtilisateur)
        elif (choixVet == 2) :
            creerDossierMedical(cur, conn)
    
    #creer dossier medicaux
    #acceder aux données des patients, clients
#Mode Administrateur
if (succesConnexionAdministrateur) :
    print("Connexion Administrateur réussie.")
    choixAdmin = -1
    while(choixAdmin != 0):
        print(
        '''------Menu Administrateur------\n
        0. Quitter\n
        1. Modifier la base de donnée\n
        2. Voir des statistiques sur la clinique
        ''')
        choixAdmin = int(input("Votre choix ? : "))
        if (choixAdmin == 0) :
            exit()
        elif (choixAdmin == 1) :
            choixModif = -1
            while (choixModif != 0) :
                print('''------Menu Modification BDD------\n
                0. Revenir au menu précédent\n
                1. Creer un client\n
                2. Mettre a jour un client\n
                3. Supprimer un client\n
                4. Creer un veterinaire\n
                5. Mettre a jour un veterinaire\n
                6. Supprimer un veterinaire\n
                7. Creer un assistant\n
                8. Mettre a jour un assistant\n
                9. Supprimer un assistant\n''')
                choixModif= int(input("Votre choix ? : "))
                if (choixModif == 0) :
                    choixAdmin = -1
                    #la boucle while sur choixAdmin tourne donc à nouveau
                elif (choixModif == 1) :
                    ajouterUser(cur, conn, "client")
                elif (choixModif == 2) :
                    updateUser(cur, conn, "client")
                elif (choixModif == 3) :
                    pass #à remplacer par l'appel à la bonne méthode
                elif (choixModif == 4) :
                    ajouterUser(cur, conn, "veterinaire")
                elif (choixModif == 5) :
                    updateUser(cur, conn, "veterinaire")
                elif (choixModif == 6) :
                    pass #à remplacer par l'appel à la bonne méthode
                elif (choixModif == 7) :
                    ajouterUser(cur, conn, "assistant")
                elif (choixModif == 8) :
                    updateUser(cur, conn, "assistant")
                elif (choixModif == 9) :
                    pass #à remplacer par l'appel à la bonne méthode
        elif (choixAdmin == 2) :
            choixStats = -1
            while choixStats != 0 :
                print('''------Menu Statistiques------\n
                  0. Revenir au menu précédent\n
                  1. Statistiques générales sur la base de données\n
                  2. Voir les médicaments consommés\n
                  3. Voir un rapport d'activité d'un vétérinaire\n
                  4. Voir un rapport d'activité d'un assistant\n
                  ''')
                choixStats = int(input("Votre choix ? : "))
                if (choixStats == 0) :
                    choixAdmin = -1
                    #la boucle while sur choixAdmin tourne donc à nouveau
                elif (choixStats == 1) :
                    statistiques_clinique(cur)
                elif (choixStats == 2) :
                    statistiques_medicament(cur)
                elif (choixStats == 3) :
                    pass #à remplacer par l'appel à la bonne méthode
                elif (choixStats == 4) :
                    pass #à remplacer par l'appel à la bonne méthode



#fermeture de la connexion à la base de données
cur.close()
conn.close()
print("La connexion PostgreSQL est fermée")

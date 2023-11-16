import psycopg2
from fonctions import *
try:
    conn = psycopg2.connect(
          user = "nf18a068",
          password = "Lm0mhSY50v",
          host = "tuxa.sme.utc",
          database = "dbnf18a068"
    )
    cur = conn.cursor()
    print(type(cur))
except (Exception, psycopg2.Error) as error :
    print ("Erreur lors de la connexion à PostgreSQL", error)



choixModeConnexion = -1
succesConnexionAdministrateur = False
while (choixModeConnexion != 0) :
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
        0 : Quitter\n
        1 : Consulter les infos de mon animal\n''')
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
        0 : Quitter\n
        1 : Consulter les infos d'un animal\n
        2 : Créer un dossier médical\n''')
        choixVet = int(input("Votre choix ? : "))
        if (choixVet == 0) :
            exit()
        elif (choixVet == 1) :
            afficherInfosAnimal(cur, idUtilisateur, typeUtilisateur)
        elif (choixVet == 2) :
            creerDossierMedical(cur) #pas encore fait
    
    #creer dossier medicaux
    #acceder aux données des patients, clients

    #peut rajouter des animaux et des clients

if (typeUtilisateur == "assistant"):
    print("Connexion assistant réussie")
    #creer dossier medicaux
    #acceder aux données des patients, clients
#Mode Administrateur
if (succesConnexionAdministrateur) :
    print("Connexion Administrateur réussie.")



#fermeture de la connexion à la base de données
cur.close()
conn.close()
print("La connexion PostgreSQL est fermée")

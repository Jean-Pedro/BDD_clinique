
# Note de clarification

## Introduction

Une clinique vétérinaire a besoin d'un système de gestion pour pouvoir organiser ses vétérinaires et ses patients. Nous sommes en charge de l'implémentation d'une base de données qui aura pour but de répondre à ce problème.


## Définition et attribution des rôles

### Administrateur du système : 

- **Définition** : Son rôle est de gérer la globalité de la base de donnée. Il en a le contrôle total.
- **Attribution** : L'administrateur est le chef de la clinique ou bien un membre de l'équipe informatique de la clinique s'il y a et que le chef de la clinique n'a pas les compétences nécessaires.

### Responsable du personnel : 
- **Définition** : Son rôle est de gérer le personnel de la clinique. Il peut en ajouter ou bien en retirer.
- **Attribution** : Le responsable du personnel est le chef du personnel de la clinique.


### Utilisateur de la base de donnée de niveau 1 : 
- **Définition** : Il doit pouvoir accéder à la Base de Données pour pouvoir y ajouter des informations concernant les patients, les clients, rédiger des dossiers médicaux ou encore consulter les données.
- **Attribution** : Un utilisateur de la base de donnée est un vétérinaire.

### Utilisateur de la base de donnée de niveau 2 :
- **Définition** : Il doit pouvoir accéder à la Base de Données pour pouvoir y rédiger des dossiers médicaux ou consulter les données.
- **Attribution** : Un utilisateur de la base de donnée est un assistant.


## Hypothèses

### Animal

Pour la relation Animal

- categorie => **CatégorieAnimal** (*, 1)
- nom : string
- espèce :string
- date_naissance : DATE (juste une année, NULL)
- numPuceId : int (NULL)
- numPasseport : int (NULL)
- est la propriété => **Client** (\* , \*), la classe association résultante aura deux attributs début et fin de type DATE pour indiquer la période durant laquelle l'animal était possédé par le propriétaire.
- est suivi par => **Personnel** (\*, \*), la classe association résultante aura deux attributs début et fin de type DATE indiquant la période de suivi par le vétérinaire.
- est de => **CatégorieAnimal** (\*, 1)
- possède => **DossierMédical** (1, \*)


### DossierMédical
On a choisi de considérer que chaque patient a plusieurs entrées de dossiers médicaux correspondant chacun à un consultation différente, permettant ainsi par la sélection sql au niveau de l'application finale d'obtenir un dossier médical complet. Dans notre implémentation il faut qu'au moins un des attibus entre mesureTaille et mesurePoids soit défini.

- mesureTaille : int (> 0 )
- mesurePoids : int (> 0)
- débutTraitement : DATE
- duréeTraitement : int
- observationGénérale : string
- descriptionProcédure : string
- saisie : DATETIME
- contient => **RésultatAnalyse** (\*, \*)
- contient => **Médicament** (\*, \*)

### Humain
Cette classe est une classe abstraite qui va permettre de donner par héritage aux classes classes Client et Personnel les attribus qu'ils possèdent en commun.
- nom : string
- prénom : string
- date naissance : DATE
- adresse : string
- tel : string

### Client
Cette classe va hériter tous ses attibus de la classe Humain. nous aurions pu simplement utiliser cette classe en temps que classe mère pour la classe Personnel mais cela aurait compliqué la compréhension de notre représentation.
- est un => **Humain**

### Personnel
Cette classe va hériter une partie de ses attribus de la classe abstraite Humain.
- poste : string ('vétérinaire' / 'assistant')
- specialité => **CatégorieAnimal** ( \*, 0..1 )
- a fait => **DossierMédical** (\*, \*)
- est un => **Humain**


### Médicament
- nomMol : string
- description : string
- quantitéMédicamentJour : int
- autorisé pour : **Especes** (\*, \*)

### Especes
- espece : string

### RésultatsAnalyse
- lien : string


### CatégorieAnimal
- taille : typeTaille
- espece : typeAnimal 

###  enum : TypeTaille 
- petite
- moyenne
- autre

###  enum : TypeAnimal
- félin
- canidé
- reptile
- rongeur
- oiseau
- autre



## Expression de requêtes types : 
- Un assistant peut chercher à savoir quels animaux sont de type 'felin'.
- Le responsable du personnel peut chercher à ajouter un nouveau vétérinaire dans la base de données.
- Un vétérinaire peut chercher à accéder à la liste des propriétaire d'un animal suivant son nom.
- Un vétérinaire peut chercher à accéder à tous les dossiers médicaux d'un patient.

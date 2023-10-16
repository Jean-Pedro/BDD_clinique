
# Projet TD3-G1

## Note de clarification

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
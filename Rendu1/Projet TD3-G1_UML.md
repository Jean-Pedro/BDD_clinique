# Projet TD3-G1

## Diagramme UML

```plantuml
hide circle

class Animal{
    nom : string
    espèce : string
    dateNaissance : DATE
    numPuceId : int
    numPasseport : int

}

class DossierMédical{
    mesureTaille : int <NULL>
    mesurePoids : int <NULL>
    débutTraitement : DATE
    duréeTraitement : int
    observationGénérale : string
    descriptionProcédure : string
    saisie : DATETIME
    
}

note right of DossierMédical
    Si mesureTaille est NULL, mesurePoids 
    ne l'est pas et réciproquement (XOR)
end note

abstract class Humain {
    nom : string
    prénom : string
    date naissance : DATE
    adresse : string
    tel : string
}

class Client {
    
}

class AssociationAnimalClient{
    début : DATE
    fin : DATE
}

class AssociationAnimalPersonnel{
    début : DATE
    fin : DATE    
}

class Personnel {
    poste : string {vétérinaire / assistant}
}

class Médicament {
    nomMol : string {key}
    description : string
    quantitéMédicamentJour : int
    
}

class RésultatsAnalyse{
    lien : string
}

class Especes {
    espece : string {key}
}

class CategorieAnimal {
    taille : typeTaille {key}
    espece : typeAnimal {key}
}

enum TypeTaille
{
    petite
    moyenne
    autre
}

enum TypeAnimal
{
    félin
    canidé
    reptile
    rongeur
    oiseau
    autre
}

Client --|> Humain : est un >
Personnel --|> Humain : est un >

Animal "1"--"*" DossierMédical : possède >
DossierMédical "*"--"*" Médicament : contient >
DossierMédical "*"--"*" RésultatsAnalyse : contient >
Personnel "*"--"*" DossierMédical : a fait >

Especes "*"--"*" Médicament : autorise_pour <
Personnel "*"--"0..1" CategorieAnimal : Spécialisé_en >
Animal "*"--"1" CategorieAnimal : Est_de >

Animal "*"--"*" Client
(Animal, Client) .. AssociationAnimalClient

Animal "*"--"*" Personnel
(Animal, Personnel) .. AssociationAnimalPersonnel
```
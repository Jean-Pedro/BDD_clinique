# Projet TD3-G1

## Diagramme UML

```plantuml
hide circle

class Animal{
    nom : string
    dateNaissance : DATE
    numPuceId : int
    numPasseport : int
    taille : typeTaille

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

class EstPossédéPar{
    début : DATE
    fin : DATE
}

class EstSuiviPar{
    début : DATE
    fin : DATE    
}

abstract class Personnel {
    
}

class Assistant {
    
}

class Vétérinaire {
    
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
    typeEspece : typeAnimal {key} : string
    intitulePrecis : string
}

note right of Especes::intitulePrecis
    Si typeEspece == 'Autre', ce champ 
    ne peut pas être NULL
end note

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

Client --|> Humain : est_un >
Personnel --|> Humain : est_un >

Assistant --|> Personnel : est_un >
Vétérinaire --|> Personnel : est_un >

Animal "1"--"*" DossierMédical : possède >
DossierMédical "*"--"*" Médicament : contient >
DossierMédical "*"--"*" RésultatsAnalyse : contient >
Personnel "*"--"*" DossierMédical : a_fait >

Especes "*"--"*" Médicament : autorise_pour <
Personnel "*"--"0..1" Especes : Spécialisé_en >
Animal "*"--"1" Especes : Est_de >

Animal "*"--"*" Client : >
(Animal, Client) .. EstPossédéPar

Animal "*"--"*" Vétérinaire : >
(Animal, Vétérinaire) .. EstSuiviPar

Vétérinaire "1"--"*" DossierMédical : traitement_precrit_par >




```
CREATE TABLE User
(
    idUser INTEGER PRIMARY KEY,
    login CHAR(6) NOT NULL,
    motDePasse VARCHAR(30) NOT NULL,
    type VARCHAR(15),
    CHECK (type IN ('veterinaire', 'assistant', 'client'))
)

CREATE TABLE Admin
(
    idAdmin INTEGER PRIMARY KEY,
    login CHAR(6) NOT NULL,
    motDePasse VARCHAR(30) NOT NULL
)

CREATE TABLE Medicament (
    nomMol VARCHAR(100) PRIMARY KEY,
    description TEXT NOT NULL,
    quantiteMedicamentJour INTEGER NOT NULL
);



CREATE TABLE ResultatAnalyse (
    idResultat INTEGER PRIMARY KEY,
    lien VARCHAR(150)
);

CREATE TABLE Client (
    idClient INTEGER PRIMARY KEY REFERENCES User(idUser),
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    dateNaissance DATE NOT NULL,
    adresse VARCHAR(100) NOT NULL,
    tel VARCHAR(11) NOT NULL
);

CREATE TABLE Espece(
    idEspece INTEGER PRIMARY KEY,
    typeEspece VARCHAR(30),
    intitulePrecis VARCHAR(30),
    CHECK (typeEspece IN ('félin', 'canidé','reptile', 'rongeur', 'oiseau', 'autre')),
    CHECK ( NOT (intitulePrecis IS NULL AND typeEspece='autre'))
);

CREATE TABLE Assistant (
    idAssist INTEGER PRIMARY KEY REFERENCES User(idUser),
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    dateNaissance DATE NOT NULL,
    adresse VARCHAR(100) NOT NULL,
    tel VARCHAR(11) NOT NULL,
    specialite INTEGER REFERENCES Espece(idEspece)
);

CREATE TABLE Animal (
    idAnimal INTEGER PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    numPuceId INTEGER,
    numPasseport INTEGER,
    taille VARCHAR(7) NOT NULL,
    espece INTEGER REFERENCES Espece NOT NULL,
    CHECK (taille in ('petite', 'moyenne', 'autre'))
);

CREATE TABLE Veterinaire (
    idVet INTEGER PRIMARY KEY REFERENCES User(idUser),
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    dateNaissance DATE NOT NULL,
    adresse VARCHAR(100) NOT NULL,
    tel VARCHAR(11) NOT NULL,
    specialite INTEGER REFERENCES Espece(idEspece)
);

CREATE TABLE DossierMedical (
    idDossier INTEGER PRIMARY KEY,
    mesureTaille INTEGER,
    mesurePoids INTEGER,
    debutTraitement DATE NOT NULL,
    dureeTraitement INTEGER NOT NULL,
    ObservationGenerale TEXT NOT NULL,
    descriptionProcedure TEXT NOT NULL,
    saisie DATE NOT NULL,
    animal INTEGER REFERENCES Animal(idAnimal) NOT NULL,
    veterinairePrescripteur INTEGER REFERENCES Veterinaire(idVet) NOT NULL,
    CHECK (mesureTaille IS NOT NULL OR mesurePoids IS NOT NULL)
);




CREATE TABLE AFaitVet(
	veterinaire INTEGER REFERENCES Veterinaire(idVet),
	dossier INTEGER REFERENCES DossierMedical(idDossier),
	PRIMARY KEY (veterinaire, dossier)
);

CREATE TABLE AFaitAssist(
	assistant INTEGER REFERENCES Assistant(idAssist),
	dossier INTEGER REFERENCES DossierMedical(idDossier),
	PRIMARY KEY (assistant, dossier)
);


CREATE TABLE ContientResultDoss(
	resultat INTEGER REFERENCES ResultatAnalyse(idResultat),
	dossier INTEGER REFERENCES DossierMedical(idDossier),
	PRIMARY KEY (resultat, dossier)
);

CREATE TABLE ContientMedicDoss(
	medicament VARCHAR(100) REFERENCES Medicament(nomMol),
	dossier INTEGER REFERENCES DossierMedical(idDossier),
	PRIMARY KEY (medicament, dossier)
);


CREATE TABLE autorisePour (
    medicament VARCHAR(11) REFERENCES Medicament(nomMol),
    espece INTEGER REFERENCES Espece(idEspece),
    PRIMARY KEY (medicament, espece)
);  

CREATE TABLE EstSuiviPar (
    animal INTEGER REFERENCES Animal(idAnimal),
    veterinaire INTEGER REFERENCES Veterinaire(idVet),
    debut DATE NOT NULL,
    fin DATE, 
    PRIMARY KEY (animal, veterinaire)
);
-- On pensera à vérifier la contrainte complexe de minimalité dans la couche applicative'

CREATE TABLE EstPossedePar(
    animal INTEGER REFERENCES Animal(idAnimal),
    client INTEGER REFERENCES Client(idClient),
    debut DATE NOT NULL,
    fin DATE,
    PRIMARY KEY (animal, client)
);


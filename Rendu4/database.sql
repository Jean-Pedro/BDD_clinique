
CREATE TABLE Users
(
    idUser INTEGER PRIMARY KEY,
    login CHAR(6) NOT NULL UNIQUE,
    motDePasse VARCHAR(30) NOT NULL,
    type VARCHAR(15),
    CHECK (type IN ('veterinaire', 'assistant', 'client'))
);

CREATE TABLE Admin
(
    idAdmin INTEGER PRIMARY KEY,

    login CHAR(6) NOT NULL,
    motDePasse VARCHAR(30) NOT NULL
);

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
    idClient INTEGER PRIMARY KEY REFERENCES Users(idUser),
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
    idAssist INTEGER PRIMARY KEY REFERENCES Users(idUser),
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
    idVet INTEGER PRIMARY KEY REFERENCES Users(idUser),
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




INSERT INTO Users (idUser, login, motDePasse, type) VALUES(1, 'user1', '123456789', 'client');
INSERT INTO Users (idUser, login, motDePasse, type) VALUES(2, 'user2', '123456789', 'client');
INSERT INTO Users (idUser, login, motDePasse, type) VALUES(3, 'user3', '123456789', 'client');
INSERT INTO Users (idUser, login, motDePasse, type) VALUES(4, 'user4', '123456789', 'client');
INSERT INTO Users (idUser, login, motDePasse, type) VALUES(5, 'user5', '123456789', 'client');
INSERT INTO Users (idUser, login, motDePasse, type) VALUES(6, 'user6', '123456789', 'client');
INSERT INTO Users (idUser, login, motDePasse, type) VALUES(7, 'user7', '123456789', 'assistant');
INSERT INTO Users (idUser, login, motDePasse, type) VALUES(8, 'user8', '123456789', 'assistant');
INSERT INTO Users (idUser, login, motDePasse, type) VALUES(9, 'user8', '123456789', 'assistant');
INSERT INTO Users (idUser, login, motDePasse, type) VALUES(10, 'user10', '123456789', 'veterinaire');
INSERT INTO Users (idUser, login, motDePasse, type) VALUES(11, 'user11', '123456789', 'veterinaire');
INSERT INTO Users (idUser, login, motDePasse, type) VALUES(12, 'user12', '123456789', 'veterinaire');
INSERT INTO Users (idUser, login, motDePasse, type) VALUES(13, 'user13', '123456789', 'veterinaire');



--  Medicaments

INSERT INTO Medicament (nomMol, description, quantiteMedicamentJour) VALUES ('amoxicillin', 'Antibiotique à effet général', 1);

INSERT INTO Medicament (nomMol, description, quantiteMedicamentJour) VALUES ('paracetamol', 'Antidouleur miraculeux', 2);

INSERT INTO Medicament (nomMol, description, quantiteMedicamentJour) VALUES ('GSE', 'Désinfectant, utile das le cas de grippe aviaire', 50);


-- ResultatAnalyse

INSERT INTO ResultatAnalyse (idResultat, lien) VALUES (1, 'https://messuperresultats.com/z5VytYNpQJJYY6D-gUq13A');

INSERT INTO ResultatAnalyse (idResultat, lien) VALUES (2, 'https://messuperresultats.com/z5VCTRYJQJJYY6D-gU236A');

INSERT INTO ResultatAnalyse (idResultat, lien) VALUES (3, 'https://messuperresultats.com/z5FT486965DERHTD6YY6D-gUq13A');

INSERT INTO ResultatAnalyse (idResultat, lien) VALUES (4, 'https://messuperresultats.com/z5VytYNpSS682F-h5613A');

INSERT INTO ResultatAnalyse (idResultat, lien) VALUES (5, 'https://messuperresultats.com/DRTYFTKU849HTYF5-u8563A');


-- Clients

INSERT INTO Client (idClient, nom, prenom, dateNaissance, adresse, tel) VALUES (1, 'Darmanin', 'Gérald', '1982-10-11', 'Hôtel de Beauvau, Paris', '0607080910');

INSERT INTO Client (idClient, nom, prenom, dateNaissance, adresse, tel) VALUES (2, 'Borne', 'Elizabeth', '1961-04-18', 'Hôtel de Matignon, Paris 7ème', '0607883911');

INSERT INTO Client (idClient, nom, prenom, dateNaissance, adresse, tel) VALUES (3, 'Macron', 'Emmanuel', '1977-12-21', 'Palais de l Elysee, Paris 8ème', '0907688920');

INSERT INTO Client (idClient, nom, prenom, dateNaissance, adresse, tel) VALUES (4, 'Béchu', 'Christophe', '1974-06-11', 'Hôtel de Roquelaure, 246, boulevard Saint-Germain, Paris 7ème', '0523748928');

INSERT INTO Client (idClient, nom, prenom, dateNaissance, adresse, tel) VALUES (5, 'Béchu', 'Marie-Hortense,', '1977-08-2', 'Hôtel de Roquelaure, 246, boulevard Saint-Germain, Paris 7ème', '0523748928');

INSERT INTO Client (idClient, nom, prenom, dateNaissance, adresse, tel) VALUES (6, 'Retailleau', 'Sylvie', '1965-02-24', 'Pavillon Boncourt, 21 rue Descartes, Paris 5ème', '0523748928');


-- Espece

INSERT INTO Espece (idEspece, typeEspece, intitulePrecis) VALUES (1, 'canidé', 'Croisé Labrador ');

INSERT INTO Espece (idEspece, typeEspece, intitulePrecis) VALUES (2, 'autre', 'Panda');

INSERT INTO Espece (idEspece, typeEspece, intitulePrecis) VALUES (3, 'félin', 'chat');

INSERT INTO Espece (idEspece, typeEspece, intitulePrecis) VALUES (4, 'oiseau', 'Perruche');


-- Assistants

INSERT INTO Assistant (idAssist, nom, prenom, dateNaissance, adresse, tel, specialite) VALUES (7, 'Renaud', 'Augustin', '1965-02-24', '124 Rue de Paris', '0685159675', 1);

INSERT INTO Assistant (idAssist, nom, prenom, dateNaissance, adresse, tel, specialite) VALUES (8,'Eberhardt', 'Alexandre', '1965-02-25', '12 rue des fleurs', '0684559671', 4);

INSERT INTO Assistant (idAssist, nom, prenom, dateNaissance, adresse, tel, specialite) VALUES (9,'Fouinat', 'Quentin', '1965-02-26', '34 avenue du Port', '0645627891', 2);


-- Animal

INSERT INTO Animal (idAnimal, nom, espece, numPuceId, numPasseport, taille) VALUES (1, 'Nemo', 1, 111111, 123456, 'petite');

INSERT INTO Animal (idAnimal, nom, espece, numPuceId, numPasseport, taille) VALUES (2, 'Dori', 2, 111111, 123456, 'moyenne');

INSERT INTO Animal (idAnimal, nom, espece, numPuceId, numPasseport, taille) VALUES (3, 'Bubu', 4, 020304, 968574, 'petite');

INSERT INTO Animal (idAnimal, nom, espece, numPuceId, numPasseport, taille) VALUES (4, 'fifi', 3, 020323, 966574, 'petite');


-- Veterinaires

INSERT INTO Veterinaire (idVet, nom, prenom, dateNaissance, adresse, tel, specialite) VALUES (10,'Pontoire', 'Julien', '2003-12-01', '36 Rue de l''Eglise', '0632458956', 1);

INSERT INTO Veterinaire (idVet, nom, prenom, dateNaissance, adresse, tel, specialite) VALUES (11, 'Biffe', 'Simon', '2003-12-02', '25 Avenue de la Gare', '0645769512', 4);

INSERT INTO Veterinaire (idVet, nom, prenom, dateNaissance, adresse, tel, specialite) VALUES (12, 'Vital', 'Simon', '2003-12-03', '12 Rue de Paris', '0745126398', 2);

INSERT INTO Veterinaire (idVet, nom, prenom, dateNaissance, adresse, tel, specialite) VALUES (13, 'Ragot', 'Nils', '2003-12-04', '15 rue d''Amiens', '0745864297', 2);



-- DossierMédical

INSERT INTO DossierMedical (idDossier, mesureTaille, mesurePoids, debutTraitement, dureeTraitement, ObservationGenerale, descriptionProcedure, saisie, animal, veterinairePrescripteur) VALUES (1, 10, 5, '2003-12-04', 20, 'Blessure à la patte', 'Guérir la patte', '2003-12-03', 1, 10);

INSERT INTO DossierMedical (idDossier, mesureTaille, mesurePoids, debutTraitement, dureeTraitement, ObservationGenerale, descriptionProcedure, saisie, animal, veterinairePrescripteur) VALUES (2, 100, 50, '2004-12-04', 30, 'Blessure à la tête', 'Guérir la tête', '2004-12-03', 2, 10);

INSERT INTO DossierMedical (idDossier, mesureTaille, mesurePoids, debutTraitement, dureeTraitement, ObservationGenerale, descriptionProcedure, saisie, animal, veterinairePrescripteur) VALUES (3, 100, 50, '2013-01-04', 10, 'Puce', 'Appliquer le produit anti-puce', '2013-12-03', 3, 12);



-- AFaitVet

INSERT INTO AFaitVet (veterinaire, dossier) VALUES (10, 1);

INSERT INTO AFaitVet (veterinaire, dossier) VALUES (11, 2);

INSERT INTO AFaitVet (veterinaire, dossier) VALUES (11, 3);

INSERT INTO AFaitVet (veterinaire, dossier) VALUES (12, 3);


-- AFaitAssist

INSERT INTO AFaitAssist (assistant, dossier) VALUES (7, 3);

INSERT INTO AFaitAssist (assistant, dossier) VALUES (8, 2);

INSERT INTO AFaitAssist (assistant, dossier) VALUES (9, 1);


-- ContientResultDoss

INSERT INTO ContientResultDoss (resultat, dossier) VALUES (1, 1);

INSERT INTO ContientResultDoss (resultat, dossier) VALUES (1, 2);

INSERT INTO ContientResultDoss (resultat, dossier) VALUES (2, 2);

INSERT INTO ContientResultDoss (resultat, dossier) VALUES (3, 3);

INSERT INTO ContientResultDoss (resultat, dossier) VALUES (4, 2);

INSERT INTO ContientResultDoss (resultat, dossier) VALUES (5, 3);


-- ContientMedicDoss

INSERT INTO ContientMedicDoss (medicament, dossier) VALUES ('paracetamol', 1);

INSERT INTO ContientMedicDoss (medicament, dossier) VALUES ('paracetamol', 2);

INSERT INTO ContientMedicDoss (medicament, dossier) VALUES ('amoxicillin', 2);

INSERT INTO ContientMedicDoss (medicament, dossier) VALUES ('paracetamol', 3);


-- autorisePour

INSERT INTO AutorisePour (medicament, espece) VALUES ('amoxicillin', 3);

INSERT INTO AutorisePour (medicament, espece) VALUES ('paracetamol', 1);

INSERT INTO AutorisePour (medicament, espece) VALUES ('paracetamol', 2);

INSERT INTO AutorisePour (medicament, espece) VALUES ('paracetamol', 4);

INSERT INTO AutorisePour (medicament, espece) VALUES ('paracetamol', 3);

INSERT INTO AutorisePour (medicament, espece) VALUES ('GSE', 4);


-- EstSuiviPar

INSERT INTO EstSuiviPar (animal, veterinaire, debut, fin) VALUES (1, 10, '2023-11-10', '2023-11-13');

INSERT INTO EstSuiviPar (animal, veterinaire, debut, fin) VALUES (2, 12, '2022-10-11', '2023-11-13');

INSERT INTO EstSuiviPar (animal, veterinaire, debut, fin) VALUES (3, 11, '2012-12-13', '2020-01-20');

INSERT INTO EstSuiviPar (animal, veterinaire, debut, fin) VALUES (3, 13, '2020-01-21', '2023-11-13');

INSERT INTO EstSuiviPar (animal, veterinaire, debut, fin) VALUES (4, 13, '2016-06-30', '2020-10-10');


-- EstPossedePar

INSERT INTO EstPossedePar (animal, client, debut, fin) VALUES (1, 3, '2017-08-27', '2023-11-13');

INSERT INTO EstPossedePar (animal, client, debut, fin) VALUES (2, 1, '2017-08-27', '2023-11-13');

INSERT INTO EstPossedePar (animal, client, debut, fin) VALUES (3, 3, '2014-09-24', '2022-10-08');

INSERT INTO EstPossedePar (animal, client, debut, fin) VALUES (4, 1, '2013-02-24', '2017-11-18');


SELECT * from Medicament; 
SELECT * from ResultatAnalyse;
SELECT * from Client;
SELECT * from Espece;
SELECT * from Assistant;
SELECT * from Animal;
SELECT * from Veterinaire;
SELECT * from DossierMedical; 


-- Avec des jointures

-- Les dossiers médicaux et leurs médicaments associés

SELECT * from DossierMedical dm
JOIN ContientMedicDoss cmd ON dm.idDossier = cmd.dossier
JOIN Medicament m ON cmd.medicament = m.nomMol;


-- le nom de l'espèce spécialité du vétérinaire

SELECT vet.nom, esp.intitulePrecis FROM Veterinaire vet 
JOIN Espece esp ON vet.specialite = esp.idEspece;

-- le nom de l'espèce spécialité de l'assistant

SELECT ass.nom, esp.intitulePrecis FROM Assistant ass 
JOIN Espece esp ON ass.specialite = esp.idEspece;


-- quantités de médicaments totale consommée pour chaque animal


SELECT ani.nom, dm.idDossier , dm.dureeTraitement, m.quantiteMedicamentJour from DossierMedical dm
JOIN ContientMedicDoss cmd ON dm.idDossier = cmd.dossier
JOIN Medicament m ON cmd.medicament = m.nomMol
JOIN Animal ani ON dm.animal = ani.idAnimal;



SELECT ani.nom, sum(dm.dureeTraitement * m.quantiteMedicamentJour) AS quantites_medicaments_totale from DossierMedical dm
JOIN ContientMedicDoss cmd ON dm.idDossier = cmd.dossier
JOIN Medicament m ON cmd.medicament = m.nomMol
JOIN Animal ani ON dm.animal = ani.idAnimal
GROUP BY ani.nom;

 

-- Nombre de vétérinaires

SELECT COUNT(*) AS nombre_veterinaire FROM Veterinaire;


-- Nombre de dossier médical par animal effectués dans la clinique

SELECT A.idAnimal, A.nom, COUNT(idAnimal) AS nb_dossiers FROM Animal A JOIN DossierMedical dm ON A.idAnimal = dm.animal GROUP BY A.idAnimal;


-- Nombre d'animaux de chaque espèce enregistré dans la clinique

SELECT E.typeEspece, COUNT(typeEspece) AS nombre_animaux FROM Espece E JOIN Animal A ON A.espece = E.idEspece GROUP BY typeEspece;

-- Nombre des animaux de chaque type de taille

SELECT COUNT(*) from Animal where taille = 'petite';
SELECT COUNT(*) from Animal where taille = 'moyenne';
SELECT COUNT(*) from Animal where taille = 'autre';




-- Donner les infos d'un animal à partir de son nom


SELECT * FROM DossierMedical dm JOIN Animal a ON dm.animal = a.idAnimal WHERE a.nom = 'Dori';

-- Donner les animaux d'un client à partir de son id

SELECT * FROM Animal A 
JOIN EstPossedePar EPP ON EPP.animal = A.idAnimal 
Join Espece e On e.idEspece = A.espece  
where EPP.client = 1;



-- Donner les infos d'un vétérinaire à partir de son nom

-- infos persos

SELECT prenom, nom, dateNaissance, adresse, tel, e.typeespece as specialite from Veterinaire vet
Join Espece e On e.idEspece = vet.specialite  
where idvet = 1;

-- Les dossiers médicaux que le vétérinaire a fait

SELECT prenom, nom, idDossier, saisie from DossierMedical dm
JOIN AFaitVet afv ON dm.idDossier = afv.dossier
JOIN Veterinaire vet ON vet.idVet = afv.veterinaire 
WHERE vet.idVet=1; 

-- Les animaux suivis par le vétérinaire

SELECT vet.prenom, vet.nom, ani.idAnimal, ani.nom from Animal ani
JOIN EstSuiviPar esp ON esp.animal = ani.idAnimal
JOIN Veterinaire vet ON esp.veterinaire = vet.idVet 
WHERE vet.idVet=1; 

-- Les traitements qu'ils prescrits

SELECT prenom, nom, idDossier, saisie from DossierMedical dm
JOIN Veterinaire vet ON vet.idVet = dm.veterinairePrescripteur  
WHERE vet.idVet=1; 




-- Donner le dossier médical d'un animal à partir de son nom

SELECT dm.* FROM DossierMedical dm JOIN Animal a ON dm.animal = a.idAnimal WHERE a.nom = 'Dori';

-- Donner le dossier médical d'un animal à partir de son id

SELECT dm.* FROM DossierMedical dm JOIN Animal a ON dm.animal = a.idAnimal WHERE a.idAnimal = 3 ORDER BY saisie;







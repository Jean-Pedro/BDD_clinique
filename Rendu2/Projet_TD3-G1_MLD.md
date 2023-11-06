# MLD du projet 

### Relations représentant des objets

La classe Humain étant abstraite, Personnel l'étant aussi, on opte pour un héritage par les classes filles. Celui-ci se révèle d'autant plus judicieux que les différente classes filles entretiennent des relations qui leur sont propres avec d'autres relations. 
Toutes ces classes étant dépourvues de clé naturelle, on leur en crée une.

Par défaut, on considère tous les attributs not null.

Ainsi, on a : -

**Vétérinaire** (#idVet : entier, nom: string, prenom : string, dateNaissance : date, adresse : string, tel : string, specialité=>Especes)
avec : specialité qui peut être NULL

**Assistant** (#idAssist : entier, nom: string, prenom : string, dateNaissance : date, adresse : string, tel : string, specialité=>Espece)
avec : specialité qui peut être NULL

**Client** (#idClient : entier, nom: string, prenom : string, dateNaissance : date, adresse : string, tel : string)

De plus, nous avons également : 

**Médicament**(#nomMol : string, description : string, quantitéMédicamentJour : int)

**DossierMédical**(#idDossier : entier, mesureTaille : entier, mesurePoids : entier, debutTraitement : date, duréeTraitement : entier, observationGénérale : string, descriptionProcédure : string, saisie : date, animal=>Animal, vétérinairePrescripteur=>Vétérinaire)

**Espece**(#typeEspece : string, intitulePrecis : string)
avec : typeEspece IN {félin, canidé, reptile, rongeur, oiseau, autre}
avec : intitulePrecis=NULL X typeEspece=autre
avec : intitulePrecis NULL

**ResultatAnalyse**(#idResultat: entier, lien: string)

**Animal**(#idAnimal : entier, nom: string, espece=>Espece, numPuceId : entier, numPasseport: entier, taille: string)
avec taille IN {petite, moyenne, autre}
avec : numPuceId NULL, numPasseport: NULL




### Relations représentant des associations

**AFaitVet**(#vétérinaire=>Vétérinaire, #dossier=>DossierMédical)
**AFaitAssist**(#assitant=>Assistant, #dossier=>DossieMédical)

**ContientResultDoss**(#resultat=>Resultat, #dossier=>DossierMédical)
**ContientMedicDoss**(#médicament=>Médicament, #dossier=>DossierMédical)

**autorisePour**(médicament=>Médicament, espèce=>Espèce)

**EstPossédéPar**(animal=>Animal, client=>Client, début : date, fin : date)

**EstSuiviPar**(animal=>Animal, vétérinaire=>Vétérinaire, début : date, fin : date)


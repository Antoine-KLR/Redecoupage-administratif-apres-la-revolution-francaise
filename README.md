# Réorganisation administrative pendant la révolution française

Instructions pour reproduire la chaine de traitement (extraction, structuration, désambiguïsation) : 

## Pré-requis : 

Système d'exploitation : Windows 32 ou 64 bits. Les logiciels suivant seront nécessaires : Unitex-Gramlab, SPARQL-Generate, 



### Installeurs : 

Unitex : https://unitexgramlab.org/fr

Sparql-Generate : https://ci.mines-stetienne.fr/sparql-generate/standalone-app.html

GraphDB : https://www.ontotext.com/products/graphdb/editions/

Silk - The Linked Data Integration Framework : http://silkframework.org/download (utiliser le workbench)

Python 2.7 : https://www.python.org/downloads/


## 1ère Partie : Extraction

La première phase de cet outil consiste à extraire les informations géographiques et les relations des textes. Pour ce faire nous utilisons Unitex ainsi qu'un ensemble de grammaires organisées en cascades. Les fichiers de configuration sont disponibles dans le dossier "1.Grammaires"

Installations : 

1. Installer Unitex, spécifier le dossier utilisateur.
2. Extraire le contenu de l'archive *fichiers à extraire.zip* ("1.Grammaires") dans le dossier utilisateur d'Unitex (généralement localisé à "C:\\*Username*\Documents\Unitex-GramLab\Unitex\French\").

Instructions : 

1. Exécuter le logiciel Unitex Visual IDE.
2. Ouvrir un texte.
3. Décocher tous dans la boite de dialogue.
4. dans Fichier > Apply Lexical Ressources, sélectionner *chefslieux.bin* et *toponyms.bin*, cliquer sur *set default* puis sur *apply*
5. Appliquer les cascades dans l'ordre.



## 2ème Partie : Structurer les données

Dans cette partie, nous allons voir comment structurer nos données et passer d'un fichier xml à un graph requêtable avec le langage SPARQL. Nous utiliserons les logiciels Sparql-Generate et GraphDB.





## 3ème Partie : Désambiguïser les noms de lieux et les afficher.

Ici nous utiliserons le code python et nous pourrons visualiser nos résultats à l'aide d'un SIG (par exemple QGIS).




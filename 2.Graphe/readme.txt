Mode d'emploi pour la création du graphe de connaissance à l'aide de sparql-generate : 


La construction du graphe de connaissance se fait grâce à 4 requêtes SPARQL (cf requêtes.txt). 
  - ESN et leurs attributs (types, noms, évolutions)
  - Leurs relations (fusion et séparation)
  - localisation dans le texte des ESN (n° article et décret)
  - localisation dans le texte des ESN pour ceux en dehors d'un décret
  
  

A utiliser avec le "SPARQL-Generate Standalone Application", en renommant le fichier xml "input.xml" et en vérifiant dans le fichier de configuration "sparql-generate-conf.json" que stream soit sur true. Le fichier de configuration est donné ici.





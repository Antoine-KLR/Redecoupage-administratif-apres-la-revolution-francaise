# coding: utf-8
from SPARQLWrapper import SPARQLWrapper, N3
from  rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL
import numpy as np
from shapely.wkt import loads
import shapely.geometry
#import fiona

#prefix
GHD = Namespace("http://data.geohistoricaldata.org/def/statutadmin#")
GHS = Namespace("http://data.geohistoricaldata.org/def/places#")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
# cd C:/Python27 && python.exe "C:\Users\Adminlocal\Desktop\desambig python\main.py"

#PREFIX ghd: <http://data.geohistoricaldata.org/def/statutadmin#>
#	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#	PREFIX ghs: <http://data.geohistoricaldata.org/def/places#>
#	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#	PREFIX dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#>
#	PREFIX geo: <http://www.opengis.net/ont/geosparql#>


"""
recupération des geometrie des candidats cassini d'une esn donnee en parametre.
"""
def recupGeomCandidat(esn):
	g = Graph()	
	for c in gMapping[esn : OWL.sameAs]:
		[g.add( (c, GEO.geometry, geom) ) for geom in gCassini[c : GEO.geometry]]
	return g
	
def recupAutresCandidats(esn, decret, dic):
	esnautre = list(dic[decret])
	esnautre.remove(esn)
	g = Graph()
	for i in esnautre:
		g+= recupGeomCandidat(i)
	return g
	
def calculScore(candidat, gAutres):
	cGeom =  loads(candidat[2])
	L = []
	for aWKT in gAutres[None : GEO.geometry] :
		aGeom = loads(str(aWKT[1]))
		L.append(cGeom.distance(aGeom))
	return candidat[0], np.median(L)
	
def exportPlacesToShape(places, path):
	schema = {
		'geometry' : 'Point',
		'properties':{}
	}
	#with fiona.open(path, 'w', 'ESRI Shapefile', schema) as c : 
	#	for wkt in gCassini[place : GEO.geometry]:
	#		c.write({
	#		'geometry': mapping(loads(wkt)), 
	#		'properties': {}
	#		})
		
		

def queryGraph(query):
	sparql.setQuery(query)
	sparql.setReturnFormat(N3)
	results = sparql.query().convert()
	g = Graph()
	g.parse(data=results, format="n3")
	return g

def boucleDecret():
	gResult = Graph()
	esntrouv = 0
	esnfalse = 0
	for decret in dic:
		print "decret courant :  " + decret
		for esn in dic[decret]:
			gCandidats = recupGeomCandidat(esn)
			
			#exportPlacesToShape(list(gCandidats.subjects()))
			gAutres = recupAutresCandidats(esn, decret, dic)
			scores = []
			uris = []
			for c in gCandidats:
				uri, score = calculScore(c, gAutres)
				uris.append( uri)
				scores.append( score)
			if scores:
				esntrouv+=1
				best_candidate =  uris[np.argmin(scores)]
				#print esn + '-->'+best_candidate +' (' +str(np.min(scores)) + ')'	
				gResult.add((esn, OWL.sameAs, best_candidate))
				gResult.add((esn, GHD.hasScore, Literal(np.min(score))))
				gResult.add((esn, GHD.hasSuccess, Literal(True)))
			else: 
				esnfalse+=1
				best_candidate = None
				gResult.add((esn, GHD.hasSuccess, Literal(False)))
			print str(esn)
	print "nb esn trouve :  " + str(esntrouv) + "   " + str(esntrouv*100./522) + "%"
	print "nb esn false :   " + str(esnfalse) + "    " + str(esnfalse*100./(esnfalse+esntrouv)) + "%"
	return gResult
	
		
		

""" MAIN """
repos = "http://127.0.0.1:7200/repositories/desambig_final"
sparql = SPARQLWrapper(repos)


gMapping = Graph()		
gMapping = queryGraph("""
		CONSTRUCT {
			?s ?p ?o .
		} 
		FROM <http://data.geohistoricaldata.org/id/mapping/>
		WHERE { ?s ?p ?o }
	""")
print "success mapping"
gCassini = Graph()		
gCassini = queryGraph("""
	PREFIX geo: <http://www.opengis.net/ont/geosparql#>
	CONSTRUCT {
		?s geo:geometry ?o .
	} 
	FROM <http://data.geohistoricaldata.org/id/cassini/>
	WHERE { ?s geo:geometry ?o }
""")
print "success cassini"
gDecret = Graph()		
gDecret = queryGraph("""
	PREFIX ghd: <http://data.geohistoricaldata.org/def/statutadmin#>
	CONSTRUCT {
		?s ghd:inArticle ?o .
	} 
	FROM <http://data.geohistoricaldata.org/id/decret/>
	WHERE { ?s ghd:inArticle ?o }
""")
print "success decret"


# Group all ESNs by their decret
dic=dict()
for esn, p, decret in gDecret :
	decret_str = str(decret)
	if decret_str not in dic:
		dic[decret_str] = []
	dic[decret_str].append(esn)
	
	
g = Graph()
g = boucleDecret()	
g.serialize(destination='result.ttl', format='turtle')
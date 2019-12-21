from sparqlpy import *


ENDPOINT = "http://127.0.0.1:3030/neo/sparql"
s = SparqlEndpoint(ENDPOINT)

q = "select ?x where {?x a owl:Class}"
results = s.query(q)

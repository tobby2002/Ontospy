import ontospy
# from .core import *
# from .core.utils import *

ENDPOINT = "http://127.0.0.1:3030/neo/sparql"

o = ontospy.Ontospy(sparql_endpoint=ENDPOINT, verbose=True)
# o.build_all()


print(o), print("---------")
q = o.query("select distinct ?b where {?x a ?b} limit 30")
if q:
    for el in q:
        print(el)
else:
    print("No results")

getOntology = o.sparqlHelper.getOntology()




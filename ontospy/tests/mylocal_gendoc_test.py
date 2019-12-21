import ontospy
from ontospy.ontodocs.viz.viz_html_single import *


import ontospy
ENDPOINT = "http://127.0.0.1:3030/neo/sparql"
model = ontospy.Ontospy(sparql_endpoint=ENDPOINT, verbose=True)
model.build_all()


v = HTMLVisualizer(model) # => instantiate the visualization object
v.build() # => render visualization. You can pass an 'output_path' parameter too
v.preview() # => open in browser

import ontospy
import multitasking
import time
ENDPOINT = "http://127.0.0.1:3030/neo/sparql"
model = ontospy.Ontospy(sparql_endpoint=ENDPOINT, verbose=True)
# model.build_all()

@multitasking.task
def show(model):
    start = time.time()
    model.build_classes()

    # print(model.all_classes)
    print(model.all_properties_object)
    print(model.printClassTree())
    print(model.toplayer_classes)

    doc_class_l = model.get_class('document')
    print(doc_class_l)


    c1 = doc_class_l[1]

    print(c1.rdf_source())
    print(c1.parents())
    print(c1.children())
    print('taken time: %s ' % (time.time() - start))
show(model)



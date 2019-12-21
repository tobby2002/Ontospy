# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit test stub for ontosPy

Run like this:

:path/to/ontospyProject>python -m ontospy.tests.test_sparql

"""

from __future__ import print_function

import unittest, os, sys
from .. import *
from ..core import *
from ..core.utils import *



# sanity check
print("-------------------\nOntospy ",  VERSION, "\n-------------------")



class TestSparqlStore(unittest.TestCase):

    ENDPOINT = "http://dbpedia.org/sparql"

    def test1_load_dbpedia(self):

        """
        Check if the dbpedia endpoint loads ok
        "http://dbpedia.org/sparql"
        """
        printDebug("=================\nTEST: Loading <%s> endpoint.\n=================" % self.ENDPOINT, "important")

        o = Ontospy(sparql_endpoint=self.ENDPOINT, verbose=True)

        print(o), print("---------")

        q = o.query("select distinct ?b where {?x a ?b} limit 30")
        if q:
            for el in q:
                print(el)
        else:
            print("No results")

        getOntology = o.sparqlHelper.getOntology()

        printDebug("=================\nTEST: sparqlHelper.\n=================")
        print("-- getOntology----")
        print('-- getOntology:%s' % getOntology)

        # getAllProperties = o.sparqlHelper.getAllProperties()
        # print("-- getAllProperties----")
        # print('-- getAllProperties:%s' % getAllProperties)

        # getAllClasses = o.sparqlHelper.getAllClasses()
        # print("-- getAllClasses----")
        # print('-- getAllClasses:%s' % getAllClasses)

        # getShapes = o.sparqlHelper.getShapes()
        # print("-- getShapes----")
        # print('-- getShapes:%s' % getShapes)

        aURI = 'http://www.openlinksw.com/schemas/virtrdf#QuadMapFormat'
        entityTriples = o.sparqlHelper.entityTriples(aURI=aURI)
        print("-- entityTriples----")
        print('-- entityTriples:%s' % entityTriples)

        # getClassAllSubs = o.sparqlHelper.getClassAllSubs(aURI=aURI)
        # print("-- getClassAllSubs----")
        # print('-- getClassAllSubs:%s' % getClassAllSubs)
        #
        # ontologyClassTree = o.ontologyClassTree()
        # print("-- ontologyClassTree----")
        # print('-- ontologyClassTree:%s' % ontologyClassTree)

        # aURI = 'http://www.openlinksw.com/schemas/virtrdf#QuadMapFormat'
        # printPropertyTree = o.printPropertyTree()
        # print("-- printPropertyTree----")
        # print('-- printPropertyTree:%s' % printPropertyTree)

        toplayer_classes = o.toplayer_classes
        print("-- toplayer_classes----")
        print('-- toplayer_classes:%s' % toplayer_classes)

        toplayer_classes = o.toplayer_classes
        print("-- toplayer_classes----")
        print('-- toplayer_classes:%s' % toplayer_classes)

if __name__ == "__main__":
    unittest.main()


from rdflib import Namespace, Literal, URIRef, ConjunctiveGraph, Namespace
from random import choice
from string import ascii_letters

class RDFFile:
    emBase = "http://www.mozilla.org/2004/em-rdf#%s"
    rdfBase = "http://www.w3.org/1999/02/22-rdf-syntax-ns#%s"

    def _genURI(self):
        id = "rdf:"
        for i in xrange(0,8):
            id += choice(ascii_letters)
        return id

    def em(self, id):
        return URIRef(self.emBase % id)

    def rdf(self, id):
        return URIRef(self.rdfBase % id)

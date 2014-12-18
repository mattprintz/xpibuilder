"""
Update interface

The Update module creates new
"""

from rdflib import Namespace, Literal, URIRef, ConjunctiveGraph, Namespace
from RDFFile import RDFFile
import hashlib


class Update(RDFFile):
    """
    TODO: Add documentation
    """

    RDFBASE = "urn:mozilla:extension:%s"

    def __init__(self, package, xpiFile, urlBase):
        self.package = package
        self.id = package.install.get('id')
        self.basename = package.basename
        self.version = package.install.get('version')
        self.graph = ConjunctiveGraph()
        self.graph.bind('em', Namespace('http://www.mozilla.org/2004/em-rdf#'))

        self.urlBase = urlBase

        self.baseUri = URIRef(self.RDFBASE % self.id)
        self.versionUri = URIRef(self.RDFBASE % "%s:%s" % (self.id, self.version))

        self.updateUri = URIRef(self._genURI())
        self.updateList = URIRef(self._genURI())

        self.graph.add((self.baseUri, self.em('updates'), self.updateList))
        self.graph.add((self.updateList, self.rdf("type"), self.rdf("Seq")))
        self.graph.add((self.updateList, self.rdf("li"), self.versionUri))
        self.graph.add((self.versionUri, self.em('version'),
                        Literal(self.version)))
        self.graph.add((self.versionUri, self.em('targetApplication'),
                        self.updateUri))

        for id, minVersion, maxVersion in self.package.install.getTargets():
            self.graph.add((self.updateUri, self.em('id'), Literal(id)))
            self.graph.add((self.updateUri, self.em('minVersion'),
                            Literal(minVersion)))
            self.graph.add((self.updateUri, self.em('maxVersion'),
                            Literal(maxVersion)))
            self.graph.add((self.updateUri, self.em('updateLink'),
                            Literal(URLBASE % xpiFile)))
            self.graph.add((self.updateUri, self.em('updateHash'),
                            Literal("sha512:%s" % self._sha512sum(xpiFile))))

    def save(self, fileName=None):
        if fileName is None:
            fileName = "%s-%s.rdf" % (self.basename, self.version)
        with open(fileName, "w") as f:
            f.write(self.graph.serialize())
        return fileName

    def _sha512sum(self, fileName):
        sha512 = hashlib.sha512()
        with open(fileName) as f:
            for line in f.readlines():
                sha512.update(line)
        return sha512.hexdigest()

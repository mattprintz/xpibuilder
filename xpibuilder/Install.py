
from rdflib import Namespace, Literal, URIRef, ConjunctiveGraph, Namespace
from RDFFile import RDFFile

class Install(RDFFile):
    def __init__(self, file):
        self.graph = ConjunctiveGraph()
        self.subject = URIRef("urn:mozilla:install-manifest")
        self.graph.load(file)
    
    def serialize(self):
        return self.graph.serialize()
    
    def get(self, name):
        predicate = self.em(name)
        objects = []
        for o in self.graph.objects(self.subject, predicate):
            objects.append(str(o))
        if len(objects) == 0:
            return None
        elif len(objects) == 1:
            return objects[0]
        else:
            return objects

    def setLiteral(self, name, value):
        predicate = self.em(name)
        tuple = (self.subject, predicate, Literal(value))
        self.graph.set(tuple)

    def setArray(self, name, list):
        predicate = self.em(name)
        self.graph.remove((self.subject, predicate, None))
        for value in list:
            self.graph.add((self.subject, predicate, Literal(value)))
    
    def getTargets(self):
        targets = []
        targetSubjects = self.get('targetApplication')
        if isinstance(targetSubjects, str):
            targetSubjects = [targetSubjects]
        for target in targetSubjects:
            id = str(self.graph.objects(URIRef(target), self.em("id")).next())
            minVersion = str(self.graph.objects(URIRef(target), self.em("minVersion")).next())
            maxVersion = str(self.graph.objects(URIRef(target), self.em("maxVersion")).next())
            targets.append((id, minVersion, maxVersion))
        return targets
    
    def clearTargets(self):
        targetSubjects = self.get('targetApplication')
        if isinstance(targetSubjects, str):
            targetSubjects = [targetSubjects]
        for target in targetSubjects:
            self.graph.remove((URIRef(target), None, None))
        self.graph.remove((self.subject, self.em('targetApplication'), None))
    
    def addTarget(self, id, minVersion, maxVersion):
        # Do/while approximation to ensure we have a unique ids
        unique = False
        while not unique:
            try:
                uri = URIRef(self._genURI())
                check = self.graph.triples((uri, None, None))
                check.next()
            except StopIteration:
                unique = True
        self.graph.add((uri, self.em("id"), Literal(id)))
        self.graph.add((uri, self.em("minVersion"), Literal(minVersion)))
        self.graph.add((uri, self.em("maxVersion"), Literal(maxVersion)))
        self.graph.add((self.subject, self.em("targetApplication"), uri))

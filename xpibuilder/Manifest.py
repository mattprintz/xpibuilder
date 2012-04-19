

class ManifestEntry:
    def __init__(self, provider, flags):
        self.provider = provider
        self.flags = flags
    
    def __str__(self):
        return "%s %s" % (self.provider, " ".join(self.flags))

    def setJar(self, jarIdent):
        needsProcess = False
        target = None
        if self.provider == "content":
            target = 1
        elif self.provider in ["skin", "locale"]:
            target = 2
        if target is not None:
            origLocation = self.flags[target]
            newLocation = "jar:chrome/%s!/%s" % (jarIdent, origLocation)
            self.flags[target] = newLocation

class Manifest:
    def __init__(self, file):
        self.entries = []
        manifestFile = open(file, "r")
        lines = manifestFile.readlines()
        for line in lines:
            data = line.split()
            if data:
                provider = data[0].lower()
                flags = data[1:]
                entry = ManifestEntry(provider, flags)
                self.entries.append(entry)
    
    def jarDirs(self):
        dirs = {}
        for entry in self.entries:
            if(entry.provider in ('content', 'skin', 'locale')):
                dirs[entry.provider] = None
        return dirs.keys()
    
    def serialize(self):
        return "\n".join([str(entry) for entry in self.entries])
    
    def setJar(self, jarIdent):
        for entry in self.entries:
            entry.setJar(jarIdent)



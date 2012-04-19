"""\
Package interface

The Package module is used to build an XPI package.
"""

import os
import zipfile
import shutil
from xpibuilder.Install import Install
from xpibuilder.Manifest import Manifest

class Package:
    """
    TODO: Add documentation
    """
    
    def __init__(self, basename, dataDir, buildDir=None):
        self.basename = basename
        self.dataDir = dataDir
        if not os.path.exists(dataDir):
            raise IOError('Datadir not found')
        if buildDir is None:
            self.buildDir = os.path.join(self.dataDir, "build")
        else:
            self.buildDir = buildDir
        self.manifest = Manifest(os.path.join(self.dataDir, "chrome.manifest"))
        self.install = Install(os.path.join(self.dataDir, "install.rdf"))
        
        if os.path.exists(self.buildDir):
            shutil.rmtree(self.buildDir)
        os.makedirs(self.buildDir)
    
    def createJar(self, jarName=None):
        if jarName is None:
            jarName = "%s.jar" % self.basename
        
        chromeDir = os.path.join(self.buildDir, 'chrome')
        if not os.path.exists(chromeDir):
            os.makedirs(chromeDir)
        jarFile = zipfile.ZipFile(os.path.join(chromeDir, jarName), 'w', zipfile.ZIP_STORED, False)
        
        ignore = shutil.ignore_patterns('.*')
        jarDirs = self.manifest.jarDirs()
        
        for dir in jarDirs:
            shutil.copytree(os.path.join(self.dataDir, dir), os.path.join(self.buildDir, dir), False, ignore)
            for dirpath, dirs, files in os.walk(os.path.join(self.buildDir, dir)):
                if dirpath != chromeDir:
                    for file in files:
                        relPath = os.path.join(dirpath, file)
                        zipPath = os.path.join(os.path.relpath(dirpath, self.buildDir), file)
                        jarFile.write(relPath, zipPath)
        
        jarFile.close()
        
        # Remove redundant directories
        for dir in jarDirs:
            shutil.rmtree(os.path.join(self.buildDir, dir))
        self.manifest.setJar(jarName)
    
    
    def updateManifest(self):
        newManifest = open(os.path.join(self.buildDir, 'chrome.manifest'), 'w')
        newManifest.write(self.manifest.serialize())
        newManifest.close()
    
    def createXPI(self, outDir=None, xpiName=None):
        if outDir is None:
            outDir = "."
        if xpiName is None:
            xpiName = "%s-%s.xpi" % (self.basename, self.install.get('version'))
        
        ignore = shutil.ignore_patterns('.*')
        defaults = ['defaults', 'modules', 'install.rdf']
        if os.path.exists(os.path.join(self.dataDir, '.xpiinclude')):
            defaults += [ filename.rstrip() for filename in open(os.path.join(self.dataDir, '.xpiinclude')).readlines()]
        
        for item in defaults:
            src = os.path.join(self.dataDir, item)
            if os.path.isdir(src):
                shutil.copytree(src, os.path.join(self.buildDir, item), False, ignore)
            else:
                shutil.copy2(src, os.path.join(self.buildDir, item))
        
        self.updateManifest()
        
        xpiFile = zipfile.ZipFile(os.path.join(outDir, xpiName), 'w', zipfile.ZIP_DEFLATED, False)
        for dirpath, dirs, files in os.walk(os.path.join(self.buildDir)):
            for file in files:
                relPath = os.path.join(dirpath, file)
                zipPath = os.path.join(os.path.relpath(dirpath, self.buildDir), file)
                xpiFile.write(relPath, zipPath)
        xpiFile.close()
        return xpiName

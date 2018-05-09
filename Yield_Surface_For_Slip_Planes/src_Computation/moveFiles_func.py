# -*- coding: utf-8 -*-
def moveFiles (name, destDir):
	rootDir = os.getcwd()
	for root, dirs, files in os.walk(rootDir):
		if (root== rootDir) :
			for i in range(len(files)):
				x = files[i].find(name)
				if x==0 :
					print files[i]
					shutil.move( files[i], destDir)

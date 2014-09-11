from optparse import OptionParser
import importlib
import os
import re
import inspect

if __name__ == "__main__":
	parser = OptionParser()

	parser.add_option("-g", "--gui", dest="guifile", default=None, help="Which GUI file to process. Warning this file will be changed")
	parser.add_option("-a", "--app", dest="appfile")

	(options, args) = parser.parse_args()

	print("GUI file: %s" % options.guifile)
	print("APP file: %s" % options.appfile)

	appname = options.appfile.split('.')[0]

	print("APP name: %s" % appname)

	i = importlib.import_module(appname)

	classname = dir(i)[0]

	mainclass = eval("i.%s" % classname)

	ClassDefinition = "self.Application = %s(self)" % classname

	print(ClassDefinition)

	ListOfFunctions = dir(mainclass)

	NameDict = {'class Ui_Dialog(object):':'class Ui_Dialog(object):\n    Application = None\n    def __init__(self):\n        %s' % ClassDefinition}
	#NameDict = {'class Ui_Dialog(object):':'class Ui_Dialog(object):\n    %s' % ClassDefinition}
	NameDict['from PyQt4 import QtCore, QtGui'] = 'from PyQt4 import QtCore, QtGui\nfrom %s import *' % appname

	for function in ListOfFunctions:
		obj = eval("i.%s.%s" % (classname, function))

		if not function.startswith("__") and inspect.ismethod(obj):
			fromName = "%s.%s" % ("Dialog", function)
			toName = "self.%s.%s" % ("Application", function)

			print("%s to %s" % (fromName, toName))

			NameDict[fromName] = toName

	#print NameDict

	try:
		f = open(options.guifile, "rb")
	except IOError:
		raise IOError("Could not read GUI file: %s" % (options.guifile))

	GUIFileContent= f.read()
	f.close()

	for key, value in NameDict.items():
		GUIFileContent = GUIFileContent.replace(key, value)

	#print GUIFileContent

	res = re.findall('Dialog\.[a-zA-Z]*\)', GUIFileContent)
	if len(res) > 0:
		for function in res:
			print "\nERROR: GUI calling undefined function: %s.%s(...)\n" % (classname, function[:-1].split('.')[1])

	try:
		if not os.path.exists(options.guifile):
			f = open(options.guifile, "wb")
			f.write(GUIFileContent)
		else:
			f = open(options.guifile, "rb")
			current_GUIFileContent = f.read()
			if not current_GUIFileContent == GUIFileContent:
				f.close()
				f = open(options.guifile, "wb")
				f.write(GUIFileContent)
		f.close()
	except IOError:
		raise IOError("Could not write file: %s" % (options.guifile))

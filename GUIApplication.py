import sys

class MainApplication(object):
	ui = None
	number = 0
	def __init__(self, gui=None):
		self.ui = gui
	def SendMessage(self):
		print("Sending a message from the GUI to console")
	def SetNumber(self, number):
		#print("Number: %u" % number)
		self.ui.progressBar.setValue(number)
	def MyTest(self):
		self.ui.label.setText("%u" % self.number)
		self.number += 1
	def ManualOverride(self, pushed):
		print "Manual override:",
		print pushed
	def SomeTextEntered(self):
		print "Hei %s" % self.ui.name.text()

if __name__ == "__main__":
	from GUI import *
	from PyQt4 import QtGui

	app = QtGui.QApplication(sys.argv)
	Dialog = QtGui.QDialog()
	ui = Ui_Dialog()
	ui.setupUi(Dialog)

	Dialog.show()
	sys.exit(app.exec_())


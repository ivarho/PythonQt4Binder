#echo on

#INPUT FILES
QT4_UI = mygui.ui
TARGET_APP = GUIApp.py
TARGET_GUI = GUI.py

#TOOLCHAIN
PYTHON = python
PYUIC = pyuic4
GUI_BINDER = ../GUIBinder.py

all: $(TARGET_APP)

$(TARGET_APP): $(TARGET_GUI)
	$(PYTHON) $(GUI_BINDER) -g $(TARGET_GUI) -a $(TARGET_APP)

$(TARGET_GUI): $(QT4_UI)
	$(PYUIC) -x -o $(TARGET_GUI) $(QT4_UI)

run: all
	$(PYTHON) $(TARGET_APP)

clean:
	rm -f $(TARGET_GUI) *.pyc

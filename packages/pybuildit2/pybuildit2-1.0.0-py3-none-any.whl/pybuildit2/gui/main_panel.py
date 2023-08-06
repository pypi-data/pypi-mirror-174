import os
from tkinter import *
import tkinter as Tk
import tkinter.ttk as ttk
from pybuildit2.gui.graph_tab import GraphTab
from pybuildit2.gui.config_tab import ConfigTab
from pybuildit2.gui.log_tab import LogTab
from pybuildit2.gui.init_tab import InitTab
from pybuildit2.gui.control_tab import ControlTab
from pybuildit2.gui.util import *

class MainPanel(Tk.Frame):

    def __init__(self, buildit, master):
        Tk.Frame.__init__(self, master)
        self.buildit = buildit

        self.add_tab()

    def add_tab(self, event=None):
        isUnsafeMode = builditGuiInfo.isUnsafeBuildit
        note = ttk.Notebook(self, width=700, height=660)
        if isUnsafeMode:
            note.add(InitTab(self.buildit, note), text = "Init")
        note.add(ControlTab(self.buildit, note), text = "Control")
        if isUnsafeMode:
            note.add(ConfigTab(self.buildit, 'unsafe-servo.yml', True, note), text = "ServoParam")
        else:
            note.add(ConfigTab(self.buildit, 'servo.yml', True, note), text = "ServoParam")
        note.add(ConfigTab(self.buildit, 'system.yml', False, note), text = "SystemParam")

        note.add(LogTab(self.buildit, note), text = "Log")

        note.add(GraphTab(self.buildit, note), text = "Graph")

        note.pack(fill="both", expand=True)

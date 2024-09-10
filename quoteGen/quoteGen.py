
"""
This script provides a simple quote generator UI in Maya.
It displays random quotes from a text file.
I created it when I was learning Python as a fun project.

1. Place the 'quoteGen' folder in your Maya scripts directory(e.g., C:/Users/your_username/Documents/maya/scripts/).
2. In Maya's script editor, python tab run the following commands:
    quoteGen import quoteGen
    quoteGen.QuoteWindow(quoteGen.QuoteGenerator()).create_ui()
"""

import random
import maya.cmds as cmds
import os

file_path = os.path.join(os.path.dirname(__file__), 'quotes.txt')

class QuoteGenerator:
    def __init__(self):
        # Load quotes from the file
        with open(file_path, 'r', encoding='utf-8') as file:
            self.quotes = [line.strip() for line in file.readlines()]

    def get_random_quote(self):
        return random.choice(self.quotes)

class QuoteWindow:
    def __init__(self, quote_generator):
        self.quote_generator = quote_generator
        self.window_name = 'quoteGeneratorWindow'

    def create_ui(self):
        # Delete window if exists
        if cmds.window(self.window_name, ex=True):
            cmds.deleteUI(self.window_name, window=True)

        # Create window
        cmds.window(self.window_name, t='Quote Generator', s=False)
        cmds.columnLayout(adjustableColumn=True)
        self.label = cmds.text(l='', align='center', font='boldLabelFont', h=100, bgc=[0.1, 0.1, 0.1])
        cmds.separator(style="in")

        # Create a button to generate random quotes
        self.button = cmds.button(l='Generate Quote', c=self.show_random_quote, w=600, h=30, bgc=[0.2, 0.2, 0.2])
        cmds.separator(style="in")
        cmds.showWindow(self.window_name)

    def show_random_quote(self, *args):
        random_quote = self.quote_generator.get_random_quote()
        cmds.text(self.label, edit=True, l=random_quote)

        


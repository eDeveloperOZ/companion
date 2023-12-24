# src/app.py
from translator import ChannelTranslator
from duplicate_scanner import DuplicateScanner

class App:
    def __init__(self):
        self.translator = ChannelTranslator()
        self.scanner = DuplicateScanner()

    def run(self):
        self.translator.start()
        self.scanner.start()

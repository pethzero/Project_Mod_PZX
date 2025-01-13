import os

class HotkeyManager:
    def __init__(self, base_list):
        self.base_list = base_list 

    def fnis_list(self, head):
        return [f"{head} {item.replace('.hkx', '').lower()} {item}" for item in self.base_list]
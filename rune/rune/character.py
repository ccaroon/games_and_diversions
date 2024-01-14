import yaml

from scriptum.inventory import Inventory

class Character:
    def __init__(self, path):
        data = yaml.safe_load(path)

        __location = None

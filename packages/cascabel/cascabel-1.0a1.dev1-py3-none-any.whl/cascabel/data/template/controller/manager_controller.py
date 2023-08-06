from flask import *

class NAME:

    def index(self):  
        return "NAME: index"

    def view(self, id):
        return f"NAME: view {id}"

    def store(self):
        return f"NAME: store {id}"

    def update(self, id):
        return f"NAME: update {id}"

    def delete(self, id):
        return f"NAME: delete {id}"


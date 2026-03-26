class Tool:
    def __init__(self, name, desc):
        self.name = name
        self.description = desc
        
    def run(self):
        raise NotImplementedError("Tool must implement run()")
class Task:
    def __init__(self,
            id: int,
            description: str,
            dependedOn: list         
        ):
        self.id = id
        self.description = description
        self.dependedOn = dependedOn
        self.status = 'pending'
        self.result = ''
    
        
    def updateTask(self, result):
        self.status = 'completed'
        self.result = result
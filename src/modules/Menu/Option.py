class Option:
    def __init__(self, identifier, funct) -> None:
        self.funct = funct
        self.identifier = identifier

    def call(self, *args):
        return self.funct(*args)
    
    def __str__(self) -> str:
        return self.identifier
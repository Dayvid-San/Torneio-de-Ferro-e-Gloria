from Game.characters.personagem import Personagem
class Cavaleiro(Personagem):
    def __init__(self, fisica, magia):
        super().__init__(fisica, magia)
    
    def FraseDeEfeito(self):
        print("Pela honra do Rei, eu te anularei")
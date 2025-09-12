from personagem import Personagem
class Mago(Personagem):
    def __init__(self, fisica, magia):
        super().__init__(fisica, magia)
    
    def FraseDeEfeito(self):
        print("Eu sou dos magos, o mais poderoso")
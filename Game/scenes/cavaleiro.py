from personagem import Personagem
class Cavaleiro(Personagem):
    def __init__(self, fisica, magia):
        super().__init__(fisica, magia)
    
    def FraseDeEfeito():
        print("Pela honra do Rei, eu te anularei")
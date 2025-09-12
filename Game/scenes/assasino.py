from personagem import Personagem
class Assasino(Personagem):
    def __init__(self, fisica, magia):
        super().__init__(fisica, magia)

    def FraseDeEfeito(self):
        print("Eu lhe caçarei até a morte")
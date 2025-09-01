#Classe Filha, herdara de Personagem, a ideia é fazer uma tela de select com Personagens pré-definidos antes.
from jogador import Jogador
#Classe Filha, herdara de Personagem, a ideia é fazer uma tela de select com Personagens pré-definidos antes.
class Cavaleiro(Jogador):
    def __init__(self, nome: str):
        super().__init__(nome, vida_max=120, ataque=8, defesa=12)

        # Metodo de Ataque 
    def RealizarAtaque(self): # Metodo Personalizado da Classe Cavaleiro
        pass

    # Metodo de Dano 
    def ReceberDano(self): # Metodo Personalizado da Classe Cavaleiro
        pass

from jogador import Jogador
#Classe Filha, herdara de Personagem, a ideia é fazer uma tela de select com Personagens pré-definidos antes.
class Mago(Jogador):
    def __init__(self, nome: str):
        super().__init__(nome, vida_max=70, ataque=15, defesa=5)

    # Metodo de Ataque 
    def RealizarAtaque(self): # Metodo Personalizado da Classe Mago
        pass

    # Metodo de Dano
    def ReceberDano(self): # Metodo Personalizado da Classe Mago
        pass
    # não sei se essas metodos serão necessarias depois 

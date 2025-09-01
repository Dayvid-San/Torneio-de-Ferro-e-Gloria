from personagem import Personagem

class Boss(Personagem):
    def __init__(self, nome: str, vida_max: int,  ataque: int, defesa: int, numeroAtaques: int, nivel: int):
        super().__init__(nome, vida_max,  ataque, defesa)
        self.__numeroAtaques = numeroAtaques # Atributo para definir o número de dificuldade do BOSS conforme o nível da torre
        self.__nivel = nivel

    def getNumeroAtaques(self):
        return self.__numeroAtaques
    
    def setNumeroAtaques(self, NovoNumeroAtaques):
        self.__numeroAtaques = NovoNumeroAtaques
        return self.__numeroAtaques
    
    def escolher_acao(self, jogador_alvo):
        self.atacar(jogador_alvo)

    # Metodos do Polimorfismo
    # Mudar Ataque e Defesa conforme o nivel do Boss (1 a 5)
    # No caso dos metodos polimorfos dos herois será pelo tipo de heroi (Ataque do Mago, do Cavaleiro, do Assassino)
    def RealizarAtaque(self, nivel):
        if nivel == 1: # Exemplo
            pass
        else:
            pass

    def ReceberDano(self, nivel):
        pass

    
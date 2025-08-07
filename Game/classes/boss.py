from personagem import Personagem

class Boss(Personagem):
    def __init__(self, nome: str, vida_max: int, ataque: int, defesa: int):
        super().__init__(nome, vida_max, ataque, defesa)
    
    def escolher_acao(self, jogador_alvo):
        self.atacar(jogador_alvo)
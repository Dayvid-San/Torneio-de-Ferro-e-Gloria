from batalha import Batalha
from boss import Boss
from jogador import Mago, Cavaleiro, Assassino

class Jogo:
    def __init__(self):
        self.jogador = None
        self.bosses = [
            Boss("Goblin Rei", vida_max=100, ataque=10, defesa=5, nivel = 1),
            Boss("Golem de Pedra", vida_max=150, ataque= 6, defesa=15, nivel = 2),
            Boss("Dragão Vermelho", vida_max=200, ataque=18, defesa=12, nivel = 3)
        ]
        self.andar_atual = 0
        self.batalha_atual = None
        self.estado_jogo = "menu_classe" 

    def criar_jogador(self, nome, classe):
        if classe == "Mago":
            self.jogador = Mago(nome)
        elif classe == " Cavaleiro":
            self.jogador =  Cavaleiro(nome)
        elif classe == "Assassino":
            self.jogador = Assassino(nome)
        print(f"Jogador {self.jogador.nome} da classe {classe} criado!")

    def proxima_batalha(self):
        if self.andar_atual < len(self.bosses):
            boss = self.bosses[self.andar_atual]
            self.batalha_atual = Batalha(self.jogador, boss)
            self.estado_jogo = "batalha"
            self.andar_atual += 1
            return True
        else:
            self.estado_jogo = "vitoria_final"
            print("Você derrotou todos os bosses!")
            return False
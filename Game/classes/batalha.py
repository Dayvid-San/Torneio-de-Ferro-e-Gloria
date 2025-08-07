from jogador import Jogador
from boss import Boss
class Batalha:
    def __init__(self, jogador: Jogador, boss: Boss):
        self.jogador = jogador
        self.boss = boss
        self.jogador.acoes_defesa = 1
        self.jogador.acoes_cura = 1

    def iniciar_batalha(self):
        print(f"Uma batalha começou entre {self.jogador.nome} e {self.boss.nome}!")

    def verificar_fim(self) -> str:
        if not self.jogador.esta_vivo():
            return "vitoria_boss"
        if not self.boss.esta_vivo():
            return "vitoria_jogador"
        return "continua"
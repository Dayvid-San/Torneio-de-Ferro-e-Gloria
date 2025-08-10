# CRIAR MAIN USANDO PYGAME

from batalha import Batalha
from boss import Boss
from jogador import Jogador

# A lista de Viloes está na classe Jogo, temos que pesquisar para saber se a lista deve ser
# criada na main para fazer o progama rodar, ou se é melhor apenas importa-la.

Argumentos = 'Preencher os argumentos das classes adequadamente'
# Caso for criar os viloes na main conforme as auals de POO, senão será por importação da lista "self.bosses"
# Temos que conversar sobre a criação dos personagens e viloes, se será no Progama Principal (Main) como nas
# aulas de POO ou realizar de outra forma como já vem sendo feito (Criação nas classes)

bossnivel1 = Boss(Argumentos)
bossnivel2 = Boss(Argumentos)
bossnivel3 = Boss(Argumentos)
bossnivel4 = Boss(Argumentos)
bossnivel5 = Boss(Argumentos)

batalha_nivel1 = Batalha(Jogador,bossnivel1)
batalha_nivel2 = Batalha(Jogador, bossnivel2)
batalha_nivel3 = Batalha(Jogador, bossnivel3)
batalha_nivel4 = Batalha(Jogador, bossnivel4)
batalha_nivel5 = Batalha(Jogador, bossnivel5)
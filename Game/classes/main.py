# CRIAR MAIN USANDO PYGAME

from batalha import Batalha
from boss import Boss
from jogador import Jogador
'''
# A lista de Viloes está na classe Jogo, temos que pesquisar para saber se a lista deve ser
# criada na main para fazer o progama rodar, ou se é melhor apenas importa-la.

Argumentos = 'Preencher os argumentos das classes adequadamente'
# Caso for criar os viloes na main conforme as aulas de POO, senão será por importação da lista "self.bosses" de uma
# das classes. Temos que conversar sobre a criação dos personagens e viloes (padronizar), se será no Progama Principal (Main)
#  como nas aulas de POO ou realizar de outra forma como já vem sendo feito (Criação nas classes).


#nome, vida_max, numeroAtaques, nivel

# Nível 1: Um chefe introdutório, com atributos baixos para o jogador aprender as mecânicas.
bossnivel1 = Boss("Goblin Ladrão", 100, 1, 1)

# Nível 2: Um desafio um pouco maior, com mais que o dobro da vida e a capacidade de atacar duas vezes.
bossnivel2 = Boss("Orc Brutamontes", 250, 2, 2)

# Nível 3: Um ponto de virada na dificuldade. Vida significativamente maior e três ataques por turno.
bossnivel3 = Boss("Golem de Pedra", 600, 3, 3)

# Nível 4: Um chefe avançado, exigindo que o jogador tenha dominado as mecânicas. Vida alta e múltiplos ataques potentes.
bossnivel4 = Boss("Dragão Ancião", 1500, 4, 4)

# Nível 5: O desafio final. Atributos massivos para testar tudo o que o jogador aprendeu.
bossnivel5 = Boss("Rei Demônio", 3000, 5, 5)

batalha_nivel1 = Batalha(Jogador,bossnivel1)
batalha_nivel2 = Batalha(Jogador, bossnivel2)
batalha_nivel3 = Batalha(Jogador, bossnivel3)
batalha_nivel4 = Batalha(Jogador, bossnivel4)
batalha_nivel5 = Batalha(Jogador, bossnivel5)
'''
# main.py
from jogo import Jogo

# 1. Inicia o jogo
game = Jogo()

# 2. Cria o jogador (esta parte seria controlada pela interface do Pygame)
nome_jogador = input("digite o nome do seu héroi ") # "Herói"
classe_jogador = input("Escolha a classe entre ") # Exemplo "Mago" 
game.escolher_jogador(nome_jogador, classe_jogador) 

# 3. Inicia a primeira batalha

game.proxima_batalha()

# 4. Aqui entraria o loop principal do Pygame, que interage com game.batalha_atual
# ...
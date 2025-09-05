# CRIAR MAIN USANDO PYGAME
from boss import Boss
from jogador import Jogador
from jogo import Jogo
#from Game.classes.jogo import Gameplay 

# 1. Inicia o jogo

# 2. Cria o jogador (esta parte seria controlada pela interface do Pygame)
#nome_jogador = input("digite o nome do seu héroi ") # "Herói"
#classe_jogador = input("Escolha a classe entre ") # Exemplo "Mago" 

# 3. Inicia a primeira batalha

# 4. Aqui entraria o loop principal do Pygame, que interage com game.batalha_atual
# ...

jogo = Jogo()
# ... (lógica para pegar nome e classe do jogador)
nome_jogador = "Aragorn"
classe_jogador = "Cavaleiro" # String limpa
jogo.escolher_jogador(nome_jogador, classe_jogador)

# Loop principal do jogo
while jogo.estado_jogo != "vitoria_final":
    if jogo.proxima_batalha():
        resultado = jogo.iniciar_batalha()
        
        if resultado == "vitoria_jogador":
            jogo.andar_atual += 1 # <<<<<<< O ANDAR É INCREMENTADO AQUI!
            # Aqui você pode dar recompensas, curar o jogador, etc.
            print("Preparando para o próximo desafio...")
        else:
            print("FIM DE JOGO!")
            break # Encerra o loop se o jogador for derrotado
    else:
        # Isso acontece quando proxima_batalha retorna False
        print("Você zerou o jogo! Parabéns!")
        break
from boss import Boss
from jogador import Jogador, Mago, Cavaleiro, Assassino

class Jogo:
    def __init__(self):
      self.jogador = None
      self.bosses = [
          Boss("homi Rei", vida_max=100, ataque=5, defesa=5, numeroAtaques=10, nivel = 1),
          Boss("homi de Pedra", vida_max=150, ataque=5, defesa=5, numeroAtaques= 6, nivel = 2),
          Boss("homi Vermelho", vida_max=200, ataque = 5, defesa = 5, numeroAtaques=18, nivel = 3)
      ]

      self.andar_atual = 0
      self.batalha_atual = None
      self.estado_jogo = "menu_classe" 
      self.boss = self.bosses[self.andar_atual]
       
      #self.jogador.acoes_defesa = 1
      #self.jogador.acoes_cura = 1

    def escolher_jogador(self, nome, classe):
      if classe == "Mago":
          self.jogador = Mago(nome)
      elif classe == "Cavaleiro":
          self.jogador =  Cavaleiro(nome)
      elif classe == "Assassino":
          self.jogador = Assassino(nome)
      print(f"Jogador da classe criado!")

    def proxima_batalha(self):
        if self.andar_atual < len(self.bosses):
            self.boss = self.bosses[self.andar_atual]
            self.estado_jogo = "batalha"
            return True
        else:
            self.estado_jogo = "vitoria_final"
            return False

        
#============================================
    def verificar_fim(self) -> str:
        if not self.jogador.estaVivo(): #trocar por valores booleanos 
            print("vitoria_boss")
            return "vitoria_boss"
        if not self.boss.estaVivo():
            print("vitoria_jogador")
            return "vitoria_jogador"
        print("continua")
        return "continua"

    def iniciar_batalha(self):
        print(f"Uma batalha começou entre {self.jogador.getNome()} e {self.boss.getNome()}!")
       
        while self.jogador.estaVivo() and self.boss.estaVivo():# troca do or por and 
            # -- TURNO DO JOGADOR --
            self.turno_jogador()# v
            if not self.boss.estaVivo():
                break # Sai do loop se o chefe morrer

            print("\n" + "="*20 + "\n")

            # -- TURNO DO CHEFE --
            self.turno_boss()
            if not self.jogador.estaVivo():
                break # Sai do loop se o jogador morrer
            
            print("\n" + "="*20 + "\n")

        # -- FIM DA BATALHA --
        '''status = self.verificar_fim()'''
        if self.jogador.estaVivo():
            print(f"Parabéns! Você derrotou {self.boss.getNome()}!")
            return "vitoria_jogador"
        else:
            print(f"Você foi derrotado por {self.boss.getNome()}.")
            return "vitoria_boss"

    def turno_jogador(self):
        # Reseta a defesa do jogador caso ele tenha defendido no turno anterior
        self.jogador.resetarDefesa()# esse método ainda n existe
        
        print(f"Turno de {self.jogador.getNome()} (Vida: {self.jogador.getVidaAtual()})")
        
        # Aqui entra a lógica para o Pygame no futuro. Por enquanto, usamos input().
        acao = input("Escolha sua ação: [1] Atacar, [2] Defender, [3] Curar\n> ")

        if acao == "1":
            #dano_causado = self.jogador.getAtaque() - self.boss.getDefesa() 
            print(f"{self.jogador.getNome()} ataca!")
            self.boss.ReceberDano(self.jogador.getAtaque())# método receber dano ainda n foi implementado
        
        elif acao == "2":
            print(self.jogador.defender())

        elif acao == "3":
            print(self.jogador.curar())
            
        else:
            print("Ação inválida, você perdeu seu turno!")

    def turno_boss(self):
        print(f"Turno de {self.boss.getNome()} (Vida: {self.boss.getVidaAtual()})")
        # IA simples: o chefe sempre ataca
        for i in range(self.boss.getNumeroAtaques()):
            if not self.jogador.estaVivo(): break # Para de atacar se o jogador já caiu
            
            print(f"{self.boss.getNome()} ataca pela {i+1}ª vez!")
            dano_causado = self.boss.getAtaque() - self.jogador.getDefesa()#  defessa está como método privado na classe personagem
            self.jogador.ReceberDano(dano_causado)# ReceberDano ainda não foi implementado
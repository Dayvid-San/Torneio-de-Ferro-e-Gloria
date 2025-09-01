from jogador import Jogador
from boss import Boss
class Batalha:
    def __init__(self, jogador: Jogador, boss: Boss):
        self.jogador = jogador
        self.boss = boss
        self.jogador.acoes_defesa = 1
        self.jogador.acoes_cura = 1

    def verificar_fim(self) -> str:
        if not self.jogador.esta_vivo(): #trocar por valores booleanos 
            return "vitoria_boss"
        if not self.boss.esta_vivo():
            return "vitoria_jogador"
        return "continua"

    def iniciar(self):
        print(f"Uma batalha começou entre {self.jogador.get_nome()} e {self.boss.get_nome()}!")
        
        while self.jogador.esta_vivo() or self.boss.esta_vivo():
            # -- TURNO DO JOGADOR --
            self.turno_jogador()
            if not self.boss.esta_vivo():
                break # Sai do loop se o chefe morrer

            #print("\n" + "="*20 + "\n")

            # -- TURNO DO CHEFE --
            self.turno_boss()
            if not self.jogador.esta_vivo():
                break # Sai do loop se o jogador morrer
            
            print("\n" + "="*20 + "\n")

        # -- FIM DA BATALHA --
        status = self.verificar_fim()
        if status == "vitoria_jogador":
            print(f"Parabéns! Você derrotou {self.boss.get_nome()}!")
        else:
            print(f"Você foi derrotado por {self.boss.get_nome()}. Fim de jogo.")
        
        return status

    def turno_jogador(self):
        # Reseta a defesa do jogador caso ele tenha defendido no turno anterior
        self.jogador.resetar_defesa()
        
        print(f"Turno de {self.jogador.get_nome()} (Vida: {self.jogador.get_vida_atual()})")
        
        # Aqui entra a lógica para o Pygame no futuro. Por enquanto, usamos input().
        acao = input("Escolha sua ação: [1] Atacar, [2] Defender, [3] Curar\n> ")

        if acao == "1":
            dano_causado = self.jogador.get_ataque() - self.boss.get_defesa()
            print(f"{self.jogador.get_nome()} ataca!")
            self.boss.receber_dano(dano_causado)
        
        elif acao == "2":
            print(self.jogador.defender())

        elif acao == "3":
            print(self.jogador.curar())
            
        else:
            print("Ação inválida, você perdeu seu turno!")

    def turno_boss(self):
        print(f"Turno de {self.boss.get_nome()} (Vida: {self.boss.get_vida_atual()})")
        # IA simples: o chefe sempre ataca
        for i in range(self.boss.get_numero_ataques()):
            if not self.jogador.esta_vivo(): break # Para de atacar se o jogador já caiu
            
            print(f"{self.boss.get_nome()} ataca pela {i+1}ª vez!")
            dano_causado = self.boss.get_ataque() - self.jogador.get_defesa()
            self.jogador.receber_dano(dano_causado)

   


  
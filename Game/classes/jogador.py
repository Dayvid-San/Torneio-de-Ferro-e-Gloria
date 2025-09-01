from personagem import Personagem

class Jogador(Personagem):
    def __init__(self, nome: str, vida_max: int, ataque: int, defesa: int):
        super().__init__(nome, vida_max, ataque, defesa)
        self.pontos = 0
        self.acoes_defesa = 1 
        self.acoes_cura = 1   


#================= Mecanincas Atreladas aos players=============
   
   #posteriormente utilizar esses métodos na barra de select na interface
    def defender(self) -> str:
        if self.acoes_defesa > 0:
            self.defesa += 10 
            self.acoes_defesa -= 1
            print(f"{self.nome} está se defendendo! Defesa aumentou.")
            return f"{self.nome} está se defendendo! Defesa aumentou."
        else:
            print(f"{self.nome} não pode mais se defender nesta batalha.")
            return f"{self.nome} não pode mais se defender."

    def curar(self) -> str:
        if self.acoes_cura > 0:
            cura = self.vida_max // 4 
            self.vida_atual += cura
            if self.vida_atual > self.vida_max:
                self.vida_atual = self.vida_max
            self.acoes_cura -= 1
            print(f"{self.nome} se curou em {cura} pontos de vida.")
            return f"{self.nome} se curou em {cura} pontos."
        else:
            print(f"{self.nome} não pode mais se curar nesta batalha.")
            return f"{self.nome} não pode mais se curar."

    def mostrar_status(self):
        return f"Nome: {self.nome}\nVida: {self.vida_atual}/{self.vida_max}\nAtaque: {self.ataque}\nDefesa: {self.defesa}\nPontos: {self.pontos}"


# ===================================================================

class Mago(Jogador):
    def __init__(self, nome: str):
        super().__init__(nome, vida_max=70, ataque=15, defesa=5)

    # Metodo de Ataque 
    def RealizarAtaque(self): # Metodo Personalizado da Classe Mago
        pass

    # Metodo de Dano
    def ReceberDano(self): # Metodo Personalizado da Classe Mago
        pass

# ===================================================================

class Cavaleiro(Jogador):
    def __init__(self, nome: str):
        super().__init__(nome, vida_max=120, ataque=8, defesa=12)

        # Metodo de Ataque 
    def RealizarAtaque(self): # Metodo Personalizado da Classe Cavaleiro
        pass

    # Metodo de Dano 
    def ReceberDano(self): # Metodo Personalizado da Classe Cavaleiro
        pass

# ===================================================================

class Assassino(Jogador):
    def __init__(self, nome: str):
        # Assassino: balanceado, com foco em ataque
        super().__init__(nome, vida_max=85, ataque=12, defesa=8)

    # Metodo de Ataque 
    def RealizarAtaque(self): # Metodo Personalizado da Classe Assassino
        pass

    # Metodo de Dano
    def ReceberDano(self): # Metodo Personalizado da Classe Assassino
        pass  
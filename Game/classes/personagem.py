# Criação da SUPER CLASSE (Classe Pai) para construção dos personagens (Heróis e Vilões) - CONCEITO: HERANÇA -
# Metodos Gerais -> GETS E SETS - CONCEITO: HERANÇA -
# Metodos Exclusivos dos Personagens: - PORLIFORFISMO - 
# Atributos dos personagens Privados: - Encapsulamento -

class Personagem:
    def __init__(self, nome: str, vida_max: int, ataque: int, defesa: int):
        self.__nome = nome
        self.__vida_max = vida_max
        self.__vida_atual = vida_max
        self.__ataque = ataque
        self.__defesa = defesa

    # METODOS GET E SET

    def getNome(self):
        return self.__nome
    
    def setNome(self, NovoNome):
        self.__nome = NovoNome
        return self.__nome
    
    def getVidaAtual(self):
        return self.__vida_atual
    
    def setVidaAtual(self, NovaVidaAtual):
        self.__vida_atual = NovaVidaAtual
        return self.__vida_atual
    
    def getVidaMax(self):
        return self.__vida_max
    
    def setVidaMax(self, NovaVidaMax):
        self.__vida_max = NovaVidaMax
        return self.__vida_max

    # add os get e set de atk e dfs 
    def getAtaque(self):
       return self.__ataque
    
    def setAtaque(self, Ataque):
        self.__ataque = Ataque

    def getDefesa(self):
       return self.__defesa
    
    def setAtaque(self, Defesa):
        self.__defesa = Defesa

    # METODOS DE AÇÕES:

    # Retorna um bool representando a condição do personagem
    def estaVivo(self) -> bool:
        return self.__vida_atual > 0

    # Metodo de Ataque 
    def RealizarAtaque(self):
        return self.__ataque

    # Metodo de Dano
    def ReceberDano(self,dano):
        dano_real = max(0, dano)
        self.__vida_atual -= dano_real
        print(f"{self.get_nome()} recebeu {dano_real} de dano e agora tem {self.__vida_atual} de vida.")
        if not self.esta_vivo():
            print(f"{self.get_nome()} foi derrotado!")

        
    def __str__(self):
        return f"{self.__nome} (Vida: {self.__vida_atual})"
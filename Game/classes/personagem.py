# Criação da SUPER CLASSE (Classe Pai) para construção dos personagens (Heróis e Vilões) - CONCEITO: HERANÇA -
# Metodos Gerais -> GETS E SETS - CONCEITO: HERANÇA -
# Metodos Exclusivos dos Personagens: - PORLIFORFISMO - 
# Atributos dos personagens Privados: - Encapsulamento -

class Personagem:
    def __init__(self, nome: str, vida_max: int):
        self.__nome = nome
        self.__vida_max = vida_max
        self.__vida_atual = vida_max

    # METODOS GET E SET

    def getNome(self):
        return self.__nome
    
    def setNome(self, NovoNome):
        self.__nome = NovoNome
        return self.__nome
    
    def getVidaAtual(self):
        return self.__vida_atual
    
    def sefVidaAtual(self, NovaVidaAtual):
        self.__vida_atual = NovaVidaAtual
        return self.__vida_atual
    
    def getVidaMax(self):
        return self.__vida_max
    
    def setVidaMax(self, NovaVidaMax):
        self.__vida_max = NovaVidaMax
        return self.__vida_max

    # METODOS DE AÇÕES:

    # Retorna um bool representando a condição do personagem
    def EstaVido(self) -> bool:
        return self.__vida_atual > 0

    # Metodo de Ataque
    def RealizarAtaque(self):
        pass

    # Metodo de Dano
    def ReceberDano(self):
        pass
        
    def __str__(self):
        return f"{self.__nome} (Vida: {self.__vida_atual})"
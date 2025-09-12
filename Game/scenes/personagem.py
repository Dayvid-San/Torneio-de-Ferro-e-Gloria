class Personagem:
    def __init__(self, fisica: int, magia: int):
        self.__fisica = fisica
        self.__magia = magia

    def setFisica(self, nova_fisica):
        self.__fisica = nova_fisica
    
    def getFisica(self):
        return self.__fisica
    
    def setMagia(self, nova_magia: int):
        self.__magia = nova_magia

    def getMagia(self: int):
        return self.__magia
    
    def FraseDeEfeito(argumento: str):
        pass
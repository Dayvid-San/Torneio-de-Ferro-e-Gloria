import pygame
from Game.utills.characterData import CharacterData


class CharacterSelectionManager:
    def __init__(self):
        # Defina os dados dos personagens aqui
        self.characters = [
            CharacterData("Assassino", "public/IconesJogo/assassino.jpeg", 
                          "Henrique, naufrago nas praias do condado e capturado roubando uma lorde, esse estrangeiro foi tomado como prisioneiro e agora luta por sua liberdade, na arena."),
            CharacterData("Cavaleiro", "public/IconesJogo/cavaleiro.jpeg", 
                          "Sula, o fracassado e desertor na batalha dos sete exércitos. Sula busca o perdão prometido em vitória na arena."),
            CharacterData("Mago", "public/IconesJogo/mago.jpeg", 
                          "Arnabin, um velho sábio (ou louco) do novo continente. Ele se diverte com seus experimentos em humanos e procura se entreter na arena.")
        ]

    def load_images(self, size):
        # Carrega e escala as imagens para cada personagem
        for char in self.characters:
            try:
                img = pygame.image.load(char.image_path).convert_alpha()
                char.image = pygame.transform.scale(img, size)
            except FileNotFoundError:
                print(f"Imagem do personagem {char.name} não encontrada.")
                char.image = pygame.Surface(size, pygame.SRCALPHA)
                char.image.fill((255, 0, 0, 100)) # Exibe um quadrado semi-transparente vermelho
    
    def get_character_data(self, name):
        for char in self.characters:
            if char.name == name:
                return char
        return None
    def __init__(self):
        # Defina os dados dos personagens aqui
        self.characters = [
            CharacterData("Assassino", "public/IconesJogo/assassino.jpeg", 
                          "Henrique, naufrago nas praias do condado..."),
            CharacterData("Cavaleiro", "public/IconesJogo/cavaleiro.jpeg", 
                          "Sula, o fracassado e desertor na batalha..."),
            CharacterData("Mago", "public/IconesJogo/mago.jpeg", 
                          "Arnabin, um velho sábio (ou louco)...")
        ]

    def load_images(self, size):
        # Carrega e escala as imagens para cada personagem
        for char in self.characters:
            try:
                img = pygame.image.load(char.image_path).convert_alpha()
                char.image = pygame.transform.scale(img, size)
            except FileNotFoundError:
                print(f"Imagem do personagem {char.name} não encontrada.")
                char.image = pygame.Surface(size, pygame.SRCALPHA) # Cria uma superfície vazia

    def get_character_data(self, name):
        # Retorna o objeto CharacterData pelo nome
        for char in self.characters:
            if char.name == name:
                return char
        return None
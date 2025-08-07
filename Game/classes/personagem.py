class Personagem:
    def __init__(self, nome: str, vida_max: int, ataque: int, defesa: int):
        self.nome = nome
        self.vida_max = vida_max
        self.vida_atual = vida_max
        self.ataque = ataque
        self.defesa = defesa

    def esta_vivo(self) -> bool:
        return self.vida_atual > 0

    def atacar(self, alvo:'Personagem') -> str:
        dano = self.ataque - alvo.defesa
        if dano < 0:
            dano = 0
        
        alvo.receber_dano(dano)
        print(f"{self.nome} atacou {alvo.nome} e causou {dano} de dano!")
        return f"{self.nome} atacou {alvo.nome} e causou {dano} de dano!"

    def receber_dano(self, dano: int):
        self.vida_atual -= dano
        if self.vida_atual < 0:
            self.vida_atual = 0
            
    def __str__(self):
        return f"{self.nome} (Vida: {self.vida_atual}/{self.vida_max})"
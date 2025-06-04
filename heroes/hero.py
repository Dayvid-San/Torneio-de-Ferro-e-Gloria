class Hero:
    def __init__(self, name, strength, intelligence, dexterity, constitution, charisma):
        self.name = name
        self.strength = strength
        self.intelligence = intelligence
        self.dexterity = dexterity
        self.constitution = constitution
        self.charisma = charisma
        self.hp = self.calculate_hp()
        self.level = 1
        self.experience = 0

    def calculateHp(self):
        # HP baseado na constituição, pode ser ajustado
        return 10 + self.constitution * 2

    def __str__(self):
        return (f"Hero: {self.name}\n"
                f"Level: {self.level}\n"
                f"HP: {self.hp}\n"
                f"Strength: {self.strength}\n"
                f"Intelligence: {self.intelligence}\n"
                f"Dexterity: {self.dexterity}\n"
                f"Constitution: {self.constitution}\n"
                f"Charisma: {self.charisma}")

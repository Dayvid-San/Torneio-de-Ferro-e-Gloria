# Game/data/character_data.py

# Este arquivo serve como um "banco de dados" em código para os personagens.
# Qualquer cena que precisar de informações sobre eles pode importar este dicionário.

CHARACTER_DATA = {
    "Assassino": {
        "description": "Henrique, naufrago nas praias do condado e capturado roubando uma lorde, esse estrangeiro foi tomado como prisioneiro e agora luta por sua liberdade, na arena.",
        "icon_path": "public/IconesJogo/assassino.jpeg",
        "stats": {"physical": 25, "magic": 15},
        "animations": {
            "idle": ["public/moveChar/right_assassino_idle_1.png", "public/moveChar/right_assassino_idle_2.png"],
            "physical": ["public/moveChar/right_assassino_ataque_fisico_1.png", "public/moveChar/right_assassino_ataque_fisico_2.png"],
            "magic": ["public/moveChar/right_assassino_magico_1.png", "public/moveChar/right_assassino_magico_2.png"]
        }
    },
    "Cavaleiro": {
        "description": "Sula, o fracassado e desertor na batalha dos sete exércitos. Sula busca o perdão prometido em vitória na arena.",
        "icon_path": "public/IconesJogo/cavaleiro.jpeg",
        "stats": {"physical": 30, "magic": 10},
        "animations": {
            "idle": ["public/moveChar/right_cavaleiro_idle_1.png", "public/moveChar/right_cavaleiro_idle_2.png"],
            "physical": ["public/moveChar/right_cavaleiro_ataque_fisico_1.png", "public/moveChar/right_cavaleiro_ataque_fisico_2.png"],
            "magic": ["public/moveChar/right_cavaleiro_magico_1.png", "public/moveChar/right_cavaleiro_magico_2.png"]
        }
    },
    "Mago": {
        "description": "Arnabin, um velho sábio (ou louco) do novo continente. Ele se diverte com seus experimentos em humanos e procura se entreter na arena.",
        "icon_path": "public/IconesJogo/mago.jpeg",
        "stats": {"physical": 10, "magic": 35},
        "animations": {
            "idle": ["public/moveChar/right_mago_idle_1.png", "public/moveChar/right_mago_idle_2.png"],
            "physical": ["public/moveChar/right_mago_ataque_fisico_1.png", "public/moveChar/right_mago_ataque_fisico_2.png"],
            "magic": ["public/moveChar/right_mago_magico_1.png", "public/moveChar/right_mago_magico_2.png"]
        }
    }
}
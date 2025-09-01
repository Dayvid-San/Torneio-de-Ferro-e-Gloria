# sugestões: trocar o nome "self.__numeroAtaques = numeroAtaques" por "self.__nvlBoss = nvlBoss"
# a classe main realmente vai ser usada? a classe jogo parece 
'''
#Nota_Diagrama:
    
    class Personagem { # Sugestão: mudança de nome da classe pai Personagem
      -nome: str
      -vida_max: int
      -vida_atual: int
      -ataque: int
      -defesa: int
      
      +esta_vivo() bool
      +receber_dano(dano)
      +getter's
      +setter's
    }

    class Jogador {
      -pontos: int
      -acoes_defesa: int
      -acoes_cura: int

      +defesa_base: int
      +acoes_defesa: int
      +acoes_cura: int
      +defender()
      +curar()
      +resetar_defesa()
    }

    class Mago {
      +__init__(nome)
    }
    class Cavaleiro {
      +__init__(nome)
    }
    class Assassino {
      +__init__(nome)
    }

    class Boss {
      -numeroAtaques: int
      -nivel: int
      +get_numero_ataques() int
    }

    class Batalha {
      -jogador: Jogador
      -boss: Boss
      +iniciar()
      +turno_jogador()
      +turno_boss()
      +verificar_fim() str
    }

    class Jogo {
      -jogador: Jogador
      -bosses: list~Boss~
      -batalha_atual: Batalha
      -andar_atual: int
      +criar_jogador(nome, classe)
      +proxima_batalha()
    }

    ' Relacionamentos de Herança
    Personagem <|-- Jogador
    Personagem <|-- Boss
    
    Jogador <|-- Mago
    Jogador <|-- Cavaleiro
    Jogador <|-- Assassino

    ' Relacionamentos de Composição/Associação
    Jogo "1" *-- "1" Jogador : contém
    Jogo "1" *-- "0..*" Boss : contém lista de
    Jogo "1" *-- "1" Batalha : gerencia
    Batalha "1" o-- "1" Jogador : usa
    Batalha "1" o-- "1" Boss : usa

'''

## 📂 `utils/` — Funções e utilitários do jogo

A pasta **`utils/`** contém **funções auxiliares, classes genéricas e módulos reutilizáveis** que **não pertencem especificamente a nenhuma cena ou entidade**, mas que podem ser usados em qualquer parte do jogo.

O objetivo é **evitar repetição de código** e **centralizar funcionalidades comuns** que serão úteis em várias partes do projeto.

---

### 🎯 O que entra em `utils/`?

Tudo que é **genérico e reaproveitável**:

* **Carregamento de recursos**
  Funções para carregar imagens, sons, fontes, mapas, etc.
* **Manipulação de arquivos**
  Leitura e escrita de dados (save/load).
* **Funções matemáticas**
  Cálculos de vetores, distâncias, ângulos, interpolação.
* **Geradores e conversores**
  Ex: converter cores, gerar IDs, formatar strings.
* **Controle de tempo**
  Contadores, timers, cooldowns.
* **Ferramentas de debug**
  Logs formatados, overlays de FPS, etc.

---

### 📁 Estrutura sugerida

```
utils/
├── __init__.py
├── loader.py         # Carrega imagens, sons e fontes
├── mathTools.py     # Funções matemáticas e de vetores
├── timer.py          # Classe utilitária de contagem de tempo
└── debug.py          # Funções de depuração e logs
```

---

### 📌 Boas práticas

* **Não coloque lógica de jogo aqui** → `utils/` não deve saber sobre cenas ou entidades específicas.
* **Evite código duplicado** → Se perceber que algo está sendo repetido em várias partes, considere movê-lo para `utils/`.
* **Mantenha funções pequenas e objetivas** → Cada utilitário deve ter uma responsabilidade clara.
* **Nomeie de forma descritiva** → Um módulo chamado `mathTools.py` deve conter apenas funções matemáticas, por exemplo.



## 📂 `scenes/` — Cenas do jogo

Este diretório contém **todas as cenas** (ou telas) do jogo.
Cada cena representa **um estado específico** em que o jogo pode estar, com sua própria lógica, interface e renderização.

---

### 🎯 O que é uma "Cena"?

No contexto do nosso jogo, **uma cena é um módulo que controla um momento ou fase do jogo**, por exemplo:

* Menu principal
* Tela de configurações
* Tela de gameplay (jogando de fato)
* Tela de pausa
* Tela de game over
* Créditos

Cada cena:

1. **Controla sua própria lógica** (eventos, atualizações, condições para mudar de cena)
2. **Gerencia seus elementos gráficos** (renderização da tela e da interface relacionada)
3. **Interage com o núcleo do jogo** (via `core` ou sistemas auxiliares)

---

### 📁 Estrutura sugerida

```
scenes/
├── __init__.py
├── mainMenu.py      # Cena do menu inicial
├── gameplay.py       # Cena principal de jogo
├── pause.py          # Cena de pausa
└── game_over.py      # Cena de fim de jogo
```

---

### 🔄 Ciclo de vida de uma cena

Cada cena geralmente terá **três funções principais**:

* **`handleEvents(events)`** → Processa entradas do jogador (teclado, mouse, etc.)
* **`update(deltaTime)`** → Atualiza o estado da cena (movimentos, animações, lógica)
* **`draw(surface)`** → Renderiza tudo na tela

---

### 📌 Boas práticas

* **Mantenha a lógica da cena isolada**: evite colocar código que pertença a outras partes (por exemplo, lógica de física ou carregamento de assets dentro de uma cena).
* **Reutilize componentes da pasta `ui/`** para menus, botões e HUD.
* **Nomeie os arquivos de forma clara** (`mainMenu.py`, `pause.py`, etc.).
* **Evite duplicar código**: use utilitários e classes compartilhadas da pasta `utils/` quando possível.




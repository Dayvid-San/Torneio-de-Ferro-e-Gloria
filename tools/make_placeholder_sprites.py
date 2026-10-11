"""Gera sprites/ícones PROVISÓRIOS de novos personagens recolorindo os de
personagens existentes (reduzidos a 1/4 do tamanho). Serve para o jogo ser
jogável enquanto a arte definitiva não existe: substitua os PNGs gerados por
arte própria mantendo os mesmos nomes de arquivo.

    python -m tools.make_placeholder_sprites          # gera tudo
"""
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MOVE = ROOT / "public" / "moveChar"
ICONS = ROOT / "public" / "IconesJogo"
KINDS = ("idle", "ataque_fisico", "magico")

# novo_slug: (slug de origem, cor de tinta RGB, força 0-1, brilho)
RECOLORS = {
    "arqueiro": ("assassino", (70, 200, 90), 0.65, 1.25),
    "clerigo": ("mago", (255, 235, 170), 0.85, 1.7),
    "barbaro": ("cavaleiro", (225, 70, 35), 0.75, 1.0),
}
SCALE = 4


def recolor(img: Image.Image, tint, strength, brightness) -> Image.Image:
    img = img.convert("RGBA")
    rgb = np.asarray(img, dtype=np.float32)[..., :3]
    alpha = np.asarray(img)[..., 3]
    lum = (rgb * (0.299, 0.587, 0.114)).sum(axis=-1, keepdims=True) / 255.0
    tinted = np.clip(lum * np.array(tint, dtype=np.float32) * 1.6 * brightness, 0, 255)
    out = rgb * (1 - strength) + tinted * strength
    out = np.clip(out * (brightness if brightness < 1.2 else 1.0), 0, 255)
    return Image.fromarray(np.dstack([out, alpha]).astype(np.uint8), "RGBA")


def shrink(img: Image.Image) -> Image.Image:
    return img.resize((img.width // SCALE, img.height // SCALE), Image.LANCZOS)


def main() -> None:
    for slug, (src, tint, strength, brightness) in RECOLORS.items():
        for kind in KINDS:
            for n in (1, 2):
                source = Image.open(MOVE / f"right_{src}_{kind}_{n}.png")
                target = MOVE / f"right_{slug}_{kind}_{n}.png"
                shrink(recolor(source, tint, strength, brightness)).save(target, optimize=True)
        icon = Image.open(ICONS / f"{src}.jpeg").convert("RGB")
        icon = recolor(icon, tint, strength, brightness).convert("RGB")
        icon.resize((icon.width // SCALE, icon.height // SCALE), Image.LANCZOS).save(
            ICONS / f"{slug}.jpeg", quality=88)
        print("gerado", slug)


if __name__ == "__main__":
    main()

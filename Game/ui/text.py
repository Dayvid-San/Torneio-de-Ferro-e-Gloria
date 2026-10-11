import pygame


def wrap_text(text: str, font: pygame.font.Font, color, max_width: int) -> list[pygame.Surface]:
    lines, current = [], ""
    for word in text.split(" "):
        candidate = f"{current} {word}".strip()
        if font.size(candidate)[0] <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return [font.render(line, True, color) for line in lines]

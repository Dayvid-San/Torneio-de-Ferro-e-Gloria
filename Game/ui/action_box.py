import pygame

class ActionBox:
    def __init__(self, x, y, width, height, options, font):
        self.__rect = pygame.Rect(x, y, width, height)
        self.__options = options
        self.__font = font
        self.__active = True
        self.__hovered_index = -1 
        self.__border_color = (255, 255, 255)
        self.__bg_color = (0, 0, 0)
        self.__text_color_normal = (200, 200, 200)
        self.__text_color_hover = (255, 255, 0)  
        self.__padding = 20

        self._prepare_options()

    def _prepare_options(self):
        self.__rendered_options = []
        self.__option_rects = []
        
        option_width = self.__rect.width / len(self.__options)
        
        for i, option_text in enumerate(self.__options):
            surf_normal = self.__font.render(option_text, True, self.__text_color_normal)
            surf_hover = self.__font.render(option_text, True, self.__text_color_hover)
            self.__rendered_options.append({"normal": surf_normal, "hover": surf_hover})

            pos_x = self.__rect.x + (i * option_width)
            rect = pygame.Rect(pos_x, self.__rect.y, option_width, self.__rect.height)
            self.__option_rects.append(rect)

    def update(self, mouse_pos):
        if not self.__active:
            self.__hovered_index = -1
            return

        for i, rect in enumerate(self.__option_rects):
            if rect.collidepoint(mouse_pos):
                self.__hovered_index = i
                return
        self.__hovered_index = -1

    def handle_click(self, event):
        if not self.__active or event.type != pygame.MOUSEBUTTONDOWN or self.__hovered_index == -1:
            return None

        if self.__option_rects[self.__hovered_index].collidepoint(event.pos):
            return self.__options[self.__hovered_index]
        
        return None

    def draw(self, screen):
        if not self.__active:
            return

        pygame.draw.rect(screen, self.__bg_color, self.__rect)
        pygame.draw.rect(screen, self.__border_color, self.__rect, 2)

        for i, rendered in enumerate(self.__rendered_options):
            if i == self.__hovered_index:
                text_surf = rendered["hover"]
            else:
                text_surf = rendered["normal"]
            
            option_rect = self.__option_rects[i]
            text_rect = text_surf.get_rect(center=option_rect.center)
            screen.blit(text_surf, text_rect)
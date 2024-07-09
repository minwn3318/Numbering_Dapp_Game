import pygame
import sys
from dataclasses import dataclass

pygame.init()

screen = pygame.display.set_mode((1040, 640))
pygame.display.set_caption('NumberingGame_Dapp')

font_dic = {
    'big_font': pygame.font.SysFont(None, 105),
    'small_font': pygame.font.SysFont(None, 55),
    'font': pygame.font.SysFont(None, 35)
}

color_dic = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'turquoise': (0, 255, 255),
    'claret': (255, 0, 255)
}

text_dic = {
    'big_text': "Numbering Game!!",
    'small_text': 'press "SPACE bar" to play',
    'text': 'OR press "SHIFT" to see Manual'
}

drawing_state = ["ready", "manual", "name","level","play", "ranking"]
now_state = drawing_state[0]
game_playeing = True

@dataclass
class UI:
    size : tuple
    coordinate : tuple
    color : str

@dataclass
class Text:
    font: int
    coordinate : tuple
    color : str

class UI_element:
    def __init__(self, text_font, text_coordinate, text_color, UI_size, UI_coordinate, UI_color) :
        self.text = Text(text_font, text_coordinate, text_color)
        self.UI = UI(UI_size, UI_coordinate, UI_color)
        self.textobj = None
        self.textrect = None
        self.string = None
        
    def render_text(self, surface):
        self.textobj = self.text.font.render(self.string, True, self.text.color)
        self.textrect = self.textobj.get_rect()
        self.textrect.topleft = self.text.coordinate
        surface.blit(self.textobj, self.textrect)

    def render_rect(self, surface) :
        UI_backGround = pygame.Rect(self.UI.coordinate, self.UI.size)
        pygame.draw.rect(surface, self.UI.color, UI_backGround, width=1)

class Scene :
    def __init__(self, UI_element_list, screen, state) :
        self.screen = screen
        self.scene_UI = UI_element_list
        self.current_state = state
        self.enter_state = False

    def start(self) :
        screen.fill(color_dic["black"])
        for UI in self.scene_UI[:1] :
            UI.render_text(screen)
            UI.render_rect(screen)
        self.scene_UI[2].render_text(screen)

    def is_alpha(self, key):
        return pygame.K_a <= key <= pygame.K_z or pygame.K_A <= key <= pygame.K_Z

    def is_digit(self, key):
        return pygame.K_0 <= key <= pygame.K_9
    
    def event_handler(self, events) :
        for event in events :
            if event.type == pygame.K_UP:
                if event.type == pygame.K_SPACE :
                    return event.unicode
                elif event == pygame.K_BACKSPACE :
                    return event.unicode
                elif event == pygame.K_RSHIFT or event == pygame.K_LSHIFT:
                    return event.unicode
                elif event == pygame.KSCAN_KP_ENTER or event == pygame.K_KP_ENTER :
                    return self.enter_state
                elif self.is_alpha(event) :
                    return event.unicode
                elif self.is_digit(event) :
                    return event.unicode

    def render_scene(self) :
        if self.current_state == drawing_state[0] :
            print("ready")
        elif self.current_state == drawing_state[1] :
            print("manual")
        elif self.current_state == drawing_state[2] :
            print("name")
        elif self.current_state == drawing_state[3] :
            print("level")
        elif self.current_state == drawing_state[4] :
            print("play")
        elif self.current_state == drawing_state[5] :
            print("rank")

def render_text(text, font, color, surf, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surf.blit(textobj, textrect)

def render_rect(startPoint, size, surf, color):
    UI_backGround = pygame.Rect(startPoint, size)
    pygame.draw.rect(surf, color, UI_backGround, width=1)

while(game_playeing):
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYUP :
            if event.key == pygame.K_SPACE :
                now_state = drawing_state[2]

    screen.fill(color_dic["black"])

    if now_state == drawing_state[0] :
        render_rect((100, 100), (830, 180), screen, color_dic["white"])
        render_rect((230, 400), (580, 100), screen, color_dic["white"])

        render_text(text_dic['big_text'], font_dic["big_font"], color_dic["blue"], screen, 180, 150)
        render_text(text_dic["small_text"], font_dic["small_font"], color_dic["red"], screen, 280, 430)
        render_text(text_dic["text"], font_dic["font"], color_dic["green"], screen, 335, 540)
    
    if now_state == drawing_state[1] : 
        render_rect((100, 100), (830, 180), screen, color_dic["white"])
        render_rect((230, 400), (580, 100), screen, color_dic["white"])

        render_text(text_dic['big_text'], font_dic["big_font"], color_dic[4], screen, 180, 150)

    if now_state == drawing_state[2] : 
        text_dic["big_text"] = "Guess Number!!"
        text_dic["text"] = "put the Number!!"

        render_rect((100, 100), (830, 180), screen, color_dic["white"])
        render_rect((230, 400), (580, 100), screen, color_dic["white"])

        render_text(text_dic["big_text"], font_dic["big_font"], color_dic["blue"], screen, 230, 150)
        render_text(text_dic["text"], font_dic["font"], color_dic["green"], screen, 400, 540)

    pygame.display.flip()
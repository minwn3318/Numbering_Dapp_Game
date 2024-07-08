import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1040, 640))
pygame.display.set_caption('NumberingGame_Dapp')

big_font = pygame.font.SysFont(None, 105)
small_font = pygame.font.SysFont(None, 55)
font = pygame.font.SysFont(None, 35)

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255,255,0)
turquoise = (0, 255, 255)
claret = (255, 0, 255)

big_text = "Numbering Game!!"
small_text = 'press "SPACE bar" to play'
text = 'OR press "SHIFT" to see Manual'

font_list = [big_font, small_font, font]
color_list = [black, white, red, green, blue, yellow, turquoise, claret]
drawing_state = ["ready", "manual", "play", "ranking"]
text_list = [big_text, small_text, text]

now_state = drawing_state[0]

def render_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_ract(startPoint, size, surface, color) :
    fount_backGround = pygame.Rect(startPoint, size)
    pygame.draw.rect(surface, color,  fount_backGround, width=1)

game_playeing = True
while(game_playeing):
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYUP :
            if event.key == pygame.K_SPACE :
                now_state = drawing_state[2]

    screen.fill(black)

    if now_state == drawing_state[0] :
        draw_ract((100, 100), (830, 180), screen, color_list[1])
        draw_ract((230, 400), (580, 100), screen, color_list[1])

        render_text(text_list[0], font_list[0], color_list[4], screen, 180, 150)
        render_text(text_list[1], font_list[1], color_list[2], screen, 280, 430)
        render_text(text_list[2], font_list[2], color_list[3], screen, 335, 540)
    
    if now_state == drawing_state[1] : 
        draw_ract((100, 100), (830, 180), screen, color_list[1])
        draw_ract((230, 400), (580, 100), screen, color_list[1])

        render_text(big_text, font_list[0], color_list[4], screen, 180, 150)

    if now_state == drawing_state[2] : 
        text_list[0] = "Guess Number!!"
        text_list[2] = "put the Number!!"

        draw_ract((100, 100), (830, 180), screen, color_list[1])
        draw_ract((230, 400), (580, 100), screen, color_list[1])

        render_text(text_list[0], font_list[0], color_list[4], screen, 230, 150)
        render_text(text_list[2], font_list[1], color_list[3], screen, 360, 540)

    pygame.display.flip()
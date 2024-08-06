import pygame as p
import sys
import ChessMain as cm

p.init()
width = 512
height = 612
screen_size = (width, height)
screen = p.display.set_mode(screen_size)
clock = p.time.Clock()
color_inactive = (100, 80, 255)
color_active = (100, 200, 255)
color_list_inactive = (255, 100, 100)
color_list_activate = (255, 150, 150)

class DropDown():
    # Test list
    option_list = ['Calibration', 'Test']

    def __init__(self, color_menu, color_option, x, y, w, h):
        self.color_menu = color_menu
        self.color_option = color_option
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    #Draw the initial button 'select mode'
    def draw_main(self, win, text=''):
        p.draw.rect(win, self.color_menu, (self.x, self.y, self.w, self.h), 0)
        if text != '':
            font = p.font.SysFont(None, 30)
            msg = font.render(text, 1,(0,0,0))
            screen.blit(msg, (self.x + (self.w/2 - msg.get_width() / 2), self.y + (self.h/2 - msg.get_height()/ 2)))

    # Draw list of option 'calibration' and 'test'
    def draw_opt(self, win, text=[]):
        opt_list = []
        if draw:
            for i, el in enumerate(text):
                opt_list.append(p.draw.rect(win, self.color_option, (self.x , self.y + (i+1)*self.h, self.w, self.h), 0))

                #write each option
                font = p.font.SysFont(None, 30)
                msg = font.render(text[i], 1,(0,0,0))
                screen.blit(msg, (self.x + (self.w/2 - msg.get_width() / 2),
                                  self.y + (i+1)*self.h +  (self.h/2 - msg.get_height()/ 2)))

    #Detect when the mouse is within the select mode box
    def choose_main(self, pos):
       if self.x < pos[0] < self.x + self.w and self.y < pos[1] < self.y + self.h:
           return True
       else:
           return False

    #detect when the mouse is within the option list
    def choose_opt(self, pos):
        if self.x < pos[0] < self.x + self.w and 2*self.y < pos[1] < 2*self.y + self.h:
            return True
        else:
            return False


draw = False
list1 = DropDown(color_inactive,color_list_inactive,50,50,200,50)

menu = True
while menu:
    screen = p.display.set_mode((width,height))


    for e in p.event.get():
        if e.type == p.quit():
            menu = False

        elif e.type == p.MOUSEBUTTONDOWN:
            pos = p.mouse.get_pos()
            if list1.choose_main(pos):
                list1.color_menu = color_active
            else:
                list1.color_menu = color_inactive

        elif e.type == p.MOUSEBUTTONDOWN:
            if e.button == 1 and list1.choose_main(pos):
                if draw == False:
                    draw = True
                elif draw == True:
                    draw = False

list1.draw_main(screen, 'Select Mode')
list1.draw_opt(screen, ['Calibration', 'Test'])

p.display.flip()
clock.tick(30)










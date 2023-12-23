from engine import Game

#setting up pygame
import pygame as py
py.init()
py.font.init()
py.display.set_caption('Bottleship')
font = py.font.FontType('JetBrainsMono-Medium.ttf',40)
tfont = py.font.FontType('JetBrainsMono-Medium.ttf',20)

sq_size=30
h_margin = sq_size*4
v_margin = sq_size
width=sq_size*10*2+h_margin
height=sq_size * 10 * 2 + v_margin
indent=10
padding=10

SCREEN = py.display.set_mode((width, height))
HUMAN1 = False
HUMAN2 = False

GREY = (40,50,60)
WHITE = (255,250,250)
GREEN = (50,200,150)
RED = (250,50,100)
BLUE = (50,150,200)
ORANGE =(250,140,20)
COLORS = {'u': GREY, 'm': BLUE, 'h': ORANGE, 's': RED,}

def draw_grid(player,left = 0, top = 0, search = False):
    for i in range(100):
        x = left + i%10 * sq_size
        y = top + i//10 * sq_size
        square = py.Rect(x,y,sq_size,sq_size)
        py.draw.rect(SCREEN,WHITE,square,width=2)

        if search:
            x += sq_size//2
            y += sq_size//2
            py.draw.circle(SCREEN,COLORS[player.search[i]],(x,y), radius = sq_size//4)

def draw_ships(player, left = 0, top = 0):
    for ship in player.ships:
        x = left + ship.col * sq_size + indent
        y = top + ship.row * sq_size + indent
        
        if ship.orient == 'h':
            width = ship.size * sq_size - 2*indent
            height = sq_size - 2*indent
        else:
            width = sq_size - 2*indent
            height = ship.size * sq_size - 2*indent
        
        rectangle = py.Rect(x,y,width,height)
        py.draw.rect(SCREEN,GREEN,rectangle,border_radius=15)

game = Game(HUMAN1,HUMAN2)

#pygame loop
anim=True
pause = False
home = True
mode = 'e'

while anim:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            anim=False
        
        if event.type == py.MOUSEBUTTONDOWN and not game.over:
            x,y=py.mouse.get_pos()
            if game.player1_turn and x<sq_size*10 and y<sq_size*10:
                row = y//sq_size
                col = x//sq_size
                ind = row*10+col
                game.make_move(ind)
            elif not game.player1_turn and x>width-sq_size*10 and y>sq_size*10+v_margin:
                row = (y-sq_size*10 - v_margin)//sq_size
                col = (x-sq_size*10 - h_margin)//sq_size
                ind = row*10+col
                game.make_move(ind)

            if home and mouse[0]>(width//2-115) and mouse[0]<(width//2+115) and mouse[1]>245 and mouse[1]<275:
                HUMAN1=True
                game = Game(HUMAN1,HUMAN2)
                home=not home
            elif home and mouse[0]>(width//2-115) and mouse[0]<(width//2+115) and mouse[1]>295 and mouse[1]<325:
                HUMAN1=True
                HUMAN2=True
                game = Game(HUMAN1,HUMAN2)
                home=not home
            elif home and mouse[0]>(width//2-115) and mouse[0]<(width//2+115) and mouse[1]>345 and mouse[1]<375:
                game = Game(HUMAN1,HUMAN2)
                home=not home
            elif home and mouse[0]>(width//2+20) and mouse[0]<(width//2+70) and mouse[1]>height-55 and mouse[1]<height-25:
                mode = 'e'
            elif home and mouse[0]>(width//2+85) and mouse[0]<(width//2+135) and mouse[1]>height-55 and mouse[1]<height-25:
                mode = 'h'

        
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                anim = False
            if event.key == py.K_SPACE:
                pause = not pause
            if event.key == py.K_BACKSPACE:
                game = Game(HUMAN1,HUMAN2)

    if not pause:

        #background
        SCREEN.fill(GREY)

        #homescreen
        if home:
            title = 'BottleSHIP'
            opt1 = 'Player Vs Computer'
            opt2 = 'Player Vs Player'
            opt3 = 'Computer vs Computer'
            diff1 = 'Easy'
            diff2 = 'Hard'
            diff = 'Difficulty:'

            SCREEN.blit(font.render(title, False, GREEN),(width//2-125, 10))
            
            if event.type == py.MOUSEMOTION:
                mouse=py.mouse.get_pos()
                
                if mouse[0]>(width//2-115) and mouse[0]<(width//2+115) and mouse[1]>245 and mouse[1]<275:
                    SCREEN.blit(tfont.render(opt1, False, ORANGE),(width//2-115, 250))
                else:
                    SCREEN.blit(tfont.render(opt1, False, WHITE),(width//2-115, 250))

                if mouse[0]>(width//2-115) and mouse[0]<(width//2+115) and mouse[1]>295 and mouse[1]<325:
                    SCREEN.blit(tfont.render(opt2, False, ORANGE),(width//2-115, 300))
                else:
                    SCREEN.blit(tfont.render(opt2, False, WHITE),(width//2-115, 300))

                if mouse[0]>(width//2-115) and mouse[0]<(width//2+115) and mouse[1]>345 and mouse[1]<375:
                    SCREEN.blit(tfont.render(opt3, False, ORANGE),(width//2-115, 350))
                else:
                    SCREEN.blit(tfont.render(opt3, False, WHITE),(width//2-115, 350))
                
                if mode == 'e':
                    SCREEN.blit(tfont.render(diff1, False, ORANGE, WHITE),(width//2+20, height-50))
                else:
                    SCREEN.blit(tfont.render(diff1, False, ORANGE),(width//2+20, height-50))

                if mode == 'h':
                    SCREEN.blit(tfont.render(diff2, False, ORANGE, WHITE),(width//2+85, height-50))
                else:
                    SCREEN.blit(tfont.render(diff2, False, ORANGE),(width//2+85, height-50))
                
                SCREEN.blit(tfont.render(diff, False, ORANGE),(width//2-135, height-50))
            
            else:
                SCREEN.blit(font.render('exit?', False, RED),(width//2-65, 300))
                
        else:

            #grids
            draw_grid(game.player1,left=padding,top=padding,search=True)
            draw_grid(game.player2,left=((width-h_margin)//2+h_margin)-padding,top=((height-v_margin)//2+v_margin)-padding,search=True)

            if(game.over):
                draw_grid(game.player1,top=((height-v_margin)//2+v_margin)-padding,left=padding)
                draw_grid(game.player2,left=((width-h_margin)//2+h_margin)-padding,top=padding)

                #ships
                draw_ships(game.player1,top=((height-v_margin)//2+v_margin)-padding,left=padding)
                draw_ships(game.player2,left=((width-h_margin)//2+h_margin)-padding,top=padding)

            if(HUMAN1 and not HUMAN2):
                draw_grid(game.player1,top=((height-v_margin)//2+v_margin)-padding,left=padding)
                draw_ships(game.player1,top=((height-v_margin)//2+v_margin)-padding,left=padding)

            elif(not HUMAN1 and not HUMAN2):
                draw_grid(game.player1,top=((height-v_margin)//2+v_margin)-padding,left=padding)
                draw_grid(game.player2,left=((width-h_margin)//2+h_margin)-padding,top=padding)

                #ships
                draw_ships(game.player1,top=((height-v_margin)//2+v_margin)-padding,left=padding)
                draw_ships(game.player2,left=((width-h_margin)//2+h_margin)-padding,top=padding)

            #computer moves
            if not game.over and game.computer_turn:
                if game.player1_turn:
                    game.basic_ai()
                else:
                    if mode == 'e':
                        game.basic_ai()
                    elif mode == 'h':
                        game.human_ai()

            #game over message
            if game.over:
                text = 'Player '+str(game.result)+' WINS!'
                textbox = font.render(text, False, ORANGE,GREY)
                SCREEN.blit(textbox, (width//2 - 160, height//2 - 30))

        #screen refresh
        py.time.wait(100)  #to slow down the move speed of computer
        py.display.flip()
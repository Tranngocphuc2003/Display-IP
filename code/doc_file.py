
import pygame
import time
pygame.init()
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
dis_width = 1400
dis_height = 860
txt1 = open ('file3.txt','r',encoding='utf8')
vb1=txt1.readlines()
txt1.close()
txt2 = open ('file4.txt','r',encoding='utf8')
vb2=txt2.readlines()
txt2.close()
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('tạo nhạc')
do_rong = 200
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 25)
def van_ban1(vb):
    value1 = score_font.render("value1 : " + str(vb), True, blue)
    dis.blit(value1, [20, 100])
def van_ban2(vb):
    value2 = score_font.render("value2 : " + str(vb), True, blue)
    dis.blit(value2, [20, 130])

def gameLoop():
    ct=True
    do_dai=min(len(vb1),len(vb2))
    dem=0
    while ct:
        dem=dem+1
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    ct=False
        dis.fill(black)
        if vb1[dem-1] == '1\n':
            pygame.draw.rect(dis, red, [400, 300, do_rong, do_rong])
            van_ban1(1)
        else:
            pygame.draw.rect(dis, green, [400, 300, do_rong, do_rong])
            van_ban1(0)
        if vb2[dem-1] == '1\n':
            pygame.draw.rect(dis, yellow, [800, 300, do_rong, do_rong])
            van_ban2(1)
        else:
            pygame.draw.rect(dis, green, [800, 300, do_rong, do_rong])
            van_ban2(0)
        pygame.display.update()
        if dem>=do_dai-1:
            ct=False
        time.sleep(0.02)
    pygame.quit()
    quit()
    
gameLoop()
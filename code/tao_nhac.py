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
txt1=open('file5.txt','w',encoding='utf8')
txt2=open('file6.txt','w',encoding='utf8')
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('tạo nhạc')
do_rong = 200
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 25)
def van_ban1(vb):
    value1 = score_font.render("value1 : " + str(vb), True, blue)
    dis.blit(value1, [20, 100])
def van_ban2(vb):
    value2 = score_font.render("vulue2 : " + str(vb), True, blue)
    dis.blit(value2, [20, 130])

def gameLoop():
    ct = True
    ct1=False
    ct2=False
    ghi=False
    t=0
    while ct:
        dis.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    ct=False
                if event.key == pygame.K_x:
                    ct1=True
                    ghi=True
                    t=time.time()
                if event.key == pygame.K_m:
                    ct2=True
                    ghi=True
                    t=time.time()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_x:
                    ct1=False
                if event.key == pygame.K_m:
                    ct2=False
        if time.time() - t >1:
            ghi=False
        if ct1:
            pygame.draw.rect(dis, red, [400, 300, do_rong, do_rong])
            van_ban1(1)
            if ghi:
                txt1.write('1\n')
        if ct1==False:
            pygame.draw.rect(dis, green, [400, 300, do_rong, do_rong])
            van_ban1(0)
            if ghi:
                txt1.write('0\n')
        if ct2:
            pygame.draw.rect(dis, yellow, [800, 300, do_rong, do_rong])
            van_ban2(1)
            if ghi:
                txt2.write('1\n')
        if ct2==False:
            pygame.draw.rect(dis, green, [800, 300, do_rong, do_rong])
            van_ban2(0)
            if ghi:
                txt2.write('0\n')
        pygame.display.update()
        time.sleep(0.02)
    txt1.close()
    txt2.close()
    pygame.quit()
    quit()
    
gameLoop()
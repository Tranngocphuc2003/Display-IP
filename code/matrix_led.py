import pygame
 
pygame.init()
dis = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
 
def blitRotate(surf, image, pos, originPos, angle):
    w, h       = image.get_size()
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])
    rotated_image = pygame.transform.rotate(image, angle)
    surf.blit(rotated_image, origin)

M=[]
a = open ('NGUYEN_HUU_THANG.txt','r',encoding='utf8')
dl=a.readlines()
a.close()
for i in dl:
    x=i.strip()
    m=[]
    for j in x:
        m.append(j)
    M.append(m)

image = pygame.image.load('banh_xe.png')
w, h = image.get_size()
start = False
angle = 0
done = False
d=-1
a=len(M)
while not done:
    d=d+1
    if d==a-7:
        d=0
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            start = True

    pos = (dis.get_width()/2, dis.get_height()/2)
    mang=M[d:d+8]
    dis.fill(0)
    blitRotate(dis, image, (200,200), (w/2, h/2), angle)
    angle += 2
    #pygame.draw.line(dis, (0, 255, 0), (pos[0]-20, pos[1]), (pos[0]+100, pos[1]), 3)
    #pygame.draw.line(dis, (0, 255, 0), (pos[0], pos[1]-20), (pos[0], pos[1]+20), 3)
    for i in range(8):
        for j in range(8):
            if mang[i][j]=='1':
                pygame.draw.circle(dis, (255, 0,0),(400+20*i,300+20*j),8)
            else:
                pygame.draw.circle(dis, (50, 100,100),(400+20*i,300+20*j),8)
    pygame.display.flip()
pygame.quit()
exit()


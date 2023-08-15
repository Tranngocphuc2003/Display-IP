from threading import Thread
from requests import get
import time, re, subprocess,random,socket,uuid,pygame

run=True
ct_rl=True
ct_dc=True
df=True
d_f=0
LCD_RS = 23
LCD_E = 27
LCD_D4 = 18
LCD_D5 = 17
LCD_D6 = 14
LCD_D7 = 3
LED_ON = 2
BT1 = 21
BT2 = 26
BT3 = 20
BT4 = 19
LED = 13
rl_1 = 16
rl_2 = 12
PIN = 22
DIR = 25
txt=[]
LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80 # 128
LCD_LINE_2 = 0xC0 # 192

### phần này để test
vb1=''
vb2=''
dl_BT1=False
dl_BT2=False
dl_BT3=False
dl_BT4=False
ma=''
### phần này để test

E_PULSE = 0.0005
E_DELAY = 0.0005

def doc_file(s):
    txt = open ('file'+str(s)+'.txt','r',encoding='utf8')
    dr=txt.readlines()
    txt.close()
    return dr

while df:
    d_f=d_f+1
    try:
        a=doc_file(d_f)
        txt.append(a)
    except:
        df=False
    at=True 

if len(txt)<2:
    print('vui lòng copy các file txt vào đúng thư mục chứa file tuan_13.py\n')
    at=False

def led(n):
    global LED
    for o in range(n):
        LED=True
        time.sleep(0.065)
        LED=False
        time.sleep(0.065)

def ip_public():
    ip = get('https://api.ipify.org').text
    return ip

def ip_private():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    IP = s.getsockname()[0]
    s.close()
    return IP


def name_pc():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    h_name = socket.gethostname()
    s.close()
    return h_name

def dia_chi_mac():
    return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

def scan_wifi():
    output = subprocess.check_output(["netsh", "wlan", "show", "network"])
    output = output.decode("utf-8")
    output = output.replace("\r","")
    print(output)
    output=output.split('SSID')
    essid=[]
    M=[]
    dem=-1
    for i in output:
        dem=dem+1
        i=i.split('\n')
        m=[]
        essid.append(i[0])
        for j in i:
            j=j.strip(' ')
            m.append(j)
        M.append(m)
    essid.remove(' ')
    return [essid,M]

def lstrip(vb,x):
    while True:
        if len(vb)<len(x):
            return vb
        X=[]
        for i in x:
            X.append(i)
        VB=[]
        for i in vb:
            VB.append(i)
        dem=-1
        ct=True
        for i in X:
            dem=dem+1
            if X[dem]!=VB[dem]:
                ct=False
                return vb
        if ct==True:
            s=[]
            d=-1
            for i in VB:
                d=d+1
                if d>dem:
                    s.append(i)
            VB=s
        s=''
        for i in VB:
            s=s+i
        vb=s

def exit_reset():
    global run,dk,ct_rl,ct_dc,ct
    global dl_BT1, dl_BT2, dl_BT3, dl_BT4,vb1,vb2 # chỉ để test
    while run:
        if dl_BT3==True and dl_BT4==True:
            run=False
            print(100*'\n'+'Cảm ơn mọi người\nChúc một ngày fix bug thành công\nHẹn gặp lại\n')
            time.sleep(1)
        if dl_BT1==True and dl_BT2==True: 
            dk=False
            ct=False
        if dl_BT1==True and dl_BT3==True: 
            if ct_rl:
                ct_rl=False
            else:
                ct_rl=True
        if dl_BT1==True and dl_BT4==True: 
            if ct_dc:
                ct_dc=False
            else:
                ct_dc=True
        time.sleep(0.04)
    print('Luồng exit_reset đã kết thúc')

def LCD ():
    print('Bắt đầu luồng LCD')
    print('Đang lấy thông tin\nxin đợi')
    global vb1, vb2, dl_BT1, dl_BT2, dl_BT3, dl_BT4 # phục vụ việc test. k có trong code chính
    global a,b,run,dk,ma,LED
    try:
        LED=True
        Mac=dia_chi_mac()
        LED=False 
        IP_private=ip_private()
        LED=True
        Host_Name=name_pc()
        LED=False
        IP_public=ip_public()
        print('Bấm nút bất kì để bắt đầu')
        led(10)
    except:
        print('Không có Internet')
        vb1='khong co'
        vb2='internet'
        exit()
    dk=True
    vb1=''
    vb2=''
    while dk and run:
        time.sleep(0.01)
        if dl_BT1==True or dl_BT2==True or dl_BT3==True or dl_BT4==True or len(ma)>0:
            dk=False
    time.sleep(0.2)
    vb1='He    '.center(16,' ')
    time.sleep(0.5)
    vb1='He Nho'.center(16,' ')
    time.sleep(0.5)
    vb2='Cac    '.center(16,' ')
    time.sleep(0.5)
    vb2='Cac Ban'.center(16,' ')
    time.sleep(1)
    vb1=''.center(16,' ')
    vb2=''.center(16,' ')
    time.sleep(0.25)
    lines1='host name'
    lines2='mac'
    lines3='ip private'
    lines4='ip public'
    lines5='scan wifi'
    lines6='chuyen co so'
    a=1
    b=0
    dk=True
    vb1='> host name'.ljust(16,' ')
    vb2='  mac'.ljust(16,' ')
    ct1=False
    ct2=False
    ct3=False
    ct4=False
    l_r='l'
    u_d=''
    print('nhấn BT1 dể di chuyển lên')
    print('nhấn BT2 để di chuyển xuống')
    print('nhấn BT3 để quay lại')
    print('nhấn BT4 để chọn')
    print('nhấn đồng thời BT1 và BT2 để reset')
    print('nhấn đồng thời BT3 và BT4 để thoát chương trình')
    while dk and run:
        if dl_BT1==True or ma=='CH+':
            ct1=True
        if dl_BT2==True or ma=='CH-':
            ct2=True
        if dl_BT3==True or ma=='VOL-':
            ct3=True
        if dl_BT4==True or ma=='VOL+':
            ct4=True
        if dl_BT1==False and ct1==True:
            ct1=False
            u_d='u'
        if dl_BT2==False and ct2==True:
            ct2=False
            u_d='d'
        if dl_BT3==False and ct3==True:
            ct3=False
            l_r='l'
        if dl_BT4==False and ct4==True:
            ct4=False
            l_r='r'
        
        
        if l_r=='l':
            if b==0 and u_d=='u':
                a=a-1
            if b==1 and u_d=='d':
                a=a+1
            if u_d=='u':
                b=0
            if u_d=='d':
                b=1
            u_d=''             
            if a%6==1:
                dong1=lines1
                dong2=lines2
            if a%6==2:
                dong1=lines2
                dong2=lines3
            if a%6==3:
                dong1=lines3
                dong2=lines4
            if a%6==4:
                dong1=lines4
                dong2=lines5
            if a%6==5:
                dong1=lines5
                dong2=lines6
            if a%6==0:
                dong1=lines6
                dong2=lines1
            if b==0:
                dong1='> '+dong1
                dong2='  '+dong2
            elif b==1:
                dong1='  '+dong1
                dong2='> '+dong2
            else:
                print ('???')
            vb1=dong1.ljust(16,' ')
            vb2=dong2.ljust(16,' ')
        elif l_r=='r':
            d=(a+b)%6
            if d==1:
                vb1='host name'.center(16,' ')
                vb2=Host_Name.center(16,' ')
            if d==2:
                vb1='mac'.center(16,' ')
                if luu_so_l_r=='l':
                    print('nhấn BT1, BT2 để di chuyển văn bản')
                    M=[]
                    dem=16
                    mac=16*' '+Mac+16*' '
                    for i in mac:
                        M.append(i)
                if (dl_BT1==True or ma=='CH+') and dem<33:
                    dem=dem+1
                    time.sleep(0.2)
                if (dl_BT2==True or ma=='CH-') and dem>0:
                    dem=dem-1
                    time.sleep(0.2)
                s=''
                for i in range(dem,dem+16):
                    s=s+M[i]
                vb2=s.center(16,' ')
            if d==3:
                vb1='ip private'.center(16,' ')
                vb2=IP_private.center(16,' ')
            if d==4:
                vb1='ip public'.center(16,' ')
                vb2=IP_public.center(16,' ')
            if d==5:
                try:
                    sc_wifi()
                    l_r='l'
                except:
                    vb1='quet wifi'.center(16,' ')
                    vb2='bi loi'.center(16,' ')
                    time.sleep(2)
                    l_r='l'
            if d==0:
                try:
                    chuyen_co_so()
                    l_r='l'
                except:
                    vb1='chuyen co so'.center(16,' ')
                    vb2='bi loi'.center(16,' ')
                    time.sleep(2)
                    l_r='l'
            u_d=''
        luu_so_l_r=l_r
        time.sleep(0.03)
        LED=True
        time.sleep(0.01)
        LED=False
    print('luồng LCD đã kết thúc')
        
def sc_wifi():
    global vb1,vb2,dl_BT1,dl_BT2,dl_BT3,dl_BT4 # chỉ dùng để test
    global ma, run,ct
    ct=True
    wifi=scan_wifi()
    print('dùng bằng điều khiển đê')
    if len(wifi[0])<1:
        vb1='khong tim'
        vb2='thay wifi'
        time.sleep(1.4)
        return None
    dem_d=0
    dem_n=0
    stt=1
    lstt=0
    M1=[]
    M2=[]
    s=''
    lsdd=0
    lsdd1=0
    ss=0
    while ct and run:
        if (dl_BT3==True or ma=='PREV') and stt==1:
            ct=False
        if stt<1:
            ct=False
        if stt==1:
            m=wifi[0]
            if ma=='0':
                s=s+'0'
            if ma=='1':
                s=s+'1'
            if ma=='2':
                s=s+'2'
            if ma=='3':
                s=s+'3'
            if ma=='4':
                s=s+'4'
            if ma=='5':
                s=s+'5'
            if ma=='6':
                s=s+'6'
            if ma=='7':
                s=s+'7'
            if ma=='8':
                s=s+'8'
            if ma=='9':
                s=s+'9'
            if s!='':
                ss=int(s)
            else:
                ss=0
            if ss>=len(wifi[1]):
                s=''
            if ma=="PLAY/PAUSE" and s!='':
                stt=2
                dem_d=0
                dem_n=0
                lstt=0
                lsdd1=lsdd
                lsdd=0
        elif stt==2:
            if ma=='CH' or dl_BT3==True or ma=='PREV':
                stt=1
                dem_n=0
                lstt=0
                dem_d=lsdd1
                s=''
                time.sleep(0.2)
                continue
            m=wifi[1][int(s)]
        else:
            print('???')
        l=len(m)
        if l==1:
            m.append('')
        if ma=='CH+' and dem_d>0:
            dem_d=dem_d-1
        if ma=='CH-' and dem_d<l-2:
            dem_d=dem_d+1
        if dem_d!=lsdd:
            dem_n=0
        d_1=m[dem_d]
        d_2=m[dem_d+1]
        l_n1=len(d_1)
        l_n2=len(d_2)
        l_n=max(l_n1,l_n2)
        d_1=d_1.ljust(l_n,' ')
        d_2=d_2.ljust(l_n,' ')
        if l_n<16:
            vb1=d_1.ljust(16,' ')
            vb2=d_2.ljust(16,' ')
        elif l_n>15:
            for i in d_1:
                M1.append(i)
            for j in d_2:
                M2.append(j)
            if ma=='VOL+' and dem_n<l_n-16:
                dem_n=dem_n+1
            if ma=='VOL-' and dem_n>0:
                dem_n=dem_n-1
            dr1=''
            dr2=''
            for i in range(dem_n,16+dem_n):
                dr1=dr1+M1[i]
            for i in range(dem_n,16+dem_n):
                dr2=dr2+M2[i]
            M1=[]
            M2=[]
            vb1=dr1
            vb2=dr2
        if stt-lstt==1:
            dem_n=0
        if stt==1 and s!='':
            vb2=s.center(16,' ')
        lstt=stt
        lsdd=dem_d
        if len(ma)>0:
            time.sleep(0.2)
        time.sleep(0.01)


def ccs10():
    a=subprocess.run(['python', 'chuyen_co_so.py'],capture_output=True,encoding='utf-8')
    return a.stdout.strip()

def ghi_ma(vb):
    m=open('chuyen_co_so.py','w',encoding='utf8')
    m.write('print('+vb+')')   
    m.close()

def chuyen_co_so():
    global vb1,vb2 # chỉ dùng để test
    global ma,run,ct
    ct=True
    stt=1
    lstt=0
    tu=''
    den=''
    t=''
    tt=''
    s=''
    M=[]
    vb1=''
    vb2=''
    while ct and run:
        if dl_BT3==True or ma=='PREV':
            ct=False
        if ma=="PREV":
            ct=False
        if stt==1:
            vb1='chuyen tu he'.center(16,' ')
            if t=='':
                vb2='2 8 10 16'.center(16,' ')
            if ma=='2':
                tu='2'
                vb2='2'.center(16,' ')
            if ma=='8':
                tu='8'
                vb2='8'.center(16,' ')
            if ma=='1':
                t='1'
                vb2='1'.center(16,' ')
            if t=='1' and ma=='0':
                tu='10'
                vb2='10'.center(16,' ')
            if t=='1' and ma=='6':
                tu='16'
                vb2='16'.center(16,' ')
            if tu!='':
                stt=2
                t=''
        elif stt==2:
            vb1='chuyen den he'.center(16,' ')
            if t=='':
                vb2='2 8 10 16'.center(16,' ')
            if ma=='2':
                den='2'
                vb2='2'.center(16,' ')
            if ma=='8':
                den='8'
                vb2='8'.center(16,' ')
            if ma=='1':
                t='1'
                vb2='1'.center(16,' ')
            if t=='1' and ma=='0':
                den='10'
                vb2='10'.center(16,' ')
            if t=='1' and ma=='6':
                den='16'
                vb2='16'.center(16,' ')
            if den!='':
                stt=3
                if tu=='16':
                    vb1='A=10 B=11 C=12'.center(16,' ')
                    vb2='D=13 E=14 F=15'.center(16,' ')
                    time.sleep(3)
                    vb1='nhap so'
                    vb2='nhan NEXT'
                    time.sleep(1)
                    vb2=''
        elif stt==3:
            vb1=('so can chuyen '+tt).center(16,' ')
            if tu=='2':
                vb2=s
                if ma=='0':
                    s=s+'0'
                if ma=='1':
                    s=s+'1'
                if ma=="PLAY/PAUSE" and s!='':
                    ghi_ma('0b'+s)
                    stt=4
            elif tu=='8':
                if ma=='0':
                    s=s+'0'
                if ma=='1':
                    s=s+'1'
                if ma=='2':
                    s=s+'2'
                if ma=='3':
                    s=s+'3'
                if ma=='4':
                    s=s+'4'
                if ma=='5':
                    s=s+'5'
                if ma=='6':
                    s=s+'6'
                if ma=='7':
                    s=s+'7'
                if ma=="PLAY/PAUSE" and s!='':
                    ghi_ma('0o'+s)
                    stt=4
            elif tu=='10':
                if ma=='0':
                    s=s+'0'
                if ma=='1':
                    s=s+'1'
                if ma=='2':
                    s=s+'2'
                if ma=='3':
                    s=s+'3'
                if ma=='4':
                    s=s+'4'
                if ma=='5':
                    s=s+'5'
                if ma=='6':
                    s=s+'6'
                if ma=='7':
                    s=s+'7'
                if ma=='8':
                    s=s+'8'
                if ma=='9':
                    s=s+'9'
                if ma=="PLAY/PAUSE" and s!='':
                    ghi_ma(s)
                    stt=4
            elif tu=='16':
                if ma=='0':
                    tt=tt+'0'
                if ma=='1':
                    tt=tt+'1'
                if ma=='2':
                    tt=tt+'2'
                if ma=='3':
                    tt=tt+'3'
                if ma=='4':
                    tt=tt+'4'
                if ma=='5':
                    tt=tt+'5'
                if ma=='6':
                    tt=tt+'6'
                if ma=='7':
                    tt=tt+'7'
                if ma=='8':
                    tt=tt+'8'
                if ma=='9':
                    tt=tt+'9'
                if len(tt)>0:
                    if int(tt)>15 or int(tt)<=0:
                        tt=''
                if ma=="NEXT":
                    if len(tt)==1:
                        s=s+tt
                    if tt=='10':
                        s=s+'A'
                    if tt=='11':
                        s=s+'B'
                    if tt=='12':
                        s=s+'C'
                    if tt=='13':
                        s=s+'D'
                    if tt=='14':
                        s=s+'E'
                    if tt=='15':
                        s=s+'F'
                    tt=''
                if ma=="PLAY/PAUSE" and s!='':
                    ghi_ma('0x'+s)
                    stt=4
        elif stt==4:
            cs10=int(ccs10())
            if den=='2':
                s=bin(cs10).lstrip('0b')
            if den=='8':
                s=oct(cs10).lstrip('0o')
            if den=='10':
                s=str(cs10)
            if den=='16':
                s=hex(cs10).lstrip('0x')
            stt=5
            s=s.upper()
        elif stt==5:
            vb1='ket qua'.center(16,' ')
            if ma=="PLAY/PAUSE":
                ct=False
        l=len(str(s))
        
        if l<16 and stt>2:
            vb2=s.center(16,' ')
        elif l>15:
            for i in s:
                M.append(i)
            if ma=='VOL+' and dem<0:
                dem=dem+1
            if ma=='VOL-' and dem>16-l:
                dem=dem-1
            dr=''
            for i in range(l-16+dem,l+dem):
                dr=dr+M[i]
            M=[]
            vb2=dr.center(16,' ')
        if stt-lstt==1:
            dem=0
        lstt=stt
        if len(ma)>0:
            time.sleep(0.2)
        time.sleep(0.01)

def ro_le(vb1,vb2):
    print('Luồng ro_le đã bắt đầu')
    pygame.mixer.music.load('t2.mp3')
    global run,ct_rl, clock,n1,n2
    try:
        n1=False
        n2=False
        ls_n1=False
        ls_n2=False
        ct=True
        do_dai=min(len(vb1),len(vb2))
        dem=0
        while ct and run and ct_rl:
            dem=dem+1
            if vb1[dem-1] == '1\n':
                n1=True
            else:
                n1=False
            if vb2[dem-1] == '1\n':
                n2=True
            else:
                n2=False
            if n1==True and ls_n1==False or n2==True and ls_n2==False:
                pygame.mixer.music.play()
            ls_n1=n1
            ls_n2=n2
            if dem>=do_dai-1:
                ct=False
            time.sleep(0.023)
    except:
        print('có lỗi gì khi điều khiển rơ le')
    print('Luồng ro_le đã kết thúc')

angle=0
mh1=False
def dong_co(vb1,vb2):
    global run,ct_dc,dis,image, w, h, black, angle, clock
    blue = (50, 153, 213)
    try:
        ct=True
        do_dai=min(len(vb1),len(vb2))
        dem=0
        while ct and run and ct_dc:
            dem=dem+1
            for i in range(6):
                pygame.draw.rect(dis, black, [30, 280, 250, 250])
                if vb1[dem-1] == '1\n' and vb2[dem-1] == '1\n':
                    angle += 4
                elif vb1[dem-1] == '1\n':
                    angle += 2
                elif vb2[dem-1] == '1\n':
                    angle += 2
                if dem>=do_dai-1:
                    ct=False
                blitRotate(dis, image, (150,400), (w/2, h/2), angle)
                pygame.display.update()
                clock.tick(300)
    except:
        print('có lỗi với động cơ')
        ct_dc=False

def nhac():
    print('Luồng nhạc đã bắt đầu')
    global run,ct_rl,ct_dc,txt 
    if at == True:
        l=len(txt)
        time.sleep(1)
        while run:
            # print('Nhấn đồng thời BT1 và BT3 hoặc nhấn nút 100+ trên điều khiển để bật tắt rơ le')
            # print('Nhấn đồng thời BT1 và BT4 hoặc nhấn nút 200+ trên điều khiển để bật tắt động cơ')
            s=random.randint(0, l//2-1)
            vb1=txt[s*2] 
            vb2=txt[s*2+1]
            if ct_dc:
                dc = Thread(target=dong_co,args=(vb1,vb2,))
                dc.start()
            time.sleep(0.02)
            if ct_rl:
                rl = Thread(target=ro_le,args=(vb1,vb2,))
                rl.start()
            if ct_dc:
                dc.join()
            if ct_rl:
                rl.join()
            
            time.sleep(0.01)
    print('luồng nhạc đã kết thúc')

def ht_lmt(vb):
    global run, dis, clock
    M=[]
    a = open (vb+'.txt','r',encoding='utf8')
    dl=a.readlines()
    a.close()
    for i in dl:
        x=i.strip()
        m=[]
        for j in x:
            m.append(j)
        M.append(m)
    d=-1
    a=len(M)
    while run:
        d=d+1
        if d==a-7:
            break
        mang=M[d:d+8]
        for i in range(8):
            for j in range(8):
                if mang[i][j]=='1':
                    pygame.draw.circle(dis, (255, 0,0),(520+20*i,330+20*j),8)
                else:
                    pygame.draw.circle(dis, (50, 100,100),(520+20*i,330+20*j),8)
        clock.tick(10)

def L_matrix():
    global run
    time.sleep(1)
    try:
        vb=['PYMA', 'NGUYEN_XUAN_AN', 'DANG_HAI_LINH', 'TRAN_NGOC_PHUC', 'TRINH_TRONG_PHUOC', 'NGUYEN_HUU_THANG','PYMA']
        while run:
            print('a')
            s=random.randint(0, 10)
            if s>6:
                ht_lmt(vb[0])
            else:
                ht_lmt(vb[s])
    except:
        print('LED_matrix bị lỗi')
### hàm mô phỏng
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

def mo_phong():
    global vb1, vb2, dl_BT1, dl_BT2, dl_BT3, dl_BT4, run, ma, dis, image, w, h, black, clock, LED,n1,n2
    pygame.init()
    clock = pygame.time.Clock()
    yellow = (255, 255, 102)
    black = (0, 0, 0)
    blue = (50, 153, 213)
    red=(255,0,0)
    dis_width = 900
    dis_height = 600
    LED=False
    n1=False
    n2=False
    image = pygame.image.load('banh_xe.png')
    w, h = image.get_size()
    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('thuyết trình tuần 13')
    score_font = pygame.font.SysFont("comicsansms", 85)
    abc = pygame.font.SysFont("comicsansms", 20)
    def van_ban1(vb):
        value1 = score_font.render(str(vb), True, yellow)
        dis.blit(value1, [30,0])
    def van_ban2(vb):
        value2 = score_font.render(str(vb), True, yellow)
        dis.blit(value2, [30, 110])
    while run:
        pygame.draw.rect(dis, (0,50,50), [20, 20, 860, 240])
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run=False
                if event.key == pygame.K_UP:
                    dl_BT1=True
                if event.key == pygame.K_DOWN:
                    dl_BT2=True
                if event.key == pygame.K_LEFT:
                    dl_BT3=True
                if event.key == pygame.K_RIGHT:
                    dl_BT4=True
                if event.key == pygame.K_1:
                    ma='1'
                if event.key == pygame.K_2:
                    ma='2'
                if event.key == pygame.K_3:
                    ma='3'
                if event.key == pygame.K_4:
                    ma='4'
                if event.key == pygame.K_5:
                    ma='5'
                if event.key == pygame.K_6:
                    ma='6'
                if event.key == pygame.K_7:
                    ma='7'
                if event.key == pygame.K_8:
                    ma='8'
                if event.key == pygame.K_9:
                    ma='9'
                if event.key == pygame.K_0:
                    ma='0'
                if event.key == pygame.K_p:
                    ma='PLAY/PAUSE'
                if event.key == pygame.K_c:
                    ma='VOL+'
                if event.key == pygame.K_t:
                    ma='VOL-'
                if event.key == pygame.K_l:
                    ma='CH+'
                if event.key == pygame.K_x:
                    ma='CH-'
                if event.key == pygame.K_h:
                    ma='CH'
                if event.key == pygame.K_r:
                    ma='PREV'
                if event.key == pygame.K_e:
                    ma='EQ'
                    run=False
                if event.key == pygame.K_a:
                    ma='100+'
                if event.key == pygame.K_b:
                    ma='200+'
                if event.key == pygame.K_n:
                    ma='NEXT'
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    dl_BT1=False
                if event.key == pygame.K_DOWN:
                    dl_BT2=False
                if event.key == pygame.K_LEFT:
                    dl_BT3=False
                if event.key == pygame.K_RIGHT:
                    dl_BT4=False
        van_ban1(vb1)
        van_ban2(vb2)
        if LED:
            pygame.draw.circle(dis, (255, 255,200),(420,370),20)
        else:
            pygame.draw.circle(dis, (0, 70,50),(420,370),20)
        value_LED = abc.render(str('LED'), True, yellow)
        dis.blit(value_LED, [405,400])
        if n1:
            pygame.draw.circle(dis, (255, 255,200),(800,370),30)
        else:
            pygame.draw.circle(dis, (0, 70,50),(800,370),30)  
        value_LED = abc.render(str('RL1'), True, yellow)
        dis.blit(value_LED, [730,356])  
        if n2:
            pygame.draw.circle(dis, (255, 255,200),(800,450),30)
        else:
            pygame.draw.circle(dis, (0, 70,50),(800,450),30)
        value_LED = abc.render(str('RL2'), True, yellow)
        dis.blit(value_LED, [730,438])
        if dl_BT1:
            pygame.draw.rect(dis, red, [400, 520, 35, 30])
        else:
            pygame.draw.rect(dis, blue, [400, 520, 35, 30])
        value_LED = abc.render(str('BT1'), True, yellow)
        dis.blit(value_LED, [400,560])
        if dl_BT2:
            pygame.draw.rect(dis, red, [500, 520, 35, 30])
        else:
            pygame.draw.rect(dis, blue, [500, 520, 35, 30])
        value_LED = abc.render(str('BT2'), True, yellow)
        dis.blit(value_LED, [500,560])
        if dl_BT3:
            pygame.draw.rect(dis, red, [600, 520, 35, 30])
        else:
            pygame.draw.rect(dis, blue, [600, 520, 35, 30])
        value_LED = abc.render(str('BT3'), True, yellow)
        dis.blit(value_LED, [600,560])
        if dl_BT4:
            pygame.draw.rect(dis, red, [700, 520, 35, 30])
        else:
            pygame.draw.rect(dis, blue, [700, 520, 35, 30])
        value_LED = abc.render(str('BT4'), True, yellow)
        dis.blit(value_LED, [700,560])
        pygame.display.update()
        clock.tick(25)
        ma=''
    print('luồng mô phỏng đã kết thúc')
    pygame.quit()
    quit()
### hàm mô phỏng

c1 = Thread(target=L_matrix)
c3 = Thread(target=nhac)
c5 = Thread(target=mo_phong)  
c6 = Thread(target=exit_reset)
c1.start()
c3.start()
c5.start()
c6.start()
while run:
    c2 = Thread(target=LCD)
    c2.start()
    c2.join()
    time.sleep(0.5)


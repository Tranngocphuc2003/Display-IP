from threading import Thread
from requests import get
#import RPi.GPIO as GPIO
import time, re, subprocess,random,socket,uuid,pygame

run=True
ct_rl=False
ct_dc=False
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

try:
    from luma.led_matrix.device import max7219 
    from luma.core.interface.serial import spi, noop
    from luma.core.render import canvas 
    from luma.core.virtual import viewport
    from luma.core.legacy import text, show_message
    from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
    led_matrix = True
except:
    print('vui lòng cài đặt thư viện Max7219 để hiển thị LED matrix')
    print('link github: https://github.com/diy-hus/max7219')
    print('bạn có thể tải file zip về giải nén hoặc tải bằng câu lệnh:')
    print('git clone https://github.com/diy-hus/max7219.git')
    print('sau khi đã tải về cài đặt bằng câu lệnh:\npython3 -m pip install --upgrade luma.led_matrix')
    print('sau khi hoàn thành bài học chạy câu lệnh: ')
    print('python3 -m pip uninstall upgrade luma.led_matrix\nđể gỡ cài đặt\n')
    led_matrix = False

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

# def led(n):
#     for o in range(n):
#         GPIO.output (LED, GPIO.LOW)
#         time.sleep(0.065)
#         GPIO.output (LED, GPIO.HIGH)
#         time.sleep(0.065)

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
    scan_wifi = subprocess.check_output(["iwlist", "wlan0", "scan"]) 
    scan_wifi = scan_wifi.decode("utf-8") #  ascii
    scan_wifi=scan_wifi.split('Cell')
    essid=[]
    M=[]
    dem=-1
    for i in scan_wifi:
        dem=dem+1
        i=i.split('\n')
        m=[]
        for j in i:
            j=j.strip(' ')
            if j.count('ESSID')>0:
                j=lstrip(j,'ESSID:"')
                j=j.rstrip('"')
                essid.append(str(dem)+': '+j)
            m.append(j)
        M.append(m)
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
        

# def dong_1(vb):
#     lcd_byte(LCD_LINE_1, LCD_CMD)
#     lcd_string(vb,2)

# def dong_2(vb):
#     lcd_byte(LCD_LINE_2, LCD_CMD)
#     lcd_string(vb,2)

def exit_reset():
    global run,dk,ct_rl,ct_dc,ct
    global dl_BT1, dl_BT2, dl_BT3, dl_BT4 # chỉ để test
    while run:
        if dl_BT3==True and dl_BT4==True:
            run=False
            time.sleep(1)
            #GPIO.cleanup()
            exit()
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

def LCD ():
    print('Đang lấy thông tin\nxin đợi')
    global vb1, vb2, dl_BT1, dl_BT2, dl_BT3, dl_BT4 # phục vụ việc test. k có trong code chính
    global a,b,run,dk,ma
    try:
        #GPIO.output (LED, GPIO.LOW)
        Mac=dia_chi_mac()
        #GPIO.output (LED, GPIO.HIGH) 
        IP_private=ip_private()
        #GPIO.output (LED, GPIO.LOW)
        Host_Name=name_pc()
        #GPIO.output (LED, GPIO.HIGH)
        IP_public=ip_public()
        print('Bấm nút bất kì để bắt đầu')
        #led(10)
    except:
        print('Không có Internet')
        vb1='khong co'
        vb2='internet'
        exit()
    dk=True
    #GPIO.output (LED_ON, False)
    vb1=''
    vb2=''
    while dk and run:
        time.sleep(0.01)
        if dl_BT1==True or dl_BT2==True or dl_BT3==True or dl_BT4==True or len(ma)>0:
            dk=False
    #GPIO.output (LED_ON, True)
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
        #GPIO.output (LED, GPIO.LOW)
        time.sleep(0.01)
        #GPIO.output (LED, GPIO.HIGH)
    #GPIO.cleanup()
    print('luồng LCD đã kết thúc')
        
# def lcd_init():
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setwarnings(False)
#     GPIO.setup(LCD_E, GPIO.OUT)
#     GPIO.setup(LCD_RS, GPIO.OUT)
#     GPIO.setup(LCD_D4, GPIO.OUT)
#     GPIO.setup(LCD_D5, GPIO.OUT)
#     GPIO.setup(LCD_D6, GPIO.OUT)
#     GPIO.setup(LCD_D7, GPIO.OUT)
#     GPIO.setup(LED_ON, GPIO.OUT)
#     GPIO.setup (LED, GPIO.OUT)
#     GPIO.setup (rl_1, GPIO.OUT)
#     GPIO.setup (rl_2, GPIO.OUT) 
#     # 
    
#     #
#     GPIO.setup (BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
#     GPIO.setup (BT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#     GPIO.setup (BT3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#     GPIO.setup (BT4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#     GPIO.setup (PIN, GPIO.IN, GPIO.PUD_UP)
#     GPIO.setup (DIR, GPIO.OUT)
#     lcd_byte(0x33,LCD_CMD) # 51
#     lcd_byte(0x32,LCD_CMD) # 50
#     lcd_byte(0x28,LCD_CMD) # 40
#     lcd_byte(0x0C,LCD_CMD) # 12
#     lcd_byte(0x06,LCD_CMD) # 6
#     lcd_byte(0x01,LCD_CMD) # 1
#     GPIO.output (rl_1, False)
#     GPIO.output (rl_2, False)

# def lcd_string(message,style):
#     if style==1:
#         message = message.ljust(LCD_WIDTH," ")
#     if style==2: 
#         message = message.center(LCD_WIDTH," ") 
#     if style==3: 
#         message = message.rjust(LCD_WIDTH," ")
#     for i in range(LCD_WIDTH):
#         lcd_byte(ord(message[i]),LCD_CHR)

# def lcd_byte(bits, mode):
#     GPIO.output(LCD_RS, mode)
#     GPIO.output(LCD_D4, False)
#     GPIO.output(LCD_D5, False)
#     GPIO.output(LCD_D6, False)
#     GPIO.output(LCD_D7, False)
#     if bits&0x10==0x10:
#         GPIO.output(LCD_D4, True)
#     if bits&0x20==0x20:
#         GPIO.output(LCD_D5, True)
#     if bits&0x40==0x40:
#         GPIO.output(LCD_D6, True)
#     if bits&0x80==0x80:
#         GPIO.output(LCD_D7, True)
#     time.sleep(E_DELAY)
#     GPIO.output(LCD_E, True)
#     time.sleep(E_PULSE)
#     GPIO.output(LCD_E, False)
#     time.sleep(E_DELAY)

#     GPIO.output(LCD_D4, False)
#     GPIO.output(LCD_D5, False)
#     GPIO.output(LCD_D6, False)
#     GPIO.output(LCD_D7, False)
#     if bits&0x01==0x01:
#         GPIO.output(LCD_D4, True) 
#     if bits&0x02==0x02: 
#         GPIO.output(LCD_D5, True) 
#     if bits&0x04==0x04:
#         GPIO.output(LCD_D6, True)
#     if bits&0x08==0x08:
#         GPIO.output(LCD_D7, True)
#     time.sleep(E_DELAY)
#     GPIO.output(LCD_E, True)
#     time.sleep(E_PULSE)
#     GPIO.output(LCD_E, False)
#     time.sleep(E_DELAY)

def sc_wifi():
    global vb1,vb2,dl_BT1,dl_BT2,dl_BT3,dl_BT4 # chỉ dùng để test
    global ma, run,ct
    ct=True
    wifi=scan_wifi()
    print('dùng bằng điều khiển đê')
    if len(wifi[0])<1:
        vb1='khong tim'
        vb2='thay wifi'
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
                time.slee(0.2)
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
    global vb1,vb2 # chỉ đung dể test
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
    dr=''
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

# def ro_le(vb1,vb2):
#     global run,ct_rl
#     try:
#         ct=True
#         do_dai=min(len(vb1),len(vb2))
#         dem=0
#         while ct and run and ct_rl:
#             dem=dem+1
#             if vb1[dem-1] == '1\n':
#                 GPIO.output (rl_1, True)
#             else:
#                 GPIO.output (rl_1, False)
#             if vb2[dem-1] == '1\n':
#                 GPIO.output (rl_2, True)
#             else:
#                 GPIO.output (rl_2, False)
#             if dem>=do_dai-1:
#                 ct=False
#             time.sleep(0.02)
#         GPIO.output (rl_1, False)
#         GPIO.output (rl_2, False)
#     except:
#         print('có lỗi gì khi điều khiển rơ le')

# def dong_co(vb1,vb2):
#     global run,ct_dc
#     try:
#         PWD1 = GPIO.PWM (DIR, 1000)
#         PWD1.start (0)
#         ct=True
#         do_dai=min(len(vb1),len(vb2))
#         dem=0
#         while ct and run and ct_dc:
#             dem=dem+1
#             if vb1[dem-1] == '1\n' and vb2[dem-1] == '1\n':
#                 PWD1.ChangeDutyCycle (100)
#             elif vb1[dem-1] == '1\n':
#                 PWD1.ChangeDutyCycle (50)
#             elif vb2[dem-1] == '1\n':
#                 PWD1.ChangeDutyCycle (50)
#             else:
#                 PWD1.ChangeDutyCycle (0)
#             if dem>=do_dai-1:
#                 ct=False
#             time.sleep(0.02)
#         PWD1.ChangeDutyCycle (0)
#     except:
#         print('có lỗi với động cơ')
#         ct_dc=False

# def nhac():
#     global run,ct_rl,ct_dc,txt 
#     if at == True:
#         l=len(txt)
#         while run:
#             # print('Nhấn đồng thời BT1 và BT3 hoặc nhấn nút 100+ trên điều khiển để bật tắt rơ le')
#             # print('Nhấn đồng thời BT1 và BT4 hoặc nhấn nút 200+ trên điều khiển để bật tắt động cơ')
#             s=random.randint(0, l//2-1)
#             vb1=txt[s*2] ## LỖI TRÀN MẢNG 
#             vb2=txt[s*2+1]
#             if ct_rl:
#                 rl = Thread(target=ro_le,args=(vb1,vb2,))
#                 rl.start()
#                 rl.join()
#             if ct_dc:
#                 dc = Thread(target=dong_co,args=(vb1,vb2,))
#                 dc.start()
#                 dc.join()
#             time.sleep(0.01)
        

# def hong_ngoai():
#     global run,ma,ct_rl, ct_dc
#     while run:
#         ma=read_IRM (PIN)
#         if ma=='100+' and ct_rl:
#             ct_rl=False
#         elif ma=='100+' and ct_rl==False:
#             ct_rl=True
#         if ma=='200+' and ct_dc:
#             ct_dc=False
#         elif ma=='200+' and ct_dc==False:
#             ct_dc=True
#         if len(ma) != 0:
#             time.sleep(0.04)

# def read_IRM (PIN): # thiếu dữ liệu của PIN 
#     if GPIO.input (PIN) == 0:
#         count=0
#         while GPIO.input (PIN) == 0 and count < 200: 
#             count += 1
#             time.sleep(0.00006)
#         count=0
#         while GPIO.input (PIN) == 1 and count < 80:
#             count += 1
#             time.sleep (0.00006)
#         idx = 0
#         cnt = 0
#         data = [0,0,0,0]
#         for i in range (0,32):
#             count=0
#             while GPIO.input (PIN) == 0 and count < 15:
#                 count += 1
#                 time.sleep(0.00006)
#             count=0
#             while GPIO.input (PIN) == 1 and count < 40:
#                 count += 1
#                 time.sleep(0.00006)
#             if count > 8:
#                 data[idx] |= 1<<cnt
#             if cnt == 7:
#                 cnt = 0 
#                 idx += 1
#             else:
#                 cnt += 1
#         if data [0] + data[1] == 0xFF and data [2] +data[3] == 0xFF: 
#             print("Get the key: 0x%02x" %data[2]) 
#             return exec_cmd(data[2])
#     return ''
                
# def exec_cmd (key_val):
#     if (key_val == 0x45):
#         return "CH-"
#     elif (key_val==0x46): 
#         return "CH"
#     elif (key_val==0x47): 
#         return "CH+"
#     elif (key_val==0x44):
#         return "PREV"
#     elif (key_val==0x40):
#         return "NEXT"
#     elif (key_val==0x43):
#         return "PLAY/PAUSE"
#     elif (key_val==0x07):
#         return "VOL-"
#     elif (key_val==0x15):
#         return "VOL+"
#     elif (key_val==0x09):
#         return "EQ"
#     elif (key_val==0x16):
#         return "0"
#     elif (key_val==0x19):
#         return "100+" 
#     elif (key_val==0x0d):
#         return "200+" 
#     elif (key_val==0x0c):
#         return "1"
#     elif (key_val==0x18):
#         return "2"
#     elif (key_val==0x5e):
#         return "3"
#     elif (key_val==0x08):
#         return "4"
#     elif (key_val==0x1c):
#         return "5"
#     elif (key_val==0x5a): 
#         return "6"
#     elif (key_val==0x42): 
#         return "7"
#     elif (key_val==0x52):
#         return "8"
#     elif (key_val ==0x4a): 
#         return "9"

def L_matrix():
    global run
    try:
        cascaded=1
        block_orientation=90
        rotate=0
        serial=spi(port=0, device=0, gpio=noop()) 
        device = max7219(serial, cascaded=cascaded, block_orientation=block_orientation, rotate=rotate)
        device.contrast(20)
        vb=['PYMA', 'NGUYEN XUAN AN', 'DANG HAI LINH', 'TRAN NGOC PHUC', 'TRINH TRONG PHUOC', 'NGUYEN HUU THANG','<3']
        while run:
            s=random.randint(0, 10)
            if s>6:
                show_message (device, vb[0], fill="white", font=proportional(CP437_FONT), scroll_delay=0.06)
            else:
                show_message (device, vb[s], fill="white", font=proportional(CP437_FONT), scroll_delay=0.06)
    except:
        print('LED_matrix bị lỗi')
### hàm mô phỏng
def mo_phong():
    global vb1, vb2,dl_BT1,dl_BT2,dl_BT3,dl_BT4,run,ma
    pygame.init()
    yellow = (255, 255, 102)
    black = (0, 0, 0)
    blue = (50, 153, 213)
    dis_width = 900
    dis_height = 250
    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('thuyết trình tuần 13')
    score_font = pygame.font.SysFont("comicsansms", 85)
    def van_ban1(vb):
        value1 = score_font.render(str(vb), True, yellow)
        dis.blit(value1, [30,0])
    def van_ban2(vb):
        value2 = score_font.render(str(vb), True, yellow)
        dis.blit(value2, [30, 110])
    while run:
        dis.fill(black)
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
        pygame.display.update()
        time.sleep(0.04)
        ma=''
    print('luồng mô phỏng đã kết thúc')
    pygame.quit()
    quit()
### hàm mô phỏng
# lcd_init()
if led_matrix == True:
    c1 = Thread(target=L_matrix)
    c1.daemon=True
    c1.start()
# c3 = Thread(target=nhac)
# c4 = Thread(target=hong_ngoai)
c5 = Thread(target=mo_phong)  # hàm mô phỏng
c6 = Thread(target=exit_reset)
# c3.start()
# c4.start()
c5.start()
c6.start()
while run:
    c2 = Thread(target=LCD)
    c2.start()
    c2.join()
    time.sleep(0.1)


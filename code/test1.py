import subprocess


networks = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])
def jls_extract_def():
    return 'utf-8'


jls_extract_var = jls_extract_def()
networks = networks.decode(jls_extract_var)


networks = networks.replace('\r', '')


ssid = networks.split('\n')


ssid = ssid[4:]


ssids = []


x = 0



while x < len(ssid):


    if x % 5 == 0:


        ssids.append(ssid[x])


    x += 1
print(ssids)  
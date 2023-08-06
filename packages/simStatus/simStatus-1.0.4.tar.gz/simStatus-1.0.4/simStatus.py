import qrcodeT
import requests
from requests.packages import urllib3
class simStatus():
    def __init__(self,title=None,qrcode=True,link=True):   
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        URL = "https://simstatus.nes.aau.at/backend.php"
        PARAMS = {'handle':'h363651'}
        if title is not None:
            PARAMS['p1'] = title
        r = requests.get(url = URL, params = PARAMS, verify=False).content.decode('utf-8').split(',')
        self.id = int(r[0])
        self.key = r[1]
        self.title = r[2]
        self.progress = 0
        self.status = 'no status yet'

        url2status = "https://simstatus.nes.aau.at/view.php" + "/?key=" + self.key
        if qrcode: qrcodeT.qrcodeT(url2status)
        if link:
            print('Simstatus record has been created for: ' + self.title)
            print('get updates at: ' + url2status)
            if qrcode: print('or scan the QRCode')
    def sendStatus(self,progress : int,status=None):
        self.progress = progress
        self.status = status
        URL = "https://simstatus.nes.aau.at/backend.php"
        PARAMS = {'handle':'h363652','p1':self.id,'p3':self.progress}
        if status is not None:
            PARAMS['p2'] = self.status
        return requests.get(url = URL, params = PARAMS, verify=False).content.decode('utf-8') == '1'
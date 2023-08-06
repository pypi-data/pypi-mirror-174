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
        r = requests.get(url = URL, params = PARAMS, verify=True).content.decode('utf-8').split(',')
        self.id = int(r[0])
        self.key = r[1]
        self.title = r[2]
        self.progress = 0
        self.status = 'no status yet'

        url2status = "https://simstatus.nes.aau.at/view.php" + "/?key=" + self.key
        if qrcode: qrcodeT.qrcodeT(url2status)
        if link:
            print('Simstatus record has been created for: ' + self.title)
            print('Your key is: ' + self.key)
            if qrcode: print('scan the QRCode or')
            print('get updates at: ' + url2status)
            print('you can update your simStatus externally in any python program using this command: ' + "\nimport simStatus; simStatus.sendStatus('" + self.key + "',[progess],[optional status])")
            
            print()
            print("Please report any problem to khalil.youssefi@aau.at")
    def sendStatus(self,progress : int,status=None):
        self.progress = progress
        URL = "https://simstatus.nes.aau.at/backend.php"
        PARAMS = {'handle':'h363652','p1':self.id,'p3':self.progress}
        if status is not None:
            self.status = status
            PARAMS['p2'] = self.status
        return requests.get(url = URL, params = PARAMS, verify=True).content.decode('utf-8') == '1'
class sendStatus():
    def __init__(self,key,progress : int,status=None):
        URL = "https://simstatus.nes.aau.at/backend.php"
        PARAMS = {'handle':'h363654','p1':key,'p3':progress}
        if status is not None:
            PARAMS['p2'] = status
        if(requests.get(url = URL, params = PARAMS, verify=True).content.decode('utf-8') == '1'):
            return "updated!"
        else:
            return "something went wrong, sorry!"
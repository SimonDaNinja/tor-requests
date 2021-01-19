import requests
import secrets

TOR_PROXY_IP = "127.0.0.1"
TOR_PROXY_PORT = "9050"
TOR_PROXY = TOR_PROXY_IP + ":" + TOR_PROXY_PORT

rnd = secrets.SystemRandom()
alphaNumeric = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890"


# for stream isolation (e.g., if proxy is Tor, every time new auth is used, it
# gives a new tor circuit)
def generateNewSocks5Auth(userNameLen = 30, passwordLen = 30):
    username = "".join([rnd.choice(alphaNumeric) for i in range(userNameLen)])
    password = "".join([rnd.choice(alphaNumeric) for i in range(passwordLen)])
    return username, password

def getHttpContentStringUsingSocks5(httpUrl, username = None, password = None, 
        proxy = None):
    if username is None:
        auth = ""
    else:
        auth = username
        if password is not None:
            auth += ":" + password
        auth += '@'
    if proxy is None:
        proxy = TOR_PROXY
    socksServer = 'socks5://' + auth + proxy
    proxies = {'http': socksServer, 'https': socksServer}
    rsp = requests.get(httpUrl, proxies=proxies)
    return str(rsp.content)

# as demonstration, generate 10 different tor circuits and display user's
# apparent IP. (assumes the user has Tor installed, and is currently running
#it on 127.0.0.1:9050)
if __name__ == "__main__":
    for i in range(10):
        print(f"generating new tor circuit...")
        userName, password = generateNewSocks5Auth()
        try:
            content = getHttpContentStringUsingSocks5("https://whatsmyip.com/", 
                    userName, password)
        except:
            print("can't access https://whatsmyip.com/")
        yourIpIndex = content.find("Your IP</span>")
        ipAddress= content[yourIpIndex+16:yourIpIndex+40]
        while not ipAddress[-1].isdigit():
            ipAddress = ipAddress.replace(ipAddress[-1], '')
        print(f"your apparent IP adress is: {ipAddress}")

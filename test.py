# SimonDaNinja/Tor-Requests: a bit of playing around with SOCKS5 and Tor for
# self-didactic purposes
#
# Copyright (C) 2021  Simon Liljestrand
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# The author can be reached by electronic mail at simon@simonssoffa.xyz

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
    rsp = requests.get(httpUrl, proxies = proxies)
    return str(rsp.content)

# as demonstration, generate 10 different tor circuits and display user's
# apparent IP. (assumes the user has Tor installed, and is currently running
# it on 127.0.0.1:9050)
if __name__ == "__main__":
    print("SimonDaNinja/Tor-Requests  Copyright (C) 2021  Simon Liljestrand\n" + \
    "This program comes with ABSOLUTELY NO WARRANTY.\n" + \
    "This is free software, and you are welcome to redistribute it\n" + \
    "under certain conditions.\n")
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

import json
import socket
import webbrowser

import requests


def socketserver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8080))
    sock.listen(1)
    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)
        # if the data is not empty
        if data:
            # decode the data
            data = data.decode('utf-8')
            # we get first line of the data
            code = data.split('\r')[0]
            # we get the code from the first line (after the first =)
            code = code.split('=')[1]
            # before the space
            code = code.split('&')[0]
            # send success message
            conn.send(b'HTTP/1.1 200 OK\r<br>Content-Type: text/html\r<br>\r<br>Success')
            # close the connection
            conn.close()
            # return the code
            return code
        conn.close()




# get access token
def msa(clientid="aaaf3f8c-8b99-4e7b-8265-b637bd89317e"):
    # make a server on localhost to get the code
    webbrowser.open(
        'https://login.live.com/oauth20_authorize.srf?client_id='+clientid+'&response_type'
        '=code&redirect_uri=http://localhost:8080&scope=XboxLive.signin%20offline_access&state=NOT_NEEDED')
    code = socketserver()

    url = 'https://login.live.com/oauth20_token.srf'
    data = {
        'client_id': clientid,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:8080'
    }
    output = json.dumps(requests.post(url, data=data).json())
    token = json.loads(output)['access_token']

    # now get xbox token
    url = 'https://user.auth.xboxlive.com/user/authenticate'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    data = {
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName": "user.auth.xboxlive.com",
            "RpsTicket": f"d={token}"
        },
        "RelyingParty": "http://auth.xboxlive.com",
        "TokenType": "JWT"
    }
    xbox = requests.post(url, headers=headers, json=data).json
    token = xbox()['Token']
    # uhs is in xui which is in displayclaims
    uhs = xbox()['DisplayClaims']['xui'][0]['uhs']

    # final microsoft(xsts) token
    url = 'https://xsts.auth.xboxlive.com/xsts/authorize'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    data = {
        "Properties": {
            "SandboxId": "RETAIL",
            "UserTokens": [
                token
            ]
        },
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT"
    }
    xsts = requests.post(url, headers=headers, json=data).json
    token = xsts()['Token']
    # its mojang time
    url = 'https://api.minecraftservices.com/authentication/login_with_xbox'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    data = {
        "identityToken": "XBL3.0 x=" + uhs + ';' + token,
        "ensureLegacyEnabled": "true"
    }
    mojang = requests.post(url, headers=headers, json=data).json
    token = mojang()['access_token']
    return token


def profile_info(token):
    url = 'https://api.minecraftservices.com/minecraft/profile'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return requests.get(url, headers=headers).json()


def player_attributes(token):
    url = 'https://api.minecraftservices.com/player/attributes'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return requests.get(url, headers=headers).json()


def player_blocklist(token):
    url = 'https://api.minecraftservices.com/privacy/blocklist'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return requests.get(url, headers=headers).json()


def player_certificates(token):
    url = 'https://api.minecraftservices.com/player/certificates'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return requests.post(url, headers=headers).json()


def profile_name_change_info(token):
    url = 'https://api.minecraftservices.com/minecraft/profile/namechange'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return requests.get(url, headers=headers).json()


def check_product_voucher(token, giftcode):
    url = f'https://api.minecraftservices.com/productvoucher/{giftcode}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return requests.get(url, headers=headers).json()


def name_availability(token, name):
    url = f'https://api.minecraftservices.com/minecraft/profile/name/{name}/available'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return requests.get(url, headers=headers).json()


def change_name(token, name):
    url = f'https://api.minecraftservices.com/minecraft/profile/name/{name}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return requests.put(url, headers=headers).json()


def change_skin(token, skinurl, variant):
    url = 'https://api.minecraftservices.com/minecraft/profile/skins'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    data = {
        "variant": variant,
        "url": skinurl
    }
    return requests.post(url, headers=headers, json=data).json()

def upload_skin(token, file, variant):
    url = 'https://api.minecraftservices.com/minecraft/profile/skins'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    data = {
        "variant": variant,
        "file": file
    }
    return requests.post(url, headers=headers, json=data).json()

def reset_skin(token):
    url = 'https://api.minecraftservices.com/minecraft/profile/skins'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return requests.delete(url, headers=headers).json()

def hide_cape(token):
    url = 'https://api.minecraftservices.com/minecraft/profile/capes/active'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return requests.delete(url, headers=headers).json()

def show_cape(token, capeid):
    url = 'https://api.minecraftservices.com/minecraft/profile/capes/active'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        "capeId": capeid
    }
    return requests.put(url, headers=headers, json=data).json()

def blocked_severs():
    url = 'https://sessionserver.mojang.com/blockedservers'
    return requests.get(url).text

def profile_info(token):
    url = 'https://api.minecraftservices.com/minecraft/profile'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return requests.get(url, headers=headers).json()
import json
import requests
import time
import hashlib
import hmac
import base64
import uuid


class Switchbot:
    """Switchbot Utility class"""
    def __init__(self):
        """Constructor"""
        pass

    def read_token(self):
        """Import access token and secret from settings.json"""
        with open('settings.json', 'r') as f:
            settings = json.load(f)

        token = settings['token']
        secret = settings['secret']

        return token, secret

    def gen_sign(self):
        """Generate Switchbot API v1.1 sign header

        Returns:
        Switchbot API v1.1 sign header
        """

        token, secret = self.read_token()

        nonce = str(uuid.uuid4())
        t = int(round(time.time() * 1000))
        string_to_sign = '{}{}{}'.format(token, t, nonce)

        string_to_sign = bytes(string_to_sign, 'utf-8')
        secret = bytes(secret, 'utf-8')

        sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

        header = {}
        header["Authorization"] = token
        header["sign"] = str(sign, 'utf-8')
        header["t"] = str(t)
        header["nonce"] = nonce

        return header

    def _devicelist(self):
        """Create all Switchbot device list as deviceList.txt"""
        header = self.gen_sign()
        response = requests.get("https://api.switch-bot.com/v1.1/devices", headers=header)
        devices = json.loads(response.text)

        with open('deviceList.txt', 'w', encoding='utf-8', newline='\n') as f:
            for device in devices['body']['deviceList']:
                f.write(device['deviceId'] + ', ')
                f.write(device['deviceName'] + ', ')
                f.write(device['deviceType'] + ', ')
                f.write(device['hubDeviceId'] + '\n')
        
            for device in devices['body']['infraredRemoteList']:
                f.write(device['deviceId'] + ', ')
                f.write(device['deviceName'] + ', ')
                f.write(device['remoteType'] + ', ')
                f.write(device['hubDeviceId'] + '\n')

    def _get_scene_list(self):
        """Get scene List as sceneList.txt"""
        header = self.gen_sign()
        response = requests.get("https://api.switch-bot.com/v1.1/scenes", headers=header)
        scenes = json.loads(response.text)

        with open('sceneList.txt', 'w', encoding='utf-8', newline='\n') as f:
            for scene in scenes['body']:
                f.write(scene['sceneId'] + ', ')
                f.write(scene['sceneName'] + '\n')

    def _scene_execute(self, sceneId):
        """Execute scene"""
        header = self.gen_sign()
        url = "https://api.switch-bot.com/v1.1/scenes/" + sceneId + "/execute"
        response = requests.post(url=url, headers=header)
        return response.text

import time
import requests
import json


class DeathByCaptcha:
    URL = "http://api.dbcapi.me/api/captcha"


    def __init__(self,token):
        self.token = token

    def resolveHCaptcha(self,sitekey,pageurl,proxy="",proxytype="",timeout=30):
        hcaptcha_params = {
            "proxy": proxy,
            "proxytype": proxytype,
            "sitekey": sitekey,
            "pageurl": pageurl
        }

        payload = {
            'authtoken': self.token,
            'type': '7',
            'hcaptcha_params': json.dumps(hcaptcha_params)
        }

        response = requests.request("POST", self.URL, data=payload)
        if response.status_code != 200:
            raise Exception(response.text)
        
        data = {x.split('=')[0]:x.split('=')[1] for x in response.text.split("&")}
        if data["is_correct"] == "0":
            raise Exception("Data Sent is not correct!")

        return self.waitSolution(data["captcha"],timeout=timeout) 


    def waitSolution(self,captcha,timeout=30):
        start = time.time()
        response = requests.request("GET", f"{self.URL}/{captcha}")
        data = {x.split('=')[0]:x.split('=')[1] for x in response.text.split("&")}
        if data["is_correct"] == "0":
            raise Exception("Data received is not correct!")
        if timeout <= 0:
            raise Exception("Timeout solving captcha")
        if data["text"] == "":
            count = time.time()- start
            return self.waitSolution(captcha,timeout-count)
        
        return data["text"]




# token = "24O1yDML8D42jvI4fz8N148k9mSFHMqMKHS2aQdQkG7lf1TBY2yretQ1RIR290H0pM9BK6AYlSbj9T93iuB48Dt9VW84BI5ibLaBu9S549ZsV1pWMFKv5Eu7Dte8x4Ohhgx3q4zBKto8rJLv4L6wChR2M66M"
# dth = DeathByCaptcha(token)
# solved = dth.resolveHCaptcha("af4fc5a3-1ac5-4e6d-819d-324d412a5e9d","https://solucoes.receita.fazenda.gov.br/",timeout=30)

# a = 1




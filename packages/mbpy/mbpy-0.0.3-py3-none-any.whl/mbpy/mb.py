import http.client
import json

class MBAPI:
    def __init__(self, token):
        self.token=token

    async def post(self,url,data):
        conn = http.client.HTTPSConnection("dev.microbees.com")
        headers = {
            'Content-type':'application/json',
            'Accept':'application/json',
            'Authorization':'Bearer '+self.token
        }
        conn.request("POST", "/v/1_0/"+url, data, headers)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        return (data.decode("utf-8"))

     async def get(self,url,data):
        conn = http.client.HTTPSConnection("dev.microbees.com")
        headers = {
            'Content-type':'application/json',
            'Accept':'application/json',
            'Authorization':'Bearer '+self.token
        }
        conn.request("GET", "/v/1_0/"+url, data, headers)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        return (data.decode("utf-8"))

    async def delete(self,url,data):
        conn = http.client.HTTPSConnection("dev.microbees.com")
        headers = {
            'Content-type':'application/json',
            'Accept':'application/json',
            'Authorization':'Bearer '+self.token
        }
        conn.request("DELETE", "/v/1_0/"+url, data, headers)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        return (data.decode("utf-8"))

    async def put(self,url,data):
        conn = http.client.HTTPSConnection("dev.microbees.com")
        headers = {
            'Content-type':'application/json',
            'Accept':'application/json',
            'Authorization':'Bearer '+self.token
        }
        conn.request("PUT", "/v/1_0/"+url, data, headers)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        return (data.decode("utf-8"))

    async def patch(self,url,data):
        conn = http.client.HTTPSConnection("dev.microbees.com")
        headers = {
            'Content-type':'application/json',
            'Accept':'application/json',
            'Authorization':'Bearer '+self.token
        }
        conn.request("PATCH", "/v/1_0/"+url, data, headers)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        return (data.decode("utf-8"))

from time import sleep,time
import urllib.parse
import redis
import json
from .Job import Job

class Preset:

    def __init__(self,Asset,id=None,name=None):
        if not id and not name:
            raise TypeError("Please specify either the name or id of the preset")
        self.Rally = Asset.Rally
        self.Asset = Asset
        self.id = id
        self.name = name
        if not id:
            try:
                self.id = self.Rally.apiCall("GET","/presets?filter=name={}".format(urllib.parse.quote_plus(name)))["data"][0]["id"]
            except IndexError:
                raise ValueError("Could not find preset with name '{}'".format(name)) from None

    def getName(self):
        self.name = self.Rally.apiCall("GET","/presets/{}".format(self.id))["data"]["attributes"]["name"]
        return self.name

    def run(self,dynamicPresetData={},timeout=5,protectProd=True):
        if not any([silo in self.Rally.apiUrl for silo in ["dev","qa","uat"]]) and protectProd:
            raise ValueError("Production assets are read only") from None
        self.Rally.apiCall("PATCH","/userMetadata/{}".format(self.Asset.id),body={"data":{"attributes":{"metadata":{"testMode":True}},"type":"userMetadata"}})
        jobId = self.Rally.apiCall("POST","/jobs",body={"data":{"type":"jobs", "attributes":{"dynamicPresetData":dynamicPresetData}, "relationships": {"movie":{"data":{"id": self.Asset.id,"type": "movies",}},"preset":{"data": {"id": self.id,"type": "presets",}}}}})["data"]["id"]
        if self.Rally.redisUrl:
            redisClient = redis.Redis.from_url(url=self.Rally.redisUrl,ssl_cert_reqs=None)
            subscriber = redisClient.pubsub()
            subscriber.subscribe('messagebus')
            start_time = time()
            delay = 0.1
            while (time()-start_time < timeout):
                response = subscriber.get_message()
                if response and response["data"] != 1:
                    data = json.loads(response["data"])
                    result = data.get("resourceState",{}).get("data",{}).get("attributes",{}).get("result")
                    if jobId == data["resourceId"] and result != None:
                        return Job(Preset=self,id=jobId,attributes=data.get("resourceState",{}).get("data",{}).get("attributes",{}))
                sleep(delay)
        else:
            start_time = time()
            delay = 2
            while (time()-start_time < timeout):
                sleep(delay)
                job = self.Rally.apiCall("GET","/jobs/{}".format(jobId))["data"]
                if job["attributes"]["state"] not in ["Queued","Active"]:
                    self.Rally.apiCall("PATCH","/userMetadata/{}".format(self.Asset.id),body={"data":{"attributes":{"metadata":{"testMode":None}},"type":"userMetadata"}})
                    return Job(Preset=self,id=jobId,attributes=job["attributes"])

    def job(self,id=None,attributes=None):
        return Job(self,id=id,attributes=attributes)
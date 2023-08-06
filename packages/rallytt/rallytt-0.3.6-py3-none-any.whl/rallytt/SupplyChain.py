from .Job import Job
from time import sleep,time
import urllib.parse
import json
import redis
from .functions import *
class SupplyChain:

    def jsonPath(obj,pathString):
        pathParts = pathString.split(".")
        for pathPart in pathParts:
            obj = obj.get(pathPart,{}) or {}
        return obj

    def __init__(self,Asset,id=None,name=None):
        if not id and not name:
            raise TypeError("Please specify either the name or id of the rule that starts the supply chain")
        self.Rally = Asset.Rally
        self.Asset = Asset
        self.id = id
        self.name = name
        if not id:
            try:
                self.id = self.Rally.apiCall("GET","/workflowRules?filter=name={}".format(urllib.parse.quote_plus(name)))["data"][0]["id"]
            except IndexError:
                raise ValueError("Could not find rule with name '{}'".format(name)) from None

    def run(self,initData={},endingPresetName=None,endingPresetId=None,timeout=15,protectProd=True):
        if not any([silo in self.Rally.apiUrl for silo in ["dev","qa","uat"]]) and protectProd:
            raise ValueError("Production assets are read only") from None
        if endingPresetName and not endingPresetId:
            endingPresetId = self.Asset.preset(name=endingPresetName).id
        self.Rally.apiCall("PATCH","/userMetadata/{}".format(self.Asset.id),body={"data":{"attributes":{"metadata":{"testMode":True}},"type":"userMetadata"}})
        baseWorkflow = self.Rally.apiCall("POST","/workflows",body={"data":{"type":"workflows", "attributes":{"initData":json.dumps(initData)}, "relationships": {"movie":{"data":{"id": self.Asset.id,"type": "movies",}},"workflowRule":{"data": {"id": self.id, "type": "workflowRules",}}}}})["data"]
        jobs = []
        workflows = [baseWorkflow]
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
                    attributes = jsonPath(data,"resourceState.data.attributes") or {}
                    relationships = jsonPath(data,"resourceState.data.relationships") or {}
                    result = attributes.get("result")
                    if data["resourceType"] == "workflows":
                        assetId = jsonPath(relationships,"baseWorkflow.data.id")
                        baseWorkflowId = jsonPath(relationships,"asset.data.id")
                        if baseWorkflow["id"] == data["resourceId"] and result != None:
                            break
                        elif assetId == self.Asset.id and baseWorkflowId == baseWorkflow["id"]:
                            workflows.append(jsonPath(data,"resourceState.data"))
                            workflows = list({v['id']:v for v in workflows}.values())
                    elif data["resourceType"] == "jobs":
                        workflowId = jsonPath(relationships,"workflow.data.id")
                        if workflowId in [i["id"] for i in workflows] and result != None:
                            if endingPresetId == jsonPath(relationships,"preset.data.id"):
                                break
        else:
            delay = 5
            start_time = time()
            while (time()-start_time < timeout):
                sleep(delay)
                baseWorkflow = self.Rally.apiCall("GET","/workflows/{}".format(baseWorkflow["id"]))["data"]
                workflows = [baseWorkflow]
                childWorkflows = [item for item in self.Rally.apiCall("GET","/workflows?filter=assetId={}".format(self.Asset.id),paginate=True)["data"] if item["relationships"]["baseWorkflow"]["data"]["id"] == baseWorkflow["id"] and item["id"] != baseWorkflow["id"]]
                workflows.extend(childWorkflows)
                if baseWorkflow["attributes"]["result"] != None:
                    break
                if endingPresetId:
                    for workflow in workflows:
                        endingPresetJob = self.Rally.apiCall("GET","/jobs?filter=workflowId={},presetId={}".format(workflow["id"],endingPresetId),paginate=True)["data"]
                        if len(endingPresetJob) != 0:
                            if endingPresetJob[0]["attributes"]["result"] != None:
                                break
                    else:
                        continue
                    break
        for workflow in workflows:
            workflow_jobs = [i["id"] for i in self.Rally.apiCall("GET","/workflows/{}".format(workflow["id"]))["data"]["relationships"]["jobs"]["data"]]
            for workflow_job in workflow_jobs:
                job_data = self.Rally.apiCall("GET","/jobs/{}".format(workflow_job))["data"]
                if job_data["attributes"]["result"] != None:
                    jobs.append(Job(self,id=job_data["id"],attributes=job_data["attributes"]))     
                else:
                    self.Rally.apiCall("PATCH","/jobs/{}".format(job_data["id"]),body={"data":{"type":"jobs", "attributes":{"state":"Cancelled"}}},fullResponse=True,errors=False)
        self.Rally.apiCall("PATCH","/userMetadata/{}".format(self.Asset.id),body={"data":{"attributes":{"metadata":{"testMode":None}},"type":"userMetadata"}})
        return jobs
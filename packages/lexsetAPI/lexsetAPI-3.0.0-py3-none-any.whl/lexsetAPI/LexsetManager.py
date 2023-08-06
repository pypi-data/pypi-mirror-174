import requests
import json
import time
import yaml
import base64

# This class will No longer be supported in version 4+ of the API
class simulation:

    def __init__(self,token,simPath,numImages,user,nodes,name,descript,seed):
        self.token = token
        self.name = "works"
        self.numImages = numImages
        self.simName = name
        self.description = descript
        self.randomSeed = seed
        self.progress = ""
        self.simID = 0
        self.userID = user
        self.nodeCount = nodes
        self.dataID = 0
        self.simPath = simPath
        self.simEncodedstr = "simEncodedstr"
        self.datasetURL = "datasetURL"
        self.simulations = ""
        self.numSimulations = 0
        self.isComplete = False
        self.dataSetItems = ""
        self.numRendered = 0
        self.progress = "you have rendered "+ str(self.numRendered) + "(images including image annotations) out of a total of " + str(self.numImages)

    def createSimulation(self):
        url = "https://lexsetapi.azurewebsites.net/api/Simulations/NewSimulation"

        #encode the config in Base64
        with open(self.simPath) as fast:
            simString = json.dumps(yaml.load(fast, Loader=yaml.FullLoader))
            simEncoded = base64.b64encode(simString.encode("utf-8"))
            self.simEncodedstr = str(simEncoded, "utf-8")

        payload = json.dumps({
          "id": 0,
          "userid": self.userID,
          "name": self.simName,
          "description": self.description,
          "simulationconfig": self.simEncodedstr,
          "requestednodecount": self.nodeCount,
          "randomseed": self.randomSeed,
          "renderjobid": 0,
          "imagecount": self.numImages
        })
        headers = {
          'Authorization': 'Bearer ' + self.token,
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        parseResponse = json.loads(response.text)

        #update simulation IDs
        self.simID = parseResponse["id"]
        self.dataID = parseResponse["datasetid"]
        self.userID = parseResponse["userid"]

    def startSimulation(self):
        url = "https://lexsetapi.azurewebsites.net/api/Simulations/StartSimulation?id=" + str(self.simID)

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.token
        }

        response = requests.request("POST", url, headers=headers, data=payload)

    def getStatus(self):
        url = "https://lexsetapi.azurewebsites.net/api/simulations/getsimulationstatus?id=" + str(self.simID)

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response_code = response.status_code
        if response_code == 401:
            return("Unauthorized")
        if response_code == 200:
            #update if sim is complete or not complete
            parseResponse = json.loads(response.text)
            self.isComplete = parseResponse["isComplete"]

    def getProgress(self):
        url = "https://lexsetapi.azurewebsites.net/api/simulations/getstatus?id=" + str(self.simID)

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        #update if sim is complete or not complete
        parseResponse = json.loads(response.text)
        print(parseResponse)
        #self.isComplete = parseResponse["isComplete"]

    def getDatasetItems(self):
        url = "https://lexsetapi.azurewebsites.net/api/datasetitems/getdatasetitems?dataset_id=" + str(self.dataID)

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        #return the dataSetItems and check the status/progress
        parseResponse = json.loads(response.text)
        self.dataSetItems = json.loads(response.text)
        self.numRendered = len(self.dataSetItems)
        self.progress = "you have rendered "+ str(self.numRendered) + " out of " + str(self.numImages)

    def stopSimulation(self):
        url = "https://lexsetapi.azurewebsites.net/api/simulations/stopsimulation?id=" + str(self.simID)

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.token
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

    def downloadData(self):
        url = "https://lexsetapi.azurewebsites.net/api/datasets/getdatasetarchives?dataset_id=" + str(self.dataID)

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)
        parseResponse = json.loads(response.text)
        print("Response:")
        print(response.text)
        self.datasetURL = parseResponse[0]["url"]
        if len(parseResponse) > 0:
            resp = requests.get(self.datasetURL, allow_redirects=True)
            open('dataset.zip', 'wb').write(resp.content)
        else:
            return("Dataset zipping")

def getDatasetID(id,userToken):
    url = "https://lexsetapi.lexset.ai/api/simulations/getsimulationstatus?id=" + str(id)

    payload={}
    headers = {
    'Authorization': 'Bearer ' + str(userToken)
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    getCode = response.status_code

    if getCode == 401:
        return("Unauthorized")
    if getCode == 200:
        parseResponse = json.loads(response.text)
        return parseResponse["datasets"][0]["id"]
    else:
        print("Error: " + str(getCode))
        return(getCode)

def listSimulations(id,userToken):
    url = "https://lexsetapi.azurewebsites.net/api/simulations/GetActiveSimulations/?userid=" + str(id)

    payload={}
    headers = {
    'Authorization': 'Bearer ' + str(userToken)
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    getCode = response.status_code

    if getCode == 401:
        return("Unauthorized")
    if getCode == 200:
        parseResponse = json.loads(response.text)
        return(parseResponse)
    else:
        print("Error: " + str(getCode))
        return(getCode)

def addRule(userID,configFile,userToken):
    # Remove in future versions
    url = "https://lexsetapi.lexset.ai/api/UserDataManagement/uploaduserfile"

    payload={'userid': str(userID)}

    path = str(configFile)

    name = path.split("/")
    files=[('files',(str(name[len(name)-1]),open(str(path),'rb'),'application/octet-stream'))]
    headers = {'Authorization': 'Bearer ' + str(userToken)}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)

def addColorMap(userID,configFile,userToken):
    # Remove in future versions
    url = "https://lexsetapi.lexset.ai/api/UserDataManagement/uploaduserfile"

    payload={'userid': str(userID),'filetype': '1'}
    print(payload)
    path = str(configFile)

    name = path.split("/")

    files=[('files',(str(name[len(name)-1]),open(str(path),'rb'),'application/octet-stream'))]
    headers = {'Authorization': 'Bearer ' + str(userToken)}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)

def listUploads(user):
    url = "http://lexsetapi.azurewebsites.net/api/UserDataManagement/getplacementfiles?userid=" + str(user)
    payload = {}

    headers = {}

    getCode = requests.status_codes

    if getCode == 401:
        return("Unauthorized")
    if getCode == 200:
        response = requests.request("GET", url, headers=headers, data=payload)
        print("uploadedFiles")
        print(response.text)
    else:
        print("Error: " + str(getCode))
        return(getCode)

def stop(simulationID,token):
    url = "https://lexsetapi.azurewebsites.net/api/simulations/stopsimulation?id=" + str(simulationID)

    payload={}
    headers = {
    'Authorization': 'Bearer ' + token
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    getCode = response.status_code
    if getCode == 401:
        return("Unauthorized")
    if getCode == 200:
        parseResponse = json.loads(response.text)
        return(parseResponse)
    else:
        print("Error: " + str(getCode))
        return(getCode)

def start(simulationID,token):
    url = "https://lexsetapi.azurewebsites.net/api/Simulations/StartSimulation?id=" + str(simulationID)

    payload={}
    headers = {
    'Authorization': 'Bearer ' + token
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    getCode = response.status_code
    if getCode == 401:
        return("Unauthorized")
    if getCode == 200:
        parseResponse = json.loads(response.text)
        return(parseResponse)
    else:
        print("Error: " + str(getCode))
        return(getCode)

def download(datasetID ,userToken, localPath = "NONE"):
    url = "https://lexsetapi.azurewebsites.net/api/datasets/getdatasetarchives?dataset_id=" + str(datasetID)

    payload={}
    headers = {
    'Authorization': 'Bearer ' + userToken
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    #print(response.text)
    parseResponse = json.loads(response.text)

    getCode = response.status_code
    if getCode == 401:
        return("Unauthorized")
    
    if getCode == 200:
        datasetURL = parseResponse[0]["url"]
        resp = requests.get(datasetURL, allow_redirects=True)
        if(localPath == "NONE"):
            localPath = "dataset.zip"
        open(localPath, 'wb').write(resp.content)
        output ={
            "local path": localPath,
            "dataset url": datasetURL,
            "dataset ID": datasetID,
            "file name": localPath.split("/")[-1]
        }
        print(output)
        return(json.dumps(output))
    else:
        output ={
            "local path": localPath,
            "dataset url": "Dataset zipping",
            "dataset ID": datasetID,
            "file name": "NONE"
        }
        print(output)
        return(json.dumps(output))

def getProgress(simID,token):
    url = "https://lexsetapi.azurewebsites.net/api/simulations/getstatus?id=" + str(simID)

    payload={}
    headers = {
    'Authorization': 'Bearer ' + token
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    getCode = response.status_code
    if getCode == 401:
        return("Unauthorized")
    if getCode == 200:
        parseResponse = json.loads(response.text)
        return(parseResponse)
    else:
        print("Error: " + str(getCode))
        return(getCode)

def getStatus(simID, token):
    url = "https://lexsetapi.azurewebsites.net/api/simulations/getsimulationstatus?id=" + str(simID)

    payload={}
    headers = {
    'Authorization': 'Bearer ' + token
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    getCode = response.status_code
    if getCode == 401:
        return("Unauthorized")
    if getCode == 200:
        #update if sim is complete or not complete
        parseResponse = json.loads(response.text)
        if parseResponse == None:
            return False
        else:
            isComplete = parseResponse["isComplete"]

            return(isComplete)
    else:
        print("Error: " + str(getCode))
        return(getCode)


# batch simulation functionality

class activateSimulation:

    def __init__(self,simID, user, token):
        self.token = token
        self.progress = ""
        self.simID = simID
        self.userID = user
        self.hasStarted = False
        self.nodeCount = 5
        self.dataID = 0
        self.simEncodedstr = "simEncodedstr"
        self.datasetURL = "datasetURL"
        self.simulations = ""
        self.numSimulations = 0
        self.isComplete = False
        self.dataSetItems = ""
        self.numRendered = 0

    def startSimulation(self):
        url = "https://lexsetapi.azurewebsites.net/api/Simulations/StartSimulation?id=" + str(self.simID)

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.token
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        getCode = response.status_code
        if getCode == 401:
            return("Unauthorized")
        if getCode == 200:
            print('NEW JOB STARTED: ' + str(self.simID) + ' has started')
            print('-------------')
        else:
            print("Error: " + str(getCode))
            return(getCode)

    def updateStatus(self):
        url = "https://lexsetapi.azurewebsites.net/api/simulations/getsimulationstatus?id=" + str(self.simID)

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        getCode = response.status_code

        if getCode == 401:
            return("Unauthorized")
        if getCode == 200:
            #update if sim is complete or not complete
            parseResponse = json.loads(response.text)
            self.nodeCount = parseResponse["requestedNodeCount"]
            self.hasStarted = parseResponse["hasStarted"]
            self.isComplete = parseResponse["isComplete"]
        else:
            print("Error: " + str(getCode))
            return(getCode)

    def getProgress(self):
        url = "https://lexsetapi.azurewebsites.net/api/simulations/getstatus?id=" + str(self.simID)

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        getCode = response.status_code
        if getCode == 401:
            return("Unauthorized")
        if getCode == 200:
            #update if sim is complete or not complete
            parseResponse = json.loads(response.text)
            print(parseResponse)
        else:
            print("Error: " + str(getCode))
            return(getCode)


    def stopSimulation(self):
        url = "https://lexsetapi.azurewebsites.net/api/simulations/stopsimulation?id=" + str(self.simID)

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.token
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        getCode = response.status_code

        if getCode == 401:
            return("Unauthorized")  
        if getCode == 200:
            print(response.text)
        else:
            print("Error: " + str(getCode))
            return(getCode)

    def downloadData(self):
        url = "https://lexsetapi.azurewebsites.net/api/datasets/getdatasetarchives?dataset_id=" + str(self.dataID)

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        getCode = response.status_code

        if getCode == 401:
            return("Unauthorized")
        if getCode == 200:
            print(response.text)
            parseResponse = json.loads(response.text)
            print("Response:")
            print(response.text)
            self.datasetURL = parseResponse[0]["url"]
            if len(parseResponse) > 0:
                resp = requests.get(self.datasetURL, allow_redirects=True)
                open('dataset.zip', 'wb').write(resp.content)
            else:
                return("Dataset zipping")
        else:
            print("Error: " + str(getCode))
            return(getCode)


def activeSimulationNodes(userID, token):
    url = "https://lexsetapi.azurewebsites.net/api/simulations/GetActiveSimulations/?userid=" + str(userID)

    payload={}
    headers = {
    'Authorization': 'Bearer ' + token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    
    parseResponse = json.loads(response.text)
    getCode = response.status_code
    if getCode == 401:
        return("Unauthorized")
    if getCode == 200:
        #update if sim is complete or not complete
        nodes = 0
        y = parseResponse

        for item in range(len(y)):
        
            if (y[item]['hasStarted']== True) :
                nodes = nodes + int(y[item]['requestedNodeCount'])

        return nodes
    else:
        print("Error: " + str(getCode))
        return(getCode)


#http request to get compute resources endpoint
def getComputeResources(id,userToken):
    url = "https://seahaven.lexset.ai/api/accountusage/GetActiveComputeNodeCount?userid=" + str(id)

    payload={}
    headers = {
    'Authorization': 'Bearer ' + userToken
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    getCode = response.status_code
    if getCode == 401:
        return("Unauthorized")
    if getCode == 200:
        parseResponse = json.loads(response.text)
        return(parseResponse)
    else:
        print("Error: " + str(getCode))
        return(getCode)
    
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\n"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'{prefix} |{bar}| {percent}% {suffix}', end = printEnd)


def batchSimulation(queue, allNodes, userID,token):

    state = []
    runningNodes = activeSimulationNodes(userID, token)
    for item in range(len(queue)):
        queue[item].updateStatus()
        state.append(queue[item].hasStarted)
        x = all(state)

    while x == False:
        #runningNodes = activeSimulationNodes(3,token)
        for item in range(len(queue)):
            if (queue[item].hasStarted == True and queue[item].isComplete == False):
                print('\033[2KSimulation [' + str(queue[item].simID) + '] : ', end='')
                printProgressBar(queue[item].getProgress(), 100, prefix='Running', length=50)
                    
            if (queue[item].hasStarted == True and queue[item].isComplete == True):
                print('\033[2KSimulation [' + str(queue[item].simID) + '] : Complete')
                    
            if (queue[item].hasStarted == False and queue[item].isComplete == False):
                print('\033[2KSimulation [' + str(queue[item].simID) + '] : Not yet started')

        print('\033['+str(len(queue)+1)+'A')

        for item in range(len(queue)):
            time.sleep(5)
            runningNodes = activeSimulationNodes(userID,token)
            queue[item].updateStatus()
            if (queue[item].nodeCount + runningNodes <= allNodes and queue[item].hasStarted == False) :
                queue[item].startSimulation()
                time.sleep(5)
                
            state[item]=queue[item].hasStarted
            x = all(state)

    for item in range(len(queue)):
        if (queue[item].hasStarted == True and queue[item].isComplete == False):
            print('\033[2KSimulation [' + str(queue[item].simID) + '] : ', end='')
            printProgressBar(queue[item].getProgress(), 100, prefix='Running', length=50)
                
        if (queue[item].hasStarted == True and queue[item].isComplete == True):
            print('\033[2KSimulation [' + str(queue[item].simID) + '] : Complete')
                
        if (queue[item].hasStarted == False and queue[item].isComplete == False):
            print('\033[2KSimulation [' + str(queue[item].simID) + '] : Not yet started')

    print("All simulations in queue have been started.")

def getOrganizationSimulations(orgID,state,token):

    # //Possible States
    # // RUNNING
    # // COMPLETED
    # // CREATED

    url = "https://lexsetapi.lexset.ai/api/Simulations/GetSimulationsByOrganization?orgid=" + (str(orgID)) +"&state=" + state

    payload={}
    headers = {
    'Authorization': 'Bearer ' + token
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    getCode = response.status_code

    if getCode == 401:
        return("Unauthorized")
    if getCode == 200:
        parseResponse = json.loads(response.text)
        return(parseResponse)
    else:
        print("Error: " + str(getCode))
        return(getCode)

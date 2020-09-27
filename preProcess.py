import json

preConf = {'removeID' : '_A_'}

try:
    with open('pre.json') as configdata:
        preConf = json.load(configdata)
except:
    print('no config file, defaulting preprocess')

    

def removeUnwanted(Filelist): #remove unwated csv from file list
    #print(Filelist)
    newFilelist = []
    for i in Filelist:
        if preConf['removeID'] in i[2]: #removes file from list if identifies is found
            print('removing %s'%i[2])
        else:
            newFilelist.append(i)
    return(newFilelist)

def findUnitID(file): #returns the unitID, eg SIM1, form the file name
    return(file.split('_')[0])


def updateMeasureID(id, configDir): #reads json file and updates measurement name with unit id

    with open(configDir) as configdata:
        configID = json.load(configdata)
    
    configID['measurementName'] = id
    #print(configID)
    return(configID)

def runPreProcess(filein, config):
    fileID = findUnitID(filein) #extracts device ID from the file name
    jsonblob = updateMeasureID(fileID, config) #updates the json file with this new ID
    return jsonblob
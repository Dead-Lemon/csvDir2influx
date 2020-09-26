import json
import csvToInfluxdb
import hashDir
import preProcess


filelist = []
filelist = (hashDir.getNewFiles('sample', '.hashstore'))
filelist = preProcess.removeUnwanted(filelist)
#preProcess.findUnitID('SIM1_T_20200914.csv')
#preProcess.updateMeasureID('SIM3', 'csv.json')

try:
    for i in filelist:
        fileID = preProcess.findUnitID(i[2])
        jsonblob = preProcess.updateMeasureID(fileID, 'csv.json')
        csvToInfluxdb.loadCsv(i[1], jsonblob)
except:
    print("nothing to do")

#csvToInfluxdb.loadConfig('sample/SIM1_T_20200914.csv', 'csv.json')


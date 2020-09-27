import json
import csvToInfluxdb
import hashDir
import preProcess


filelist = []
filelist = (hashDir.getNewFiles('sample', '.hashstore'))
filelist = preProcess.removeUnwanted(filelist)

try:
    for i in filelist: #[i = HASH, Full path to file, filename]
        fileID = preProcess.findUnitID(i[2])
        jsonblob = preProcess.updateMeasureID(fileID, 'csv.json')
        csvToInfluxdb.loadCsv(i[1], jsonblob)
except:
    print("nothing to do")

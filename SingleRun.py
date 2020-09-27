# Single run of script, possibly used with cron trigger.
# Keeps file comparison and uploads new files
import argparse
import json
import csvToInfluxdb
import hashDir
import preProcess

def runImport(inputfiles, config, hashstore, preprocess):
    filelist = []
    filelist = hashDir.getNewFiles(inputfiles, hashstore) #checks is there is any changed files and return a list
    if preprocess: #probably not usable for any one but me, but this is how I'm allowing modability to my scripts
        print("PreProcess selected")
        filelist = preProcess.removeUnwanted(filelist) #removes files, based on a set phrase, from the file list.
        for i in filelist: #[i = HASH, Full path to file, filename]
            jsonblob = preProcess.runPreProcess(i[2], config)
            csvToInfluxdb.loadCsv(i[1], jsonblob) #passes the the json object into the csv import script        
    else:
        for i in filelist: #[i = HASH, Full path to file, filename]
            csvToInfluxdb.loadConfig(i[1], config) 
    
    print("Import Done")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='csv to influxdb')

    parser.add_argument('-i', '--input', nargs='?', required=True,
                        help='Input folder to watch')

    parser.add_argument('-c', '--config', nargs='?', default='csv.json',
                        help='config file location')

    parser.add_argument('-s', '--hashstore', nargs='?', default='.hashstore',
                        help='hashed file store')

    parser.add_argument('-p', '--preprocess', nargs='?', default=False,
                        help='enable use of preprocessing script')

    args = parser.parse_args()

    runImport(args.input, args.config, args.hashstore, args.preprocess)



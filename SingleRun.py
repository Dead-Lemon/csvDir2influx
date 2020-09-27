# Single run of script, possibly used with cron trigger.
# Keeps file comparison and uploads new files



import json
import csvToInfluxdb
import hashDir
#import preProcess

def runImport(inputfiles, config, hashstore)
    filelist = []
    filelist = hashDir.getNewFiles(inputfiles, hashstore)
    #filelist = preProcess.removeUnwanted(filelist)

    try:
        for i in filelist: #[i = HASH, Full path to file, filename]
            csvToInfluxdb.loadConfig(i[1], config)
    except:
        print("nothing to do")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='csv to influxdb')

    parser.add_argument('-i', '--input', nargs='?', required=True,
                        help='Input folder to watch')

    parser.add_argument('-c', '--config', nargs='?', default='csv.json',
                        help='config file location')

    parser.add_argument('-s', '--hashstore', nargs='?', default='.hashstore',
                        help='hashed file store')

    args = parser.parse_args()

    runImport(args.input, args.configm args.hashstore)



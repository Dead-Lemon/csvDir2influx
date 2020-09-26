import inotify.adapters
import argparse
import csvToInfluxdb
import hashDir
import postProcess
import time


def filesFound(fileList, postprocess):
    for files in filesList:
        if postprocess:
            postProcess.run(files)
        else:
            csvToInfluxdb.loadCsv(inputfilename, servername, user, password, dbname, metric, 
            timecolumn, timeformat, tagcolumns, fieldcolumns, usegzip, 
            delimiter, batchsize, create, datatimezone, usessl, singletag, fieldname)



def folderwatch(folderpath, postprocess):

    i = inotify.adapters.Inotify()

    i.add_watch(folderpath) #set folder to watch for changes

    for event in  i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event #extracts the topics of interest, as taken from the example
        #print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(path, filename, type_names)) #displays the info from the differnt topics
        
        if 'IN_CLOSE_WRITE' in type_names: #looks for a file that has been written to, indicated IOT device has uploaded new logs
            print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(path, filename, type_names)) #displays the info from the differnt topics
            time.sleep(1) #delay to ensure IOT FTP uploads are done
            newFiles = hashDir.getNewFiles(folderpath, '.oldhash')
            if newFiles == []:
                print("nothing to do")
            else:
                filesFound(newFiles, postprocess)

        



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='folder activity trigger')

    parser.add_argument('-i', '--input', nargs='?', required=True,
                        help='Input folder to watch')

    parser.add_argument('-p', '--postprocess', nargs='?', default=False,
                        help='enable custom postprocess script')

    parser.add_argument('-c', '--config', nargs='?', default='csv.conf',
                        help='config file location')

    args = parser.parse_args()

    folderwatch(args.input, args.postprocess, args.config)



#(_INOTIFY_EVENT(wd=1, mask=8, cookie=0, len=32), ['IN_CLOSE_WRITE'], '/home/pointftp/SIM1', u'SIM1_A_20200913.csv')
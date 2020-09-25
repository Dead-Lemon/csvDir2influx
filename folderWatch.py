import inotify.adapters
import argparse
import csvToInfluxdb
import hashDir


def folderwatch(folderpath):

    i = inotify.adapters.Inotify()

    i.add_watch(folderpath) #set folder to watch for changes

    for event in  i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event #extracts the topics of interest, as taken from the example
        
        print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(path, filename, type_names)) #displays the info from the differnt topics
        
        if 'IN_CLOSE_WRITE' in type_names: #looks for a file that has been written to, indicated IOT device has uploaded new logs
            sleep(20)
            newFiles = hashDir.getNewFiles(folderpath, '.oldhash')
            if newFiles == []:
                print("nothing to do")
            else:
                print(newFiles)

        



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='folder activity trigger')

    parser.add_argument('-i', '--input', nargs='?', required=True,
                        help='Input folder to watch')

    args = parser.parse_args()

    folderwatch(args.input)



#(_INOTIFY_EVENT(wd=1, mask=8, cookie=0, len=32), ['IN_CLOSE_WRITE'], '/home/pointftp/SIM1', u'SIM1_A_20200913.csv')
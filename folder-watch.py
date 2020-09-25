import inotify.adapters
import argparse
#import csv-to-influxdb



def folderwatch(folderpath):

    i = inotify.adapters.Inotify()

    i.add_watch(folderpath)

    for event in  i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(path, filename, type_names))
        if 'IN_CLOSE_WRITE' in type_names:
            print('found file to have updated')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='folder activity trigger')

    parser.add_argument('-i', '--input', nargs='?', required=True,
                        help='Input folder to watch')

    args = parser.parse_args()

    folderwatch(args.input)



#(_INOTIFY_EVENT(wd=1, mask=8, cookie=0, len=32), ['IN_CLOSE_WRITE'], '/home/pointftp/SIM1', u'SIM1_A_20200913.csv')
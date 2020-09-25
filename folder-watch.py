import inotify.adapters
import argparse
import csv-to-influxdb



def folderwatch(folderpath):
    i = inotify.adapters.InotifyTree(folderpath)

    for event in i.event_gen():
        print(event)







if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='folder activity trigger')

    parser.add_argument('-i', '--input', nargs='?', required=True,
                        help='Input folder to watch')

    args = parser.parse_args()

    folderwatch(args.input)
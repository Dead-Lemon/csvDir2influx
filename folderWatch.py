import minotaur
import argparse
import SingleRun

def folderwatch(inputfiles, config, hashstore, preprocess):

    with minotaur.Inotify() as n:
        n.add_watch('sample', minotaur.Mask.CLOSE_WRITE)
        try:
            for evt in n:
                #print(evt)
                SingleRun.runImport(inputfiles, config, hashstore, preprocess)
        except KeyboardInterrupt:
            print(' stopped')
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Folder watch for auto import of CSV files')

    parser.add_argument('-i', '--input', nargs='?', required=True,
                        help='Input folder to watch')

    parser.add_argument('-c', '--config', nargs='?', default='csv.json',
                        help='config file location')

    parser.add_argument('-s', '--hashstore', nargs='?', default='.hashstore',
                        help='hashed file store')

    parser.add_argument('-p', '--preprocess', nargs='?', default=False,
                        help='enable use of preprocessing script')

    args = parser.parse_args()

    folderwatch(args.input, args.config, args.hashstore, args.preprocess)


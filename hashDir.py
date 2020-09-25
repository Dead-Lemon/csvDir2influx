import argparse
import hashlib
import os

hasher = hashlib.sha1()

def checkDir(folderPath):
    for files in os.walk(folderpath)
        print(files)
        









if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='folder activity trigger')

    parser.add_argument('-i', '--input', nargs='?', required=True,
                        help='Input folder to watch')

    args = parser.parse_args()

    checkDir(args.input)
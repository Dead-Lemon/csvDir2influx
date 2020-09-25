import argparse
import hashlib
import os

hasher = hashlib.sha1()

def hashfile(filepath): #generates sha1 hash of inputted file
    with open(filepath, 'rb') as filetohash: #opens file in the list, ignoring sub directories
        buf = filetohash.read() #some hash magic --_0_--
        hasher.update(buf) 
        return(hasher.hexdigest())     


def getDirHash(folderPath): #generates hashes for all files in a directory
    hashlist = []
    
    for dirName, subdirList, fileList in os.walk(folderPath): #retrieves lists for files in folder
        for files in fileList:
            filepath = "/".join([folderPath,files])
            print(filepath) #recreating the full path so we can open the file
            hashedfile = hashfile(filepath)
            hashlist.append([hashedfile, filepath]) #add hash and file path to a list
    return hashlist
#    with open('.newhash','w+') as storehash: #creates/overrides file and stores hash list to disk
#        for data in hashlist:
#            storehash.write('%s\n' % data)
#            print(data)

def checkFileHash(newhash):
     if os.path.isfile('.oldhash') == False: #checks if file exists
        with open('.oldhash', 'w+') as f: #creates the file
             temp = ['','']
             f.write('%s\n' % temp) #initilize table


def getNewFiles(folderPath): #finds what files have changes and returns them in a list
    return checkFileHash(getDirHash(folderPath))








if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='folder activity trigger')

    parser.add_argument('-i', '--input', nargs='?', required=True,
                        help='Input folder to watch')

    args = parser.parse_args()

    getDirHash(args.input)
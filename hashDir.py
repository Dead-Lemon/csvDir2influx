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
            filepath = "/".join([folderPath,files]) #creates the full path of the file
            print(filepath) #recreating the full path so we can open the file
            hashedfile = hashfile(filepath) #get has of the selected file
            hashlist.append([hashedfile, filepath]) #add hash and file path to a list
    return hashlist

def storeHashList(hashlist, filename):
    with open(filename,'w+') as storehash: #creates/overrides file and stores hash list to disk
        for data in hashlist:
            storehash.write('%s\n' % data)
            print(data)

def checkFileHash(newhash, filename):
    if os.path.isfile(filename) == False: #checks if file exists
        with open(filename, 'w+') as f: #creates the file
            temp = ['','']
            f.write('%s\n' % temp) #initilize table
    with open(filename) as f:
        for line in f:
            line = line.strip()
            print(line)




def getNewFiles(folderPath, hashstore): #finds what files have changes and returns them in a list
    return checkFileHash(getDirHash(folderPath), hashstore)








if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='folder activity trigger')

    parser.add_argument('-i', '--input', nargs='?', required=True,
                        help='Input folder to watch')

    parser.add_argument('-s', '--store', nargs='?', default='.oldhash',
                        help='file name of hash store')

    args = parser.parse_args()

    getNewFiles(args.input, get.store)
import argparse
import hashlib
import os
import json

hasher = hashlib.sha1()

def hashfile(filepath): #generates sha1 hash of inputted file
    return hashlib.md5(open(filepath, 'rb').read()).hexdigest() 

def getDirHash(folderPath): #generates hashes for all files in a directory
    hashlist = []
    
    for dirName, subdirList, fileList in os.walk(folderPath): #retrieves lists for files in folder
        for files in fileList:
            filepath = "/".join([folderPath,files]) #creates the full path of the file
            #print(filepath) #recreating the full path so we can open the file
            hashedfile = hashfile(filepath) #get has of the selected file
            hashlist.append([hashedfile, filepath]) #add hash and file path to a list
    return hashlist

def storeHashList(hashlist, filename):
    with open(filename,'w+') as storehash: #creates/overrides file and stores hash list to disk
        json.dump(hashlist, storehash) #stores hashlist as a json file

def checkFileHash(newhash, filename):
    oldhash = []
    filefound = []
    if os.path.isfile(filename) == False: #checks if file exists
        with open(filename, 'w+') as f: #creates the file
            temp = ['','']
            json.dump(temp, f) #save blank template as json file

    with open(filename) as f: #opens saved hash file as f
        oldhash = json.load(f) #load json data from file
    
    found = False
    try: #try to see if there is usable data
        for i in newhash: #loops through all new hashes
            for j in oldhash: #each newhash is checked against all old hashes
                if (i[0] == j[0]): #hash vs hash
                    found = True 
            if found:
                found = False #reset found trigger
            else:
                filefound.append(i) #add entry of new hash with file path
    except: #exception assumes empty file and treats all hashes as new
        print('no historical hashes')
        filefound = newhash

    storeHashList(newhash, filename) #store newhash as oldhash
    return filefound

            
def getNewFiles(folderPath, hashstore): #finds what files have changes and returns them in a list
    newFileList = checkFileHash(getDirHash(folderPath), hashstore)
    #print(newFileList)
    return newFileList


if __name__ == "__main__": #arguments are used if this is run stand alone
    parser = argparse.ArgumentParser(description='New file finder')

    parser.add_argument('-i', '--input', nargs='?', required=True,
                        help='Input folder to watch')

    parser.add_argument('-s', '--store', nargs='?', default='.oldhash',
                        help='file name of hash store')

    args = parser.parse_args()

    getNewFiles(args.input, args.store)
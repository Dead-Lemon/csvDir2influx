import requests
import gzip
import argparse
import csv
import datetime
import json
from pytz import timezone

from influxdb import InfluxDBClient

epoch_naive = datetime.datetime.utcfromtimestamp(0)
epoch = timezone('UTC').localize(epoch_naive)

def unix_time_millis(dt):
    return int((dt - epoch).total_seconds() * 1000)


def testFloat(data):
    try:
        return(float(data))
    except:
        pass

def testInt(data):
    try:
        return(int(data))
    except:
        return()

def testBool(data):
    try:
        if data == 'True':
            return(True)
        elif data == 'False':
            return(False)
        else:
            return()
    except:
        return()

def loadCsv(inputfilename, config):

    client = InfluxDBClient(config['host'], config['port'], config['user'], config['password'], config['db'], ssl=testBool(config['ssl']))
    dbname = config['db']
    if(config['createdb'] == 'True'):
        print('Deleting database %s'%dbname)
        client.drop_database(dbname)
        print('Creating database %s'%dbname)
        client.create_database(dbname)

    client.switch_user(config['user'], config['password'])

    # open csv
    datapoints = []
    count = 0
    with open(inputfilename, 'r', errors="ignore") as csvfile: #errors=ignore drops special charactors not in UTF-8.
        
        reader = csv.DictReader(csvfile, delimiter=config['csv']['delimiter'])

        for row in reader:
            #print(row)
            
            datetime_naive = datetime.datetime.strptime(row[config['mapping']['time']['from']],config['mapping']['time']['format']) #strptime(2020/09/12 12:12:12, %Y/%m%d %H:%M:%S) converts time string to unix time based on set template
            #print(datetime_naive)

            if datetime_naive.tzinfo is None:
                datetime_local = timezone(config['tz']).localize(datetime_naive) #timezone offset converts back to UTC
            else:
                datetime_local = datetime_naive

            timestamp = unix_time_millis(datetime_local) * 1000000 # in nanoseconds
            if config['tags'] == 'True':
                for t in config['mapping']['tagSchema']:
                        if config['mapping']['tagSchema'][t]['from'] in row:
                            tags[t] = row[t]

            fields = {}

            for f in config['mapping']['fieldSchema']: #go through set field list

                fn = config['mapping']['fieldSchema'][f]['from'] #gets actual column field names to be found in csv
                ftype = config['mapping']['fieldSchema'][f]['type'] #gets the var type

                if fn in row: #loops though columns and save it under new headings
                    if ftype == 'float':
                        fields[f] = testFloat(row[fn])
                    elif ftype == 'int':
                        fields[f] = testInt(row[fn])
                    elif ftype[f] == 'bool':
                        fields[f] = testBool(row[fn])
                    else:    
                        fields[f] = str(row[fn])
                #print(fields)

            if config['tags'] == 'True':
                point = {"measurement": config['measurementName'], "time": timestamp, "fields": fields, "tags": tags}
            else:
                point = {"measurement": config['measurementName'], "time": timestamp, "fields": fields}

            datapoints.append(point)
            count+=1
            batchsize = int(config['batchSize'])
            if len(datapoints) % batchsize == 0:
                print('Read %d lines'%count)
                print('Inserting %d datapoints...'%(len(datapoints)))
                response = client.write_points(datapoints)

                if not response:
                    print('Problem inserting points, exiting...')
                    exit(1)

                print("Wrote %d points, up to %s, response: %s" % (len(datapoints), datetime_local, response))

                datapoints = []
            

    # write rest
    #print(datapoints)
    if len(datapoints) > 0:
        print('Read %d lines'%count)
        print('Inserting %d datapoints...'%(len(datapoints)))
        response = client.write_points(datapoints)

        if response == False:
            print('Problem inserting points, exiting...')
            exit(1)

        print("Wrote %d, response: %s" % (len(datapoints), response))

    print('Done')


def loadConfig(inputfilename, configfile): ## load config from file. allows passing json object to LoadCsv directly if using in an external script
    with open(configfile) as configdata:
        config = json.load(configdata)
    loadCsv(inputfilename, config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='csv to influxdb')

    parser.add_argument('-i', '--input', nargs='?', required=True,
                        help='Input folder to watch')

    parser.add_argument('-c', '--config', nargs='?', default='csv.json',
                        help='config file location')

    args = parser.parse_args()

    loadConfig(args.input, args.config)
    
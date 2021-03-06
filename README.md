# csvDir2influx
## Monitors folder for uploaded CSV files and sends to influx
Library is being modified to watch a folder for FTP uploaded CSV files.

* importCSVfolder - import csv file in a folder and watch for additions
* hashDir - returns a list of change files between runs
* csvToInfluxdb - import csv to influxdb
* preProcess - custom user functionality

## importCSVfolder Usage

* Usable in cron like usage, or just once off runs
* Able to set folder to monitor for changes

```
usage: importCSVfolder.py -i '/tmp/upload' --watch True --config '.csv.json' 
                                            --hashstore '.hashstore' -p True

  required
  -i [INPUT], --input [INPUT]
                        Path to folder to check                        
  optional
  -w [WATCH] --watch [WATCH]
                        watch set input folder for changes
                        Default = False                  
  -c [CONFIG] --config [CONFIG]
                        Store name for dirtory hashes
                        Default = csv.json

  -s [HASHSTORE] --hashstore [HASHSTORE]  
                        help='hashed file store'
                        default= .hashstore

  -p [PREPROCESS] --preprocess [PREPROCESS] default=False,
                        Enable use of preprocessing.py script
                        Very application specific at the moment
                        Default = False
```
```requires $pip install minotaur```

## hashDir Usage

```
usage: hashDir.py -i [INPUT] -s [STORE]
  required
  -i [INPUT], --input [INPUT]
                        Path to folder to check
  optional                      
  -s [STORE], --store [STORE]
                        Store name for dirtory hashes
                        Default = .oldhash

returns [HASH, FULL PATH OF FILE, FILE NAME]

```

## csvToInfluxdb Usage

```Require $pip install influxdb```

```
usage: csvToInfluxdb.py -i [INPUT] -c [CONFIG]
  required
  -i [INPUT], --input [INPUT]
                        Path to csv file 
  optional
  -c [CONFIG], --config [CONFIG]
                        path to config file
                        Default = csv.json
```
The following command will insert the file into a influxdb database:

```python csvToInfluxdb.py -i logs.csv -c csv.json```

## Example of json config file

```
{
    "host": "127.0.0.1",
    "port" : "8086",
    "db" : "csvlogs",
    "user" : "csv",
    "password" : "csv",
    "ssl" : "False",
    "createdb" : "True",
    "measurementName": "Site1",
    "tz" : "Etc/UCT",
    "tags" : "False",
    "batchSize" : "5000",
    "mapping": {
      "time": {
        "from": "Date & Time",
        "type": "timestamp",
        "format": "%Y/%m/%d %H:%M:%S"
      },
      "fieldSchema": {
        "AI00": {
          "from": "AI00 ()",
          "type": "float"
        },
        "AI01": {
          "from": "AI01 ()",
          "type": "float"
        },
      },
      "tagSchema": {
        "SIM1": {
          "from": "SIM1",
          "type": "*"
        }
      }
    },
    "csv": {
      "delimiter": ","
    }
  }

```

* fieldScheme create the list of field names to be used. 
* 'From' denotes the actual column name 
* 'type' denotes the expected variable type. float, int, bool, string 


## Raw Data Example

Csv Data system is being modeled around:
```
Date & Time,AI00 (),AI01 (),AI05 (�C),AI06 (v),CI00,CI06,CI07,CI08,
2020/09/14 00:00:00,0.056250,1.348250,20.809998,6.972709,1,2,0,0,
2020/09/14 00:01:00,0.056250,1.348250,20.809998,,1,,,,
2020/09/14 00:02:00,0.056250,1.348250,20.809998,,1,,,,
2020/09/14 00:03:00,0.056250,1.348250,20.809998,,1,,,,
2020/09/14 00:04:00,0.053750,1.348250,20.809998,,1,,,,
2020/09/14 00:05:00,0.056250,1.348250,20.809998,,1,,,,
2020/09/14 00:06:00,0.055000,1.348250,20.809998,,1,,,,
2020/09/14 00:07:00,0.056250,1.348250,20.809998,,1,,,,
2020/09/14 00:08:00,0.055000,1.348250,20.809998,,1,,,,
2020/09/14 00:09:00,0.055000,1.348250,20.809998,,1,,,,
2020/09/14 00:10:00,0.055000,1.348250,20.809998,,1,,,,
2020/09/14 00:11:00,0.055000,1.348250,20.809998,,1,,,,
2020/09/14 00:12:00,0.053750,1.348250,20.809998,,1,,,,
2020/09/14 00:13:00,0.055000,1.348250,20.809998,,1,,,,
2020/09/14 00:14:00,0.055000,1.348250,20.809998,,1,,,,
2020/09/14 00:15:00,0.053750,1.348250,20.809998,6.972709,1,2,0,0,
```

## PreProcess
user code to manipulate files lists and jsons file.
Allows automating some extra tasks

* Find deviceID from file name
* Update measurement name to DevID
* Remove files from file list, if set phrase is found

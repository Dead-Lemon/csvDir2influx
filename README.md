# csv-to-influxdb Extended
Library is being modified to watch a folder for FTP uploaded CSV files.

hashDir returns a list of change files between runs
folderWatch monitors a set folder and will call hashDir when a change is detected
csvToInfluxdb is configured by the csv.json file. Column names can me renamed

## hashDir Usage

```
usage: hashDir.py -i [INPUT] -s [STORE]

  -i [INPUT], --input [INPUT]
                        Path to folder to check
  -s [STORE], --store [STORE]
                        Store name for dirtory hashes
                        Default = .oldhash

returns [HASH, FULL PATH OF FILE, FILE NAME]

```


## csvToInfluxdb Usage

```
usage: hashDir.py -i [INPUT] -c [CONFIG]

  -i [INPUT], --input [INPUT]
                        Path to csv file
  
  optional

  -c [CONFIG], --config [CONFIG]
                        path to config file
                        Default = csv.json

returns [HASH, FULL PATH OF FILE, FILE NAME]

```

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

## Example

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

The following command will insert the file into a influxdb database:

```python csvToInfluxdb.py -i logs.csv -c csv.json```

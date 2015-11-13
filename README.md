DD-WRT Firmware Configuration Conversion Tool
=============================================

Description
-----------

This tool converts from a [DD-WRT firmware](http://www.dd-wrt.com) settings backup binary file to a JSON dictionary and vice versa. The format of the binary file from DD-WRT has been described [here](http://www.dd-wrt.com/phpBB2/viewtopic.php?t=33164).

You should be very cautious about restoring a backup binary file, you could brick your device! Of course, I am certainly not responsible for whatever damage you may cause by using this tool. Use at your own risk or do not use it!

Usage
-----
To convert a backup binary file to a JSON file:
```
#> python ddwrt-cfg-conv-tool.py bin2json nvrambak.bin > settings.json
```

To convert a JSON file to a backup binary file:
```
#> cat settings.json | python ddwrt-cfg-conv-tool.py json2bin nvrambak--custom.bin
```

Please have a look at the LICENSE file for more info on what is permitted to do with this code.


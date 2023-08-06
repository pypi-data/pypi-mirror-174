# Description

Interpret bytes through different customizable actions

# Installation

`pip install ntrprtr`

# Configuration

In order to interpet the given bytes, you need to provide a `.json` file
with the following structure:

```json
{
    "name": "ntrprtr example",
    "description": "This is a description within the result",
    // Specify as many ntrprtr objects as you want
    "ntrprtr": [
        {
            "name": "Enter the name here..",
            "description": "Provide description here..",
            "start": 0,  // The start byte from where you want to interpret
            "end": 10,   // The end byte where interpreting shall stop
            "action": [   
                        // --> Specify as many actions as you want
                        // --> Each action will be applied to the specified bytes
                        // --> You do not need to provide an action
                        // --> Output is a list of tuples (more information in example section)
                        // --> The actions are specified below
            ]
        }
    ]
}    
```

The following actions are available:

```json
// Get the decimal value of the given bytes.
// Specify if you want to interpret it as little or big endian
{
    "type": "decimal",
    "endianess": "little|big" // Default: little
}

// Apply endianess to given bytes
// Specify if you want to interpret it as little or big endian
{
    "type": "endianess",
    "endianess": "little|big" // Default: little
}

// Get the binary value of the given bytes.
// Specify if you want to interpret it as little or big endian
{
    "type": "binary",
    "endianess": "little|big" // Default: little
}

// Get the ascii representation of the given bytes.
// If a non ascii value is there, specify a placeholder
{
    "type": "ascii",
    "nonAsciiPlaceholder": "." // Default: .
}

// Get the unicode representation of the given bytes.
{
    "type": "unicode"
}

// Provides a hexdump for the given bytes
// If a non ascii value is there, specify a placeholder
{
    "type": "hexdump",
    "nonAsciiPlaceholder": "." // Default: .
}

// Compare the given bytes against your own values:
// Specify if you want to interpret it as little or big endian
// Specify a result if there is no match
{
    "type": "equals",
    "endianess": "little|big", // Default: big
    // Add as many objects as you want to the "cmp" list
    "cmp": [{
                // The value you want to compare with the given bytes
                "value": "1D1E", 
                // A description which will be added to the result, 
                // if the given bytes matches "value"         
                "description": "Compare 1"      
            },{
                "value": "1D1",
                "description": "Compare 2"
            }],
    // The result if there was no match 
    "noMatch": "No Match found!" // Default: No match found!
}

// Compare the bits of the given bytes against your own values
// Important: Provide leading zeros
// Specify if you want to interpret it as little or big endian
// Specify a result if there is no match
{
    "type": "bitequals",
    "endianess": "little|big", // Default: big
    // Add as many objects as you want to the "cmp" list
    "cmp": [{
                // The bits you want to compare
                "value": "01110111",
                // Description to be added to the result,
                // if bits machtes "value"
                "description": "Bits are equal"
            }],
    // The result if there was no match 
    "noMatch": "Bits are not equal!" // Default: No match found!
}

// Interprets 2 Bytes as DOS time - format hour:minute:seconds
// Specify if you want to interpret it as little or big endian
{
    "type": "dostime",
    "endianess": "little|big" // Default: little
}

// Interprets 4 Bytes as unix time - Convert it to UTC datetime
// Specify if you want to interpret it as little or big endian
{
    "type": "unixtime",
    "endianess": "little|big" // Default: little
}

// Interprets 2 Bytes as DOS date - format day.month.year
// Specify if you want to interpret it as little or big endian
{
    "type": "dosdate",
    "endianess": "little|big" // Default: little
}

// Interprets 8 Bytes as Win32 Epoch Time (01.01.1601)
// Specify if you want to interpret it as little or big endian
{
    "type": "win32time",
    "endianess": "little|big" // Default: little
}
```

# Options

`python -m ntrprtr --mode {config,interpret,testfile} [--amount AMOUNT] [--name NAME] [--target TARGET] [--config CONFIG] [--result RESULT] [--offset OFFSET] [--bytes BYTES]`

<hr>

**General**

| Option | Short | Type | Default | Description |
|---|---|---|---|---|
|--mode | -m | String | - | config = Create a configuration template <br> interpret = Overview of disk space usage <br> testfile = Create a binary testfile |

<hr>

**mode = config**

| Option | Short | Type | Default | Description |
|---|---|---|---|---|
|--amount | -a | Int | 1 | Create a config with the given number of objects |
|--name | -n | String | config.json | Name of the config file to be created |


<hr>

**mode = interpret**

| Option | Short | Type | Default | Description |
|---|---|---|---|---|
|--target | -t | String | - | Path to file which shall be interpreted |
|--config | -c | String | - | Path to config file |
|--result | -r | String | - | Path to result file |
|--offset | -o | Int | 0 | Offset in bytes to start reading |
|--bytes  | -b | Int | 0 | No. of bytes to read starting from offset |
|--disableHashing | -d | Bool | False | True if hashing shall be disabled <br> False otherwise|

<hr>

**mode = testfile**

| Option | Short | Type | Default | Description |
|---|---|---|---|---|
|--input | -i | String | "" | Path to textfile with hex values|
|--output | -u | String | "" | Path to binary test file to be created |


# Example

**Shell:**

```bash
# Create a config template
python -m ntrprtr -m config -a 10 -n ntrprtr-config.json
```

```bash
# Interprets example.dd with config.json
python -m ntrprtr -m interpret -t path/to/example.dd -c config.json
```

```bash
# Interprets example.dd with config.json and write it to result.txt
python -m ntrprtr -m interpret -t path/to/example.dd -c config.json -r result.txt
```

```bash
# Interprets example.dd starting at offset 42 with length of 10 bytes applying config.json
python -m ntrprtr -m interpret -t path/to/example.dd -c config.json -o 42 -b 10
```

```bash
# Interprets example.dd starting at offset 42 with length of 10 bytes applying config.json
# Disable Hashing for big files
python -m ntrprtr -m interpret -t path/to/example.dd -c config.json -o 42 -b 10 -d True
```

To create a binary testfile use a textfile with hex values as input:

```bash
# Max. 16 hex values per row within a .txt
# hexdata.txt
00 01 02 03 04 04 06 07 08 09 0A 0B 0C 0D 0E 0F 
68 61 6C 6C 6F 20 77 6F 72 6C 64 1B 1C 1D 1E 1F
43 B7 67 42 00 00 00 00 00 00 00 00 00 00 00 00
79 00 5F 00 30 00 31 00 2E 00 6A 00 D0 14 FE 52
00 72 25 8B EF EA D8 01
```

```bash
# Create hex.bin from hexdata.txt
python -m ntrprtr -m testfile -i path/to/hexdata.txt -u hex.bin
```

**Programmatically:**

Given bytes to interpret:

```
00 01 02 03 04 04 06 07 08 09 0A 0B 0C 0D 0E 0F 
68 61 6C 6C 6F 20 77 6F 72 6C 64 1B 1C 1D 1E 1F
43 B7 67 42 00 00 00 00 00 00 00 00 00 00 00 00
79 00 5F 00 30 00 31 00 2E 00 6A 00 D0 14 FE 52
00 72 25 8B EF EA D8 01
```

Use the following `config.json`:

```json
{
    "name": "ntrprtr example",
    "description": "This is a description within the result",
    "ntrprtr": [
        {
            "name": "first-byte-with-no-action",
            "description": "No action",
            "start": 0,
            "end": 2
        },
        {
            "name": "first-bytes",
            "description": "First three bytes",
            "start": 0,
            "end": 2,
            "action": [
                {
                    "type": "decimal",
                    "endianess": "little"
                }
            ]
        },
        {
            "name": "endian-bytes",
            "description": "Little Endian",
            "start": 0,
            "end": 2,
            "action": [
                {
                    "type": "endianess",
                    "endianess": "little"
                }
            ]
        },
        {
            "name": "bin-bytes",
            "description": "Binary bytes",
            "start": 2,
            "end": 3,
            "action": [
                {
                    "type": "binary",
                    "endianess": "little"
                }
            ]
        },
        {
            "name": "ascii-bytes",
            "description": "Ascii values",
            "start": 16,
            "end": 26,
            "action": [
                {
                    "type": "ascii",
                    "nonAsciiPlaceholder": "."
                }
            ]
        },
        {
            "name": "hexdump-bytes",
            "description": "Hexdump values",
            "start": 0,
            "end": 3,
            "action": [
                {
                    "type": "hexdump",
                    "nonAsciiPlaceholder": "."
                }
            ]
        },
        {
            "name": "equals-bytes",
            "description": "Test equals",
            "start": 29,
            "end": 30,
            "action": [
                {
                    "type": "equals",
                    "endianess": "big",
                    "cmp": [
                        {
                            "value": "1D1E",
                            "description": "Compare 1"
                        },
                        {
                            "value": "1D1",
                            "description": "Compare 2"
                        }
                    ],
                    "noMatch": "No Match found!"
                }
            ]
        },
        {
            "name": "bitEquals",
            "description": "Bit equality",
            "start": 22,
            "end": 22,
            "action": [
                {
                    "type": "binary",
                    "endianess": "big"
                },
                {
                    "type": "bitequals",
                    "endianess": "big",
                    "cmp": [
                        {
                            "value": "01110111",
                            "description": "Bits are equal!"
                        }
                    ],
                    "noMatch": "Bits are not equal!"
                }
            ]
        },
        {
            "name": "dos-time-bytes",
            "description": "DOS time bytes",
            "start": 32,
            "end": 33,
            "action": [
                {
                    "type": "dostime",
                    "endianess": "little"
                }
            ]
        },
        {
            "name": "unixtime-bytes",
            "description": "unix time bytes",
            "start": 60,
            "end": 63,
            "action": [
                {
                    "type": "unixtime",
                    "endianess": "little"
                }
            ]
        }
        {
            "name": "dos-date-bytes",
            "description": "DOS date bytes",
            "start": 34,
            "end": 35,
            "action": [
                {
                    "type": "dosdate",
                    "endianess": "little"
                }
            ]
        },
        {
            "name": "win32time",
            "description": "win32 time bytes",
            "start": 64,
            "end": 71,
            "action": [
                {
                    "type": "endianess",
                    "endianess": "little"
                },
                {
                    "type": "decimal",
                    "endianess": "little"
                },
                {
                    "type": "win32time",
                    "endianess": "little"
                }
            ]
        }
        {
            "name": "unicode-bytes",
            "description": "unicode repr.",
            "start": 48,
            "end": 59,
            "action": [
                {
                    "type": "unicode"
                }
            ]
        }
    ]
}
```

Use it programmatically:

```python
import json

from ntrprtr.ByteInterpreter import ByteInterpreter
from ntrprtr.printer.Printer import Printer

configPath = "config.json"
pathToFile = "example.dd" # Contains the above bytes


fileHandle = open(pathToFile, "rb")
testBytes = fileHandle.read()

configHandle = open(configPath, encoding="utf8")
config = json.load(configHandle)

b = ByteInterpreter(testBytes, config["ntrprtr"])
result = b.interpret()

# If you want a standard output use Printer
p = Printer()
p.print(result, config["name"], config["description"])
```

The result is a list of tuples:
```python
[
    #       Result: [0] = Name, [1] = Description, [2] = Start Byte, [3] = End Byte, [4] = Bytes, [5] = List(ActionResult)
    # ActionResult: [0] = Type, [1] = Result
    ('first-byte-with-no-action', 'No action', 0, 2, bytearray(b'\x00\x01\x02'), [('None', '-')])
    ('first-bytes', 'First three bytes', 0, 2, bytearray(b'\x00\x01\x02'), [('decimal', 258)]), 
    ('endianess-bytes', 'Little Endian', 0, 2, bytearray(b'\x00\x01\x02'), [('endianess', "02 01 00")]), 
    ('bin-bytes', 'Binary bytes', 2, 3, bytearray(b'\x02\x03'), [('binary', '0000 0011 0000 0010')]), 
    ('ascii-bytes', 'Ascii values', 16, 26, bytearray(b'hallo world'), [('ascii', 'hallo world')]), 
    ('hexdump-bytes', 'Hexdump values', 0, 3, bytearray(b'\x00\x01\x02\x03'), [('hexdump', 'see below')]), 
    ('equals-bytes', 'Test equals', 29, 30, bytearray(b'\x1d\x1e'), [('equals', 'Compare 1')]), 
    ('bitEquals', 'Bit equality', 22, 22, bytearray(b'w'), [('binary', '0111 0111'), ('bitequals', 'Bits are equal!')]), 
    ('unixtime-bytes', 'unix time bytes', 60, 63, bytearray(b'C\xd0\x14\xfe\x52'), [('unixtime', '14.02.14 13:06:24 UTC')]),
    ('win32time', 'win32 time bytes', 64, 71, bytearray(b'C\x00\x72\x25\x8B\xEF\xEA\xD8\x01'), [('win32time', '28.10.22 17:05:56 UTC')]),
    ('dos-time-bytes', 'DOS time bytes', 32, 33, bytearray(b'C\xb7'), [('dostime', '22:58:6')]), 
    ('dos-date-bytes', 'DOS date bytes', 34, 35, bytearray(b'gB'), [('dosdate', '7.3.2013')]), 
    ('unicode-bytes', 'unicode repr.', 48, 59, bytearray(b'y\x00_\x000\x001\x00.\x00j\x00'), [('unicode', 'y_01.j')])
]
```
The output from printer looks like the following:

```
###########################################################################################

ntrprtr by 5f0
Interpret bytes through different customizable actions

Current working directory: path/to/ntrprtr
        Investigated File: path/to/example.dd

                      MD5: 3f8555928a712492c23ca27fb142ebe2
                   SHA256: 715899b61bf6a6aa02adac9124db94e74ec4f7e837acb7ed7a361acd10045b63

          Offset in Bytes: 0

                 Datetime: 10/11/1970 10:11:12

###########################################################################################


ntrprtr example
---------------
This is a description within the result


Analysis
--------

--> No action
    --------------
      Start Byte: 0 (0x0)
        End Byte: 2 (0x2)
    Nr. of Bytes: 3
    --------------
     Bytes: 
            00 01 02
    --------------
    Action: 
            none
    Result: 
            -


--> No action
    --------------
      Start Byte: 0 (0x0)
        End Byte: 2 (0x2)
    Nr. of Bytes: 3
    --------------
     Bytes: 
            00 01 02
    --------------
    Action: 
            none
    Result: 
            -


--> First three bytes
    --------------
      Start Byte: 0 (0x0)
        End Byte: 2 (0x2)
    Nr. of Bytes: 3
    --------------
     Bytes: 
            00 01 02
    --------------
    Action: 
            decimal
    Result: 
            131328


--> Little Endian
    --------------
      Start Byte: 0 (0x0)
        End Byte: 2 (0x2)
    Nr. of Bytes: 3
    --------------
     Bytes: 
            00 01 02
    --------------
    Action: 
            endianess
    Result: 
            02 01 00


--> Binary bytes
    --------------
      Start Byte: 2 (0x2)
        End Byte: 3 (0x3)
    Nr. of Bytes: 2
    --------------
     Bytes: 
            02 03
    --------------
    Action: 
            binary
    Result: 
            0000 0011 0000 0010


--> Ascii values
    --------------
      Start Byte: 16 (0x10)
        End Byte: 26 (0x1a)
    Nr. of Bytes: 11
    --------------
     Bytes: 
            68 61 6C 6C 6F 20 77 6F 72 6C 64
    --------------
    Action: 
            ascii
    Result: 
            hallo world


--> Hexdump values
    --------------
      Start Byte: 0 (0x0)
        End Byte: 3 (0x3)
    Nr. of Bytes: 4
    --------------
     Bytes: 
            See below
    --------------
    Action: 
            hexdump
    Result: 

              Offset   00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F    ASCII           
            --------   -----------------------------------------------    ---------------- 
                   0   00 01 02 03                                        ....             
            


--> Test equals
    --------------
      Start Byte: 29 (0x1d)
        End Byte: 30 (0x1e)
    Nr. of Bytes: 2
    --------------
     Bytes: 
            1D 1E
    --------------
    Action: 
            equals
    Result: 
            Compare 1


--> Bit equality
    --------------
      Start Byte: 22 (0x16)
        End Byte: 22 (0x16)
    Nr. of Bytes: 1
    --------------
     Bytes: 
            77
    --------------
    Action: 
            binary
    Result: 
            0111 0111
    --------------
    Action: 
            bitequals
    Result: 
            Bits are equal!


--> DOS time bytes
    --------------
      Start Byte: 32 (0x20)
        End Byte: 33 (0x21)
    Nr. of Bytes: 2
    --------------
     Bytes: 
            43 B7
    --------------
    Action: 
            dostime
    Result: 
            22:58:6


--> DOS date bytes
    --------------
      Start Byte: 34 (0x22)
        End Byte: 35 (0x23)
    Nr. of Bytes: 2
    --------------
     Bytes: 
            67 42
    --------------
    Action: 
            dosdate
    Result: 
            7.3.2013
    --------------
    Action: 
            dostime
    Result: 
            8:19:14


--> unicode repr.
    --------------
      Start Byte: 48 (0x30)
        End Byte: 59 (0x3b)
    Nr. of Bytes: 12
    --------------
     Bytes: 
            79 00 5F 00 30 00 31 00 2E 00 6A 00
    --------------
    Action: 
            unicode
    Result: 
            y_01.j


--> unix time bytes
    --------------
      Start Byte: 60 (0x3c)
        End Byte: 63 (0x3f)
    Nr. of Bytes: 4
    --------------
     Bytes: 
            D0 14 FE 52
    --------------
    Action: 
            unixtime
    Result: 
            14.02.14 13:06:24 UTC

--> win32 time bytes
    --------------
      Start Byte: 64 (0x40)
        End Byte: 71 (0x47)
    Nr. of Bytes: 8
    --------------
     Bytes: 
            00 72 25 8B EF EA D8 01
    --------------
    Action: 
            win32time
    Result: 
            28.10.22 17:05:56 UTC

###########################################################################################

Execution Time: 0.000976 sec
```

# License

MIT
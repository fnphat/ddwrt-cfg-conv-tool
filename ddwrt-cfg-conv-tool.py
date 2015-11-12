#!/usr/bin/env python
"""
Copyright (c) 2015 Frederic N. Therrien

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json as _json
import sys as _sys
import collections as _collections
import argparse as _argparse
import StringIO as _stringio
import struct as _struct


VERSION = '0.1'
URL = 'https://github.com/fnphat/ddwrt-cfg-conv-tool'

HEADER = 'DD-WRT'


def decode_ddwrt_bin(bin_data):
    """
    Decodes a DD-WRT firmware backup binary data string
    Returns a dictionary of NVRAM parameters
    """
    f = _stringio.StringIO(bin_data)
    # Get the file header and number or records
    id, number_of_records = _struct.unpack(str(len(HEADER))+ 'sH', f.read(len(HEADER)+2))
    if id == HEADER:
        data = {}
        # For each parameter
        for i in range(number_of_records):
            # Key string size contained in a byte
            key_size, = _struct.unpack('B', f.read(1))
            # Get the key
            key, = _struct.unpack(str(key_size)+ 's', f.read(key_size))
            # Value string size contained in two bytes
            value_size, = _struct.unpack('H', f.read(2))
            # Get the value
            value, = _struct.unpack(str(value_size)+ 's', f.read(value_size))
            data[key] = value
        return data
    else:
        raise Exception("Error! Data does not seems to be a DD-WRT backup.")


def encode_ddwrt_bin(data_dict):
    """
    Encodes a dictionary of NVRAM parameters
    Returns a DD-WRT firmware backup binary data string
    """
    # Put the file header
    bin_data = _struct.pack(str(len(HEADER))+ 'sH', HEADER, len(data_dict))
    for k, v in data_dict.items():
        k = str(k)
        k_size = len(k)
        bin_data += _struct.pack('B' +str(k_size)+ 's', k_size, k)
        v = str(v)
        v_size = len(v)
        bin_data += _struct.pack('H' +str(v_size)+ 's', v_size, v)
    return bin_data


def bin2json_cmd(args):
    with open(args.in_file, 'rb') as f:
        data_dict = decode_ddwrt_bin(f.read())
    # Output as JSON string, sorting the keys alphabetically
    print _json.dumps( _collections.OrderedDict(sorted(data_dict.items(), key=lambda t: t[0].lower())), indent=4 )   


def json2bin_cmd(args):
    data = _sys.stdin.read()
    data_dict = _json.loads('\n'.join([x for x in data.splitlines() if not x.startswith('#')]))
    with open(args.out_file, 'wb') as f:
        f.write(encode_ddwrt_bin(_collections.OrderedDict(sorted(data_dict.items(), key=lambda t: t[0].lower()))))


def main(arguments=None):
    parser = _argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version="Version " +VERSION+ " - " +URL)
    subparsers = parser.add_subparsers(help='Conversion tool for DD-WRT firmware configuration backups.')

    parser_bin2json = subparsers.add_parser('bin2json', help='Converts a DD-WRT firmware backup binary file to a JSON dict containing all the NVRAM parameters (stdout).')
    parser_bin2json.add_argument('in_file', help="DD-WRT backup binary input file.")
    parser_bin2json.set_defaults(func=bin2json_cmd)

    parser_json2bin = subparsers.add_parser('json2bin', help='Converts a JSON dict containing all the NVRAM parameters (stdin) to a DD-WRT firmware backup binary file.')
    parser_json2bin.add_argument('out_file', help="DD-WRT backup binary output file.")
    parser_json2bin.set_defaults(func=json2bin_cmd)

    args = parser.parse_args(arguments)
    args.func(args)

        
if __name__ == "__main__":
    main()
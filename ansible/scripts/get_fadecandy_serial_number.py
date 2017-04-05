#!/usr/bin/env python3
# coding: utf-8


from io import StringIO

with open('/var/log/syslog') as logf:
    log = tuple(l for l in logf.read().splitlines() if 'usb' in l)

    last_loading_index = max(i for i,e in enumerate(log) if 'Fadecandy'  in e)
    s_num = next(l for l in log[last_loading_index:] if 'SerialNumber' in l).rpartition(' ')[2]       
print(s_num)


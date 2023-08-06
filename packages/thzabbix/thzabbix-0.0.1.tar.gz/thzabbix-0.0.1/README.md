# thzabbix

Library for work with zabbix api.

Support Zabbix 6.0.x

Contains two classes - ZabbReq and HTTPtest. First do different kind of tasks in Zabbix api, second has target only Zabbix web tests.

1. [ZabbReq](zabbreq)
2. [HTTPtest](httptest)

### ZabbReq

`ZabbReq.req_post(req_data)` - simpliest function for send requests to zabbix server, where `req_data` is dictionary in zabbix api format. All information about it you can find in api documentation.

For example, print list of host' interfaces list data:

```
from thzabbix import ZabbReq

host_ip = "XXX.XXX.XXX.XXX"
zabb_user = "apiuser"
passwd = "secret"
url = "https://zabbix.example.com/api_jsonrpc.php"

zabb_creds = dict(user=zabb_user, passwd=zabb_passwd, url=zabb_url)
ZabbReq = ZabbReq(zabb_creds)

print(ZabbReq.req_post(dict(params=dict(filter=dict(ip=host_ip)), method="hostinterface.get"))["result"])
```

`ZabbReq.hostidbyip(host_ip)` - get host id by external interface ip address. `host_ip` is string variable

`ZabbReq.hostipbyid(host_id)` - get external interface ip address by host id. `host_id` is string variable

`ZabbReq.host_tmplt_list(host_id)` - get templates list (as template id), linked to host id. `host_id` is string variable

`ZabbReq.host_tmplt_upd(hostid, tmplt_lst)` - update templates (as template id), linked to host id. `host_id` is string variable, `tmplt_lst` is list of templates id.

`ZabbReq.host_tmplt_add(hostid, tmplt_id)` - get template ids list, linked to host id. `host_id` is string variable, `tmplt_id` is string variable, template id.

`ZabbReq.addhost(hcreatedata)` - create host. `hcreatedata` is dict of parameters for new host. 

For example:

```
from thzabbix import ZabbReq

zabb_user = "apiuser" # zabbix username, string
passwd = "secret" # zabbix user password, string
url = "https://zabbix.example.com/api_jsonrpc.php" # url of zabbix api

zabb_creds = dict(user=zabb_user, passwd=zabb_passwd, url=zabb_url)
ZabbReq = ZabbReq(zabb_creds)

hostname = "Example host"
tls_accept =  "2" # enable tls (for disable set this variable and tls_connect to "1")
tls_connect = "2" # set psk encription
tls_psk_identity = PSK KEY NAME
tls_psk = 123124324rwefdsfgdfsgsdfg546t42 #some psk key
host_ip = "XXX.XXX.XXX.XXX"

group_id = XXXXXX # group id for host
template_id = YYYYYY # template id linked to host

# groups and templates can be set as list of dictionary to add hosr in many groups or/and lynk many templates 

hostcreate = dict(host=hostname, 
    tls_connect=tlsconnect, 
    tls_accept=tlsaccept, 
    tls_psk_identity=psk_identity, 
    tls_psk=psk_key, 
    interfaces=[dict(type=1, main=1, useip=1, ip=host_ip, dns="", port=host_port)], 
    groups=[dict(groupid=group_id)], 
    templates=[dict(templateid=template_id)])
```

`ZabbReq.hostslist()` - print host list with extended data. 

`ZabbReq.hostsidlist()` - print host id list. 

### HTTPtest

`HTTPtest.httptestdel(del_testid)` - delete test by id

`HTTPtest.httptestadd(add_params)` - add new http test

For example:

```
from thzabbix import ZabbReq

zabb_user = "apiuser" # zabbix username, string
passwd = "secret" # zabbix user password, string
url = "https://zabbix.example.com/api_jsonrpc.php" # url of zabbix api

zabb_creds = dict(user=zabb_user, passwd=zabb_passwd, url=zabb_url)
HTTPtest = HTTPtest(zabb_creds)

host_ip = "XXX.XXX.XXX.XXX" # host ip in zabbix
test_dom = "example.com" # name of http test
test_dom = "example.com" # name of http test
steps_list = list(dict(name="example.com", url="https://example.com/", status_codes="200", no=1)) # data for one step check with default parameters

print(HTTPtest.httptestadd(dict(host_ip=test_host, name=test_dom, steps=steps_list))
```

`HTTPtest.httptestupd(upd_params)` - update existence http test. `upd_params` is similar to `add_params` in `HTTPtest.httptestadd()`

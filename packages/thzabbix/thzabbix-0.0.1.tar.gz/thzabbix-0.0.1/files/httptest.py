import json
import requests

from .functions import ZabbReq


class HTTPtest(object):
    def __init__(self, creds):
        self.authdata = dict(jsonrpc="2.0", method="user.login", params=dict(user=creds["user"], password=creds["passwd"]), id="1")
        self.headers = {'content-type': 'application/json-rpc'}
        self.url = creds["url"]
        self.authtock = requests.post(self.url, data=json.dumps(self.authdata), headers=self.headers).json()["result"]
        self.basedata = dict(jsonrpc="2.0", auth=self.authtock, id=1)
        self.delay = str("3m")
        self.timeout = str("30s")
        self.retr = 3
        self.follow_redirects = 0
        self.zabb_req = ZabbReq(creds)

    def _addparam(self, add_params):
        if not add_params.get("delay"):
            add_params["delay"] = self.delay
        for step in add_params["steps"]:
            if not step.get("follow_redirects"):
                step["follow_redirects"] = self.follow_redirects
            if not step.get("timeout"):
                step["timeout"] = self.timeout
        return add_params

    def _httptest_addlist(self, add_params):
        add_params = self._addparam(add_params)
        steps_dict = dict(name=add_params["name"], url=add_params.pop("url"), follow_redirects=add_params.pop("follow_redirects"), timeout=add_params.pop("timeout"), status_codes=add_params.pop("status_codes"), no=str("1"))
        steps_list = list()
        steps_list.append(steps_dict)
        add_params["hostid"] = self.zabb_req.hostidbyip(add_params.pop("host_ip"))
        add_params["steps"] = steps_list
        return add_params

    def _httptest_updlist(self, upd_params):
        upd_params = self._addparam(upd_params)
        full_params = dict(httptestid=upd_params.pop("httptestid"), delay=upd_params.pop("delay"))
        steps_dict = upd_params
        steps_dict["no"] = str("1")
        steps_list = list()
        steps_list.append(steps_dict)
        full_params["steps"] = steps_list
        full_params["retries"] = self.retr
        return full_params

    def _trigg_add(self, name, host):
        trigg_descr = str("Web scenario " + name + " failed: {ITEM.VALUE}")
        trigg_expr = str("length(last(/" + host + "/web.test.error[" + name + "]))>0 and last(/" + host + "/web.test.fail[" + name + "])>0")
        paramslst = dict(description=trigg_descr, expression=trigg_expr, priority=4)
        full_data = self.basedata.copy()
        full_data["params"] = paramslst
        full_data["method"] = "trigger.create"
        return self.zabb_req.req_post(full_data)

    def _httptestfull(self, params, method):
        check_name = params["name"]
        params = self._addparam(params)
        result = list()
        if method == "httptest.create":
            host_id = self.zabb_req.hostidbyip(params["host_ip"])
            hostname = self.zabb_req.hostget(dict(hostid=host_id))["name"]
            triggadd_ret = self._trigg_add(check_name, hostname).json()
            del params["host_ip"]
            params["hostid"] = host_id
            result.append(triggadd_ret)
        if method != "httptest.create" and method != "httptest.update":
            return False
        test_add_data = self.basedata.copy()
        test_add_data["params"] = params
        test_add_data["method"] = method
        httptestret = self.zabb_req.req_post(test_add_data).json()
        result.append(httptestret)
        return result

    def httptestdel(self, del_testid):
        paramslst = dict(httptestid=del_testid)
        full_data = self.basedata.copy()
        full_data["params"] = paramslst
        full_data["method"] = "httptest.delete"
        del_data = self.zabb_req.req_post(full_data)
        return del_data

    def httptestadd(self, add_params):
        method = "httptest.create"
        return self._httptestfull(add_params, method)

    def httptestupd(self, upd_params):
        method = "httptest.update"
        return self._httptestfull(upd_params, method)

import os
import sys
import getopt
import requests
import time
import subprocess
import datetime
import json
import re
from urllib import parse


class GitLabTools():
    ''' download aritfact and create tag by gitlab api'''
    def __init__(self):
        self.gitlab_domain = "git.iwellmass.com"
        self.token = "TM99wdzKSsZQJjPAL687"
        self.projects = ""
        self.branch = ""
        self.jobs_id_list = []
        self.download = False
        self.createtag = ""
        self.meassge  = ""
        self.truncatetag = ""
        self.mergerequest = {}
        self.updaterequest = {"state_event": "close", "tbranch": "", "title": ""}
        self.time = datetime.datetime.now().strftime(r"%Y%m%d%H")
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hp:b:j:dc:t::m:-r:-u:", ["help", "project=", "branch=", "job=", "download", "createtag=", "truncatetag=", "meassge=", "requestmerge=", "updatemerge"])
        except getopt.GetoptError:
            self.usage()
            sys.exit()
        for opt, value in opts:
            if opt in ("-h", "--help"):
                self.usage()
                sys.exit()
            elif opt in ("-p", "--project"):
                self.projects = list(filter(None, value.split(",")))
            elif opt in ("-b", "--branch"):
                self.branch = value
            elif opt in ("-j", "--job"):
                self.jobs_id_list = list(filter(None, value.split(",")))
            elif opt in ("-m", "--meassge"):
                # self.meassge = re.sub(r"\s+","%20", value)
                self.meassge = value
            elif opt in ("-d", "--download"):
                self.download = True
            elif opt in ("-c", "--createtag"):
                self.createtag = value
            elif opt in ("-t", "--truncatetag"):
                self.truncatetag = value
            elif opt in ("-r", "--requestmerge"):
                merge_request = parse.parse_qs(value)
                print(merge_request)
                if not merge_request.get("sb") or not merge_request.get("tb") or not merge_request.get("tt"):
                    self.usage()
                    raise Exception("merge requests miss args")
                self.mergerequest["sbranch"] = merge_request["sb"][0]
                self.mergerequest["tbranch"] = merge_request["tb"][0]
                self.mergerequest["title"] = merge_request["tt"][0]
            elif opt in ("-u", "--updatemerge"):
                update_request = parse.parse_qs(value)
                if not update_request.get("iid"):
                    self.usage()
                    raise Exception("update merge miss iid")
                self.updaterequest["iid"] = update_request["iid"][0]
                if update_request.get("state_event"):
                    self.updaterequest["state_event"] = update_request["state_event"][0]
                if update_request.get("title"):
                    self.updaterequest["title"] = update_request["title"][0]
                if update_request.get("target_branch"):
                    self.updaterequest["tbranch"] = update_request["target_branch"][0]
        if not sys.argv[1:]:
            self.usage()
            sys.exit()
        if not self.download and not self.createtag and not self.truncatetag and not self.mergerequest and not self.updaterequest:
            self.usage()
            raise Exception("operate nedd  -d or -c or -t or -r -u")
        if not self.projects:
            self.usage()
            raise Exception("miss project name ")
        if self.createtag and not self.branch and not self.jobs_id_list:
            self.usage()
            raise Exception("create tag need job_id or branch")
        if self.branch and self.jobs_id_list:
            self.usage()
            raise Exception("job and branch cant concurrence")
        self.projects_id_list = self.get_project()

    def usage(self):
        print('''  Usage: python ./gitlabtools.py  [options]
        options:
            -h, --help               show this help
            -p, --project            assign project, example: -p base,wac-html
            -b, --branch             assign branch, example: -b test
            -j, --job                assign job, example: -j 20849,20848
            -d, --download           open download artifact
            -c, --createtag          assign create tag, example: -c v2020060722
            -t, --truncatetag        assign truncate tag, example: -t v2020060722
            -m, --meassge            assign git commit tag message, example: -m "tag meassge"
            -r, --requestmerge       push and accept MR, example: -r "sb=lzf&tb=master&tt=testmerge"
            -u, --updatemerge        update MR by merge_iid, example: -u "iid=5&state_event=close&title=test&target_branch=master"
        ''')

    def get_project(self):
        projects_id_list = []
        contents = json.load(open("project.json"))
        if self.projects[0] == "all" or self.projects[0] == "ALL":
            for project in contents:
                projects_id_list.append(project["id"])
        elif self.projects[0] != "all" or self.projects[0] != "ALL":
            for send_project in self.projects:
                sign = False
                for project in contents:
                    if project["name"] == send_project:
                        projects_id_list.append(project["id"])
                        sign = True
                if not sign:
                    raise Exception("project name[%s] not find in project.json " % send_project)
        return projects_id_list

    def remove_dicemp(self, dics):
        for k in list(dics.keys()):
            if not dics[k]:
                del dics[k]
        return dics

    def get_file_name(self, url, headers):
        filename = ''
        if 'Content-Disposition' in headers and headers['Content-Disposition']:
            disposition_split = headers['Content-Disposition'].split(';')
            if len(disposition_split) > 1:
                if disposition_split[1].strip().lower().startswith('filename='):
                    file_name = disposition_split[1].split('=')
                    if len(file_name) > 1:
                        filename = parse.unquote(file_name[1])
        if not filename and os.path.basename(url):
            filename = os.path.basename(url).split("?")[0]
        if not filename:
            return time.time()
        return filename.strip('"')

    def download_by_requests(self):
        header = {"PRIVATE-TOKEN": self.token}
        info = {"gitlab_domain": self.gitlab_domain, "project_id": 40, "branch": "test", "job_re": "bjtest_build"}
        url = r"http://{gitlab_domain}/api/v4/projects/{project_id}/jobs/artifacts/{branch}/download?job={job_re}".format(**info)
        print("url:", url)
        down_res = requests.get(url=url, headers=header)
        content_length = (down_res.headers['Content-Length'])
        file_name = self.get_file_name(url, down_res.headers)
        print("文件大小：", content_length, "文件名称：" + file_name)
        with open(file_name, 'wb') as f:
            for chunk in down_res.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    def download_by_shell(self):
        if self.branch == "test":
            job_re = "bjtest_build"
        elif self.branch == "dev":
            job_re = "dev_build"
        elif self.branch == "":
            job_re = ""
        else:
            raise Exception("branch only support dev or test ")
        dir = self.time
        if not os.path.exists(dir):
            os.mkdir(dir)
        os.chdir(dir)

        if self.projects_id_list and self.branch:
            # download artifact by branch
            for project in self.projects_id_list:
                info = {"gitlab_domain": self.gitlab_domain, "project_id": project, "branch": self.branch, "job_re": job_re}
                url = r"http://{gitlab_domain}/api/v4/projects/{project_id}/jobs/artifacts/{branch}/download?job={job_re}".format(**info)
                cmd = r'curl -OJ --header "PRIVATE-TOKEN: {}"  "{}"'.format(self.token, url)
                subprocess.call(cmd, shell=True)
        elif self.projects_id_list and self.jobs_id_list and len(self.projects_id_list) == len(self.jobs_id_list):
            # download artifact by jobs_id
            for i, project in enumerate(self.projects_id_list):
                info = {"gitlab_domain": self.gitlab_domain, "project_id": project, "job_id": self.jobs_id_list[i]}
                url = r"http://{gitlab_domain}/api/v4/projects/{project_id}/jobs/{job_id}/artifacts".format(**info)
                cmd = r'curl -OJ --header "PRIVATE-TOKEN: {}"  "{}"'.format(self.token, url)
                subprocess.call(cmd, shell=True)
        else:
            raise Exception("download exception")

    def doshell(self, cmd, info=None):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate()
        if output:
            output = json.loads(output.decode("utf-8"))
            if output.get("message"):
                r_message = "".join(output["message"])
                print("{}, message: {}".format(info, r_message))
            elif output.get("state"):
                state = str(output["state"])
                iid = str(output["iid"])
                print("{}, state: {}, iid: {}".format(info, state, iid))
            else:
                print(output)
            return output
        else:
            print(info + "success")

    def create_tag(self):
        if self.branch:
            url_params = {"tag_name": self.createtag, "ref": self.branch, "message": self.meassge}
            for project in self.projects_id_list:
                info = {"gitlab_domain": self.gitlab_domain, "project_id": project, "params": parse.urlencode(url_params)}
                url = r"http://{gitlab_domain}/api/v4/projects/{project_id}/repository/tags?{params}".format(**info)
                cmd = r'curl --request POST --header "PRIVATE-TOKEN: {}" "{}"'.format(self.token, url)
                self.doshell(cmd, "create tag[%s] " % url_params["tag_name"])
        elif self.jobs_id_list:
            for i, project in enumerate(self.projects_id_list):
                info = {"gitlab_domain": self.gitlab_domain, "token": self.token, "project_id": project, "job_id": self.jobs_id_list[i]}
                cmd1 = r'curl --header "PRIVATE-TOKEN: {token}" "http://{gitlab_domain}/api/v4/projects/{project_id}/jobs/{job_id}"'.format(**info)
                result = self.doshell(cmd1)
                if result:
                    commit_sha = result["commit"]["short_id"]
                    url_params = {"tag_name": self.createtag, "ref": commit_sha, "message": self.meassge}
                    info["params"] =  parse.urlencode(url_params)
                    cmd2 = r'curl --request POST --header "PRIVATE-TOKEN: {token}" "http://{gitlab_domain}/api/v4/projects/{project_id}/repository/tags?{params}"'.format(**info)
                    self.doshell(cmd2, "create tag[%s] " % url_params["tag_name"])
                else:
                    print("%s create tag is interrupted,because pre_cmd is faild" % project)

    def delete_tag(self):
        for project in self.projects_id_list:
            info = {"gitlab_domain": self.gitlab_domain, "token": self.token, "project_id": project, "tag_name": self.truncatetag}
            cmd = r'curl --request DELETE --header "PRIVATE-TOKEN: {token}" "http://{gitlab_domain}/api/v4/projects/{project_id}/repository/tags/{tag_name}"'.format(**info)
            self.doshell(cmd, "delete tag[%s] " % info["tag_name"])

    def request_merge(self):
        url_params = {"source_branch": self.mergerequest["sbranch"], "target_branch": self.mergerequest["tbranch"], "title": self.mergerequest["title"]}
        for i, project  in enumerate(self.projects_id_list):
            info = {"token": self.token, "gitlab_domain": self.gitlab_domain, "project_id": project, "params": parse.urlencode(url_params)}
            cmd1 = r'curl --request POST  --header "PRIVATE-TOKEN: {token}" "http://{gitlab_domain}/api/v4/projects/{project_id}/merge_requests?{params}"'.format(**info)
            result = self.doshell(cmd1, "merge request[%s] " % url_params["title"])
            if result and result.get("iid"):
                info["iid"] = result["iid"]
                time.sleep(5)
                cmd2 = r'curl --request PUT  --header "PRIVATE-TOKEN: {token}" "http://{gitlab_domain}/api/v4/projects/{project_id}/merge_requests/{iid}/merge"'.format(**info)
                self.doshell(cmd2, "merge accept merge request[%s] " % url_params["title"])
            else:
                print("%s merge request is interrupted,iid not found,because pre_cmd is faild" % self.projects[i])

    def update_merge(self):
        url_params = {"state_event": self.updaterequest["state_event"], "target_branch": self.updaterequest["tbranch"], "title": self.updaterequest["title"]}
        url_params = self.remove_dicemp(url_params)
        for project  in self.projects_id_list:
            info = {"token": self.token, "gitlab_domain": self.gitlab_domain, "project_id": project, "iid": self.updaterequest["iid"], "params": parse.urlencode(url_params)}
            cmd = r'curl --request PUT  --header "PRIVATE-TOKEN: {token}" "http://{gitlab_domain}/api/v4/projects/{project_id}/merge_requests/{iid}?{params}"'.format(**info)
            self.doshell(cmd, "update merge request[%s] " % info["iid"])


if __name__ == "__main__":
    gitlab = GitLabTools()
    if gitlab.download:
        gitlab.download_by_shell()
    if gitlab.createtag:
        gitlab.create_tag()
    if gitlab.truncatetag:
        gitlab.delete_tag()
    if gitlab.mergerequest:
        gitlab.request_merge()
    if gitlab.updaterequest:
        gitlab.update_merge()

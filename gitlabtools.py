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
        self.time = datetime.datetime.now().strftime(r"%Y%m%d%H")
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hp:b:j:dc:t::m:", ["help", "project=", "branch=", "job=", "download", "createtag=", "truncatetag=", "meassge="])
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
                self.meassge = re.sub(r"\s+","%20", value)
            elif opt in ("-d", "--download"):
                self.download = True
            elif opt in ("-c", "--createtag"):
                self.createtag = value
            elif opt in ("-t", "--truncatetag"):
                self.truncatetag = value
        if not sys.argv[1:]:
            self.usage()
            sys.exit()
        if not self.download and not self.createtag and not self.truncatetag:
            raise Exception("operate nedd  -d or -c or -t")
        if self.createtag and not self.branch and not self.jobs_id_list:
            raise Exception("create tag need job_id or branch")
        if self.branch and self.jobs_id_list:
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

    def create_tag(self):
        if self.branch:
            for project in self.projects_id_list:
                url_params = {"tag_name": self.createtag, "ref": self.branch, "message": self.meassge}
                info = {"gitlab_domain": self.gitlab_domain, "project_id": project, "params": parse.urlencode(url_params)}
                url = r"http://{gitlab_domain}/api/v4/projects/{project_id}/repository/tags?{params}".format(**info)
                cmd = r'curl --request POST --header "PRIVATE-TOKEN: {}" "{}"'.format(self.token, url)
                self.doshell(cmd, "create tag[%s] " % url_params["tag_name"])


        elif self.jobs_id_list:
            for i, project in enumerate(self.projects_id_list):
                info = {"gitlab_domain": self.gitlab_domain, "token": self.token, "project_id": project, "job_id": self.jobs_id_list[i]}
                cmd1 = r'curl --header "PRIVATE-TOKEN: {token}" "http://{gitlab_domain}/api/v4/projects/{project_id}/jobs/{job_id}"'.format(**info)
                output = self.doshell(cmd1)
                commit_sha = output["commit"]["short_id"]
                url_params = {"tag_name": self.createtag, "ref": commit_sha,"branch": self.branch, "message": self.meassge}
                info["params"] =  parse.urlencode(url_params)
                cmd2 = r'curl --request POST --header "PRIVATE-TOKEN: {token}" "http://{gitlab_domain}/api/v4/projects/{project_id}/repository/tags?{params}"'.format(**info)
                self.doshell(cmd2, "create tag[%s] " % url_params["tag_name"])

    def delete_tag(self):
        for project in self.projects_id_list:
            info = {"gitlab_domain": self.gitlab_domain, "token": self.token, "project_id": project, "tag_name": self.truncatetag}
            cmd = r'curl --request DELETE --header "PRIVATE-TOKEN: {token}" "http://{gitlab_domain}/api/v4/projects/{project_id}/repository/tags/{tag_name}"'.format(**info)
            self.doshell(cmd, "delete tag[%s] " % info["tag_name"])

    def doshell(self, cmd, info=None):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate()
        if output:
            output = json.loads(output.decode("utf-8"))
            if output.get("message"):
                r_message = re.sub(r"\s+", "%20", output["message"]).strip("'")
                if r_message != self.meassge:
                    print(info + " error,message:" + output["message"])
                else:
                    print(info + " success,message: "+ output["message"])
        # elif err:
        #     err = json.loads(output.decode("utf-8"))


        else:
            print(info + " success")
        return output


if __name__ == "__main__":
    gitlab = GitLabTools()
    if gitlab.download:
        gitlab.download_by_shell()
    if gitlab.createtag:
        gitlab.create_tag()
    if gitlab.truncatetag:
        gitlab.delete_tag()

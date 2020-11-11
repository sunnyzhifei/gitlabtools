from flask import Flask, redirect, url_for, request, render_template,make_response, jsonify, Response
from gitlabtools import GitLabTools,logger
import os
from time import sleep
import json
from flask_cors import CORS
# from wsgiref.simple_server import make_server

app = Flask(__name__, template_folder='build', static_folder='build/static')
CORS(app)

dirname, filename = os.path.split(os.path.abspath(__file__))

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/api/gitlab',methods = ['POST', 'GET'])
def gitlab():
   if request.method == 'POST':
        result = json.loads(request.data.decode("utf-8"))
        try:
            type = result.get("type")
            if type == "uniquebranch":
                project = result.get("project")
                projects_list = []
                for p in project:
                    project_url = p.get("value").replace("/","%2F")
                    projects_list.append(project_url)
                branch = result.get("branch")
                download = result.get("artifact")
                createTagName = result.get("tagName")
                createTagMessage = result.get("tagMessage")
                mergeTargetBranch = result.get("targetBranch")
                mergeMessage = result.get("mergeMessage")
                createBranchName = result.get("createBranchName")
                piplineEnvironment = result.get("pipline")
                pipline_data = json.dumps({"ref":branch, "variables":[{"key":"env","value":piplineEnvironment}]})
                
                gitlab = GitLabTools()
                gitlab.projects_id_list = projects_list
                gitlab.projects = projects_list
                gitlab.branch = branch
                gitlab.download = download
                gitlab.createtag = createTagName
                gitlab.meassge = createTagMessage
                gitlab.mergerequest["sbranch"] = branch
                gitlab.mergerequest["tbranch"] = mergeTargetBranch
                gitlab.mergerequest["title"] = mergeMessage
                gitlab.pipline_data = pipline_data
                gitlab.createBranchName = createBranchName

                if download:
                    gitlab.download_by_shell()
                if createTagName:
                    gitlab.create_tag()
                if mergeTargetBranch:
                    gitlab.request_merge()
                if piplineEnvironment:
                    gitlab.create_pipline()
                if createBranchName:
                    gitlab.create_branch()

            elif type == "mutibranch":
                project_branch_list = result.get("project")
                download = result.get("artifact")
                createTagName = result.get("tagName")
                createTagMessage = result.get("tagMessage")
                mergeTargetBranch = result.get("targetBranch")
                mergeMessage = result.get("mergeMessage")
                piplineEnvironment = result.get("pipline")
                createBranchName = result.get("createBranchName")
                
                gitlab = GitLabTools()
                for p in project_branch_list:
                    projects_list = []
                    projects_list.append(p.get("name").replace("/","%2F"))
                    branch = p.get("branch")
                    gitlab.projects_id_list = projects_list
                    gitlab.projects = projects_list
                    gitlab.branch = branch
                    
                    pipline_data = json.dumps({"ref":branch,"variables":[{"key":"env","value": piplineEnvironment}]})
                    gitlab.download = download
                    gitlab.createtag = createTagName
                    gitlab.meassge = createTagMessage
                    gitlab.mergerequest["sbranch"] = branch
                    gitlab.mergerequest["tbranch"] = mergeTargetBranch
                    gitlab.mergerequest["title"] = mergeMessage
                    gitlab.pipline_data = pipline_data
                    gitlab.createBranchName = createBranchName

                    if download:
                        gitlab.download_by_shell()
                    if createTagName:
                        gitlab.create_tag()
                    if mergeTargetBranch:
                        gitlab.request_merge()
                    if piplineEnvironment:
                        gitlab.create_pipline()
                    if createBranchName:
                        gitlab.create_branch()

            elif type == "job":
                project_job_list = result.get("project")
                download = result.get("artifact")
                createTagName = result.get("tagName")
                createTagMessage = result.get("tagMessage")
                mergeSourceBranch = result.get("mergeSourceBranch")
                mergeTargetBranch = result.get("mergeTargetBranch")
                mergeMessage = result.get("mergeMessage")
                piplineSourceBranch = result.get("piplineSourceBranch")
                piplineTargetBranch = result.get("piplineTargetBranch")
                createBranchName = result.get("createBranchName")

                pipline_data = json.dumps({"ref": piplineSourceBranch, "variables":[{"key":"env","value": piplineTargetBranch}]})
                
                gitlab = GitLabTools()
                for p in project_job_list:
                    projects_list = []
                    projects_list.append(p.get("name").replace("/","%2F"))
                    job = p.get("job")
                    gitlab.projects_id_list = projects_list
                    gitlab.projects = projects_list
                    jobs_id_list = []
                    jobs_id_list.append(job)
                    gitlab.jobs_id_list = jobs_id_list

                    gitlab.download = download
                    gitlab.createtag = createTagName
                    gitlab.meassge = createTagMessage
                    gitlab.mergerequest["sbranch"] = mergeSourceBranch
                    gitlab.mergerequest["tbranch"] = mergeTargetBranch
                    gitlab.mergerequest["title"] = mergeMessage
                    gitlab.createBranchName = createBranchName
                    gitlab.pipline_data = pipline_data

                    if download:
                        gitlab.download_by_shell()
                    if createTagName:
                        gitlab.create_tag()
                    if mergeSourceBranch and mergeTargetBranch and mergeMessage:
                        gitlab.request_merge()
                    if createBranchName:
                        gitlab.create_branch()
                    if piplineSourceBranch and piplineTargetBranch:
                        gitlab.create_pipline()
        except Exception  as e:
            logger.exception(e)
        finally:
            result_text = {"message": "操作成功"}
            response = make_response(jsonify(result_text))
            return response

@app.route('/api/stream')
def stream():
    def generate():
        with open('%s/job.log' %dirname, mode='rb') as f:
            try:
                f.seek(-10000, 2)
            finally:
                while True:
                    for line in f.readlines():
                        yield "event: log\ndata: %s\n\n" %line.decode("utf-8")
                    sleep(1)
    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=54320)
    # server = make_server(host='0.0.0.0', port=54320, app=app)
    # server.serve_forever()
    # app.run()
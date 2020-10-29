from flask import Flask, redirect, url_for, request, render_template
from gitlabtools import GitLabTools,logger
import os
from time import sleep
import json
#from flask_cors import *
app = Flask(__name__)

dirname, filename = os.path.split(os.path.abspath(__file__))

#CORS(app, supports_credentials=True)
@app.route('/')
def hello_world():
   return render_template('index.html')

@app.route('/gitlab',methods = ['POST', 'GET'])
def gitlab():
   if request.method == 'POST':
        result = request.form
        project = result.get("project")
        select = result.get("select")
        selectInput = result.get("selectInput")
        download = result.get("download")
        createTag = result.get("createTag")
        createTagName = result.get("createTagName")
        createTagMessage = result.get("createTagMessage")
        createBranch = result.get("createBranch")
        createBranchName = result.get("createBranchName")
        merge = result.get("merge")
        mergeSourceBranch = result.get("mergeSourceBranch")
        mergeTargetBranch = result.get("mergeTargetBranch")
        mergeMessage = result.get("mergeMessage")
        pipline = result.get("pipline")
        piplineBranch = result.get("piplineBranch")
        piplineEnvironment = result.get("piplineEnvironment")
        pipline_data = json.dumps({"ref":piplineBranch,"variables":[{"key":"env","value":piplineEnvironment}]})
        
        gitlab = GitLabTools()
        gitlab.projects = list(filter(None, project.split(",")))
        gitlab.projects_id_list = gitlab.get_project()
        if select=="branch":
            gitlab.branch = selectInput
        elif select=="job":
            gitlab.jobs_id_list=list(filter(None, selectInput.split(",")))
        gitlab.download = download
        gitlab.createtag = createTagName
        gitlab.meassge = createTagMessage
        gitlab.mergerequest["sbranch"] = mergeSourceBranch
        gitlab.mergerequest["tbranch"] = mergeTargetBranch
        gitlab.mergerequest["title"] = mergeMessage
        gitlab.pipline_data = pipline_data
        gitlab.createBranchName = createBranchName

        if download:
            gitlab.download_by_shell()
        if createTag:
            gitlab.create_tag()
        if merge:
            gitlab.request_merge()
        if pipline:
            gitlab.create_pipline()
        if createBranch:
            gitlab.create_branch()
   return "gitlab"

@app.route('/stream')
def stream():
    def generate():
        with open('%s/job.log' %dirname, encoding="utf-8") as f:
        #with open('%s/gitlabtools.log' %dirname, encoding="utf-8") as f:
            while True:
                yield f.read()
                sleep(1)
    return app.response_class(generate(), mimetype='text/plain')


if __name__ == '__main__':
   app.run(debug=False, host="0.0.0.0", port=54321)

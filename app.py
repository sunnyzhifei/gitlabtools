from flask import Flask, redirect, url_for, request, render_template,make_response, jsonify
from gitlabtools import GitLabTools,logger
import os
from time import sleep
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

dirname, filename = os.path.split(os.path.abspath(__file__))

# @app.route('/')
# def hello_world():
#    return render_template('index.html')

@app.route('/gitlab',methods = ['POST', 'GET'])
def gitlab():
   if request.method == 'POST':
        result = json.loads(request.data.decode("utf-8"))
        print(result)
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
            piplineEnvironment = result.get("pipline")
            pipline_data = json.dumps({"ref":branch,"variables":[{"key":"env","value":piplineEnvironment}]})
            
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

            if download:
                gitlab.download_by_shell()
            if createTagName:
                gitlab.create_tag()
            if mergeTargetBranch:
                gitlab.request_merge()
            if piplineEnvironment:
                gitlab.create_pipline()

        elif type == "mutibranch":
            project_branch_list = result.get("project")
            download = result.get("artifact")
            createTagName = result.get("tagName")
            createTagMessage = result.get("tagMessage")
            mergeTargetBranch = result.get("targetBranch")
            mergeMessage = result.get("mergeMessage")
            piplineEnvironment = result.get("pipline")
            
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

                print(projects_list)
                print(branch)

                if download:
                    gitlab.download_by_shell()
                if createTagName:
                    gitlab.create_tag()
                if mergeTargetBranch:
                    gitlab.request_merge()
                if piplineEnvironment:
                    gitlab.create_pipline()

        result_text = {"message": "操作成功"}
        response = make_response(jsonify(result_text))
        return response

@app.route('/stream')
def stream():
    def generate():
        with open('%s/job.log' %dirname, encoding="utf-8") as f:
            while True:
                yield f.read()
                sleep(1)
    return app.response_class(generate(), mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=54321)
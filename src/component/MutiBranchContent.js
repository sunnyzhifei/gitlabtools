import React, { Component } from "react";
import ".././App.css";
import { Form, Input, Checkbox, Button, message } from "antd";
import { Select, Spin } from "antd";
import debounce from "lodash/debounce";
import axios from "axios";
import { MinusCircleOutlined, PlusCircleOutlined } from '@ant-design/icons';
import { config } from "../Api.js"

const { Option } = Select;

const headers = { "Private-Token": config.gitlab_token };

const layout = {
  labelCol: {
    span: 8,
  },
  wrapperCol: {
    span: 24,
  },
};

class MutiBranchContent extends Component {
  constructor(props) {
    super(props);
    this.fetchProject = debounce(this.fetchProject, 800);
    this.fetchBranch = debounce(this.fetchBranch, 800);
    this.state = {
      loading: false,
      project:{
        data: [],
        value: [],
        fetching: false
      },
      branch:{
        data: [],
        value: [],
        fetching: false
      }
    };
  }
  formRef = React.createRef();

  onFinish = (values) => {
    this.setState({loading: true})
    const form = values
    form.type = "mutibranch"
    // console.log("form: ",form)
    axios
      .post(`${config.apiServer}/api/gitlab`, 
        form
      )
      .then((res)=>{
        message.success(res.data.message)
        this.setState({loading: false})
      })
      .catch((err)=>{
        message.error("服务异常,请稍后重试")
        console.log(err)
        this.setState({loading: false})
      })
  };

  fetchProject = (value) => {
    this.setState({ project: {data: [], fetching: true }});
    axios
      .get(`http://${config.gitlab_domain}/api/v4/search`, {
        params: {
          scope: "projects",
          search: value,
        },
        headers: headers,
      })
      .then((response) => {
        const data = response.data.map((item) => {
          let data1 = [...this.state.project.data];
          data1.push(item.path_with_namespace);
          return data1;
        });
        const data2 = data.length ? data : ["none"];
        this.setState({ project: {data: data2, fetching: false }});
      })
      .catch((err) => {
        console.log(err);
      });
  };

  fetchBranch = (value,field) => {
    // console.log('field:',field)
    // console.log("formRef.project",this.formRef.current.getFieldValue("project")[field])
    if(this.state.project.value.length){
      if (this.state.project.value!=="none"){
        const projectName = this.formRef.current.getFieldValue("project")[field].name.replace("/","%2F")
        this.setState({branch: {data: [], fetching: true }});
        axios.all([
          axios.get(`http://${config.gitlab_domain}/api/v4/projects/${projectName}/repository/branches`, {
            params: {
              per_page: 500,
              search: value
            },
            headers: headers,
          }),
          axios.get(`http://${config.gitlab_domain}/api/v4/projects/${projectName}/repository/tags`, {
            params: {
              per_page: 500,
              search: value
            },
            headers: headers,
          })])
          .then(
            axios.spread((branchs,tags) => {
              let searchData = branchs.data.concat(tags.data)
              console.log("searchData: ",searchData)
              const data = searchData.map((item) => {
                let data1 = [...this.state.branch.data];
                data1.push(item.name);
                return data1;
              });
              this.setState({ branch:{ data: data, fetching: false }});
            })
          )
          .catch((err) => {
            console.log("err:",err);
          });
      }else {
        this.setState({ branch:{ data: ["none"], fetching: false }});
      }

    }
  };

  handleProjectChange = (value) => {
    this.setState({
      project:{
        value,
        data: [],
        fetching: false
      }
    });
  };

  handleBranchChange = (value) => {
    this.setState({
      branch:{
        value,
        data: [],
        fetching: false
      }
    });
  };


  render() {
    const { project,branch,loading } = this.state;
    return (
      <Form {...layout} ref={this.formRef} name="nest-messages" onFinish={this.onFinish} initialValues={{"project":[{
      }]}}>
        <Form.List name="project" >
        {(fields, { add, remove }) => {
          return (
            <div>
              {fields.map((field,index) => (
                  <Form.Item className="myant-form-item" required label={index === 0 ? 'project' : 'project'+index} key={'fields'+index} >
                    <Input.Group compact>
                      <Form.Item 
                      {...field}
                      name={[field.fieldKey, 'name']}
                      fieldKey={[field.fieldKey, 'name']}
                      key={'project'+index}
                      rules={[{ required: true, message: 'missing project name' }]}
                      >
                      <Select
                        showSearch
                        value={project.value}
                        placeholder="select project"
                        notFoundContent={project.fetching ? <Spin size="small" /> : null}
                        filterOption={false}
                        onSearch={this.fetchProject}
                        onChange={this.handleProjectChange}
                        style={{ width: "300px" }}
                      >
                        {project.data.map((d) => (
                          <Option key={d}>{d}</Option>
                        ))}
                      </Select>
                      </Form.Item>
                      <Form.Item 
                      {...field}
                      name={[field.fieldKey, 'branch']}
                      fieldKey={[field.fieldKey, 'branch']}
                      key={'branch'+index}
                      rules={[{ required: true, message: 'missing project branch' }]}
                      >
                      <Select
                        showSearch
                        value={branch.value}
                        placeholder="select branch or tag"
                        notFoundContent={branch.fetching ? <Spin size="small" /> : null}
                        filterOption={false}
                        onSearch={(value)=>{this.fetchBranch(value,field.fieldKey)}}
                        onChange={this.handleBranchChange}
                        style={{ width: "300px" }}
                      >
                        {branch.data.map((d) => (
                          <Option key={d}>{d}</Option>
                        ))}
                      </Select>
                      </Form.Item>
                      { fields.length > 1 ? (<MinusCircleOutlined
                        // style={{display: "inline"}}
                        className="dynamic-delete-button"
                        style={{ margin: '8px 8px' }}
                        onClick={() => {
                          remove(field.name);
                        }}
                      />): ''}
                      <PlusCircleOutlined
                        style={{ margin: '8px 8px' }}
                        onClick={() => {
                          add();
                        }}
                      />
                    </Input.Group>
                  </Form.Item>
              ))}
            </div>
          );
        }}
      </Form.List>
        <Form.Item
          name={"artifact"}
          label="artifact"
          valuePropName="checked"
        >
          <Checkbox></Checkbox>
        </Form.Item>
        <Form.Item label="createTag">
          <Input.Group compact>
            <Form.Item name={"tagName"}>
              <Input
                placeholder="tag name"
                style={{ display: "inline", width: "300px" }}
              />
            </Form.Item>
            <Form.Item name={"tagMessage"}>
              <Input
                placeholder="tag message"
                style={{ display: "inline", width: "500px" }}
              />
            </Form.Item>
          </Input.Group>
        </Form.Item>
        <Form.Item label="mergeCode">
          <Input.Group compact>
            <Form.Item name={"targetBranch"}>
              <Input
                placeholder="target branch"
                style={{ display: "inline", width: "300px" }}
              />
            </Form.Item>
            <Form.Item name={"mergeMessage"}>
              <Input
                placeholder="merge message"
                style={{ display: "inline", width: "500px" }}
              />
            </Form.Item>
          </Input.Group>
        </Form.Item>
        <Form.Item 
          name={"createBranchName"} 
          label="createBranch" 
          style={{ height: "56px" }}
        >
          <Input 
          style={{ width: "300px" }} 
          placeholder="input branch name"
          />
        </Form.Item>
        <Form.Item
          name={"pipline"}
          label="pipline"
          valuePropName="value"
          style={{ height: "56px" }}
        >
          <Select  style={{ width: 140 }} allowClear="true" placeholder="target env">
            <Option value="dev">dev</Option>
            <Option value="test">test</Option>
            <Option value="master">master</Option>
          </Select>
        </Form.Item>
        <Form.Item wrapperCol={{ ...layout.wrapperCol, offset: 7 }}>
          <Button type="primary" htmlType="submit" loading={loading}>
            Submit
          </Button>
        </Form.Item>
      </Form>
    );
  }
}

export default MutiBranchContent;

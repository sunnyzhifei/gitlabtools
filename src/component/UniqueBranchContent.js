import React, { Component } from "react";
// import ReactDOM from 'react-dom';
import ".././App.css";
import { Form, Input, Checkbox, Button, message } from "antd";
import { Select, Spin } from "antd";
import debounce from "lodash/debounce";
import axios from "axios";
import { apiServer } from "../Api.js"

const { Option } = Select;

const headers = { "Private-Token": "TM99wdzKSsZQJjPAL687" };

const layout = {
  labelCol: {
    span: 8,
  },
  wrapperCol: {
    span: 24,
  },
};

class BranchContent extends Component {
  
  constructor(props) {
    super(props);
    this.fetchProject = debounce(this.fetchProject, 800);
  }
  
  state = {
    loading: false,
    data: [],
    value: [],
    fetching: false,
  };

  onFinish = (values) => {
    this.setState({loading: true})
    const form = values
    form.type = "uniquebranch"
    console.log("form: ",form)
    axios
      .post(`${apiServer}/gitlab`, 
        form
      )
      .then((res)=>{
        message.success(res.data.message)
        this.setState({loading: false})
      })
      .catch((e)=>{
        message.error(e)
      })
  };
  fetchProject = (value) => {
    this.setState({ data: [], fetching: true });
    axios
      .get("http://git.iwellmass.com/api/v4/search", {
        params: {
          scope: "projects",
          search: value,
        },
        headers: headers,
      })
      .then((response) => {
        // console.log(response.data)
        const data = response.data.map((item) => {
          let data1 = [...this.state.data];
          data1.push(item.path_with_namespace);
          return data1;
        });
        const data2 = data.length ? data : ["none"];
        console.log(data2);
        this.setState({ data: data2, fetching: false });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  handleProjectChange = (value) => {
    this.setState({
      value,
      data: [],
      fetching: false,
    });
  };

  render() {
    const { fetching, data, value , loading} = this.state;
    return (
      <>
      <Form {...layout} name="nest-messages" onFinish={this.onFinish}>
        <Form.Item 
          name={"branch"} 
          label="branch" 
          rules={[{ required: true, message: 'missing branch' }]}
        >
          <Input 
          style={{ width: "300px" }} 
          placeholder="input branch"
          />
        </Form.Item>
        <Form.Item 
          name={"project"} 
          label="project" 
          rules={[{ required: true, message: 'missing project' }]}
        >
          <Select
            mode="multiple"
            labelInValue
            value={value}
            placeholder="select projects"
            notFoundContent={fetching ? <Spin size="small" /> : null}
            filterOption={false}
            onSearch={this.fetchProject}
            onChange={this.handleProjectChange}
            style={{ width: "800px" }}
          >
            {data.map((d) => (
              <Option key={d}>{d}</Option>
            ))}
          </Select>
        </Form.Item>
        <Form.Item
          name={"artifact"}
          label="artifact"
          valuePropName="checked"
        >
          <Checkbox></Checkbox>
        </Form.Item>
        <Form.Item label="createTag" >
          <Input.Group compact >
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
        >
          <Select style={{ width: 140 }} allowClear="true" placeholder="target branch">
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
      </>
    );
  }
}

export default BranchContent;

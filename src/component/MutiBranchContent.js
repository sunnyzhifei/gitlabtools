import React, { Component } from "react";
import ".././App.css";
import { Form, Input, Checkbox, Button, Space } from "antd";
import { Select, Spin } from "antd";
import debounce from "lodash/debounce";
import axios from "axios";
import { MinusCircleOutlined, PlusCircleOutlined } from '@ant-design/icons';

const { Option } = Select;

const headers = { "Private-Token": "TM99wdzKSsZQJjPAL687" };

const layout = {
  labelCol: {
    span: 8,
  },
  wrapperCol: {
    span: 16,
  },
};

const onFinish = (values) => {
  console.log(values);
};

class MutiBranchContent extends Component {
  constructor(props) {
    super(props);
    this.fetchProject = debounce(this.fetchProject, 800);
  }

  state = {
    data: [],
    value: [],
    fetching: false,
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
        const data2 = data.length ? data : ["not found"];
        console.log(data2);
        this.setState({ data: data2, fetching: false });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  fetchBranch = (value) => {
    this.setState({ data: [], fetching: true });
    axios
      .get("http://git.iwellmass.com/api/v4/search", {
        // /projects/5/repository/branches
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
        const data2 = data.length ? data : ["not found"];
        console.log(data2);
        this.setState({ data: data2, fetching: false });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  handleBranchChange = (value) => {
    this.setState({
      value,
      data: [],
      fetching: false,
    });
    console.log(this.state)
  };

  handleProjectChange = (value) => {
    this.setState({
      value,
      data: [],
      fetching: false,
    });
    console.log(this.state)
  };

  render() {
    const { fetching, data, value } = this.state;
    return (
      <Form {...layout} name="nest-messages" onFinish={onFinish} initialValues={{"project":[{
      }]}}>
        <Form.List name="project" >
        {(fields, { add, remove }) => {
          return (
            <div>
              {fields.map((field,index) => (
                <>
                  <Form.Item className="myant-form-item"  label={index === 0 ? 'project' : 'project'+index} key={index}>
                    <Input.Group compact>
                      <Form.Item 
                      {...field}
                      name={[field.name, 'name']}
                      fieldKey={[field.fieldKey, 'name']}
                      key={[field.fieldKey, 'name']}
                      rules={[{ required: true, message: 'missing project name' }]}
                      >
                      <Select
                        showSearch
                        value={value}
                        placeholder="Select Project"
                        notFoundContent={fetching ? <Spin size="small" /> : null}
                        filterOption={false}
                        onSearch={this.fetchProject}
                        onChange={this.handleProjectChange}
                        style={{ width: "300px" }}
                      >
                        {data.map((d) => (
                          <Option key={d}>{d}</Option>
                        ))}
                      </Select>
                        {/* <Input
                          placeholder="project name"
                          style={{ display: "inline", width: "300px" }}
                        /> */}
                      </Form.Item>
                      <Form.Item 
                      {...field}
                      name={[field.name, 'branch']}
                      fieldKey={[field.fieldKey, 'branch']}
                      key={[field.fieldKey, 'branch']}
                      rules={[{ required: true, message: 'missing project branch' }]}
                      >
                      <Select
                        showSearch
                        value={value}
                        placeholder="Select Branch"
                        notFoundContent={fetching ? <Spin size="small" /> : null}
                        filterOption={false}
                        onSearch={this.fetchBranch}
                        onChange={this.handleBranchChange}
                        style={{ width: "300px" }}
                      >
                        {data.map((d) => (
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
                {/* // </Space> */}
                </>
              ))}
            </div>
          );
        }}
      </Form.List>
        <Form.Item
          name={"artifact"}
          label="download artifact"
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
          name={"pipline"}
          label="pipline"
          initialValue="test"
          valuePropName="value"
        >
          <Select defaultValue="test" style={{ width: 120 }}>
            <Option value="dev">dev</Option>
            <Option value="test">test</Option>
            <Option value="master">master</Option>
          </Select>
        </Form.Item>
        <Form.Item wrapperCol={{ ...layout.wrapperCol, offset: 7 }}>
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
        </Form.Item>
      </Form>
    );
  }
}

export default MutiBranchContent;

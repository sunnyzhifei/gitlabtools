import {Form, Input, Button, Checkbox, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import React,{ Component } from 'react';
import ".././App.css";
import axios from "axios";
import { config } from "../Api.js"
import { Redirect } from "react-router-dom";

const LoginComponent = (props) => {
  const onFinish = (values) => {
    axios
      .post(`${config.apiServer}/api/login`, 
      values
      )
      .then((res)=>{
        if (res.data.state == 1) {
          message.error(res.data.message)
        }else {
          message.success(res.data.message)
          props.history.push('/')
        }
      })
      .catch((err)=>{
        message.error("服务异常,请稍后重试")
        console.log(err)
      })
  };

  return (
    <>
      <Form 
      name="normal_login"
      className="login-form"
      initialValues={{
        remember: true,
      }}
      onFinish={onFinish}
    >
      <Form.Item
        name="username"
        rules={[
          {
            required: true,
            message: 'Please input your Username!',
          },
        ]}
      >
        <Input prefix={<UserOutlined className="site-form-item-icon" />} placeholder="Username" />
      </Form.Item>
      <Form.Item
        name="password"
        rules={[
          {
            required: true,
            message: 'Please input your Password!',
          },
        ]}
      >
        <Input
          prefix={<LockOutlined className="site-form-item-icon" />}
          type="password"
          placeholder="Password"
        />
      </Form.Item>
      <Form.Item>
        <Form.Item name="remember" valuePropName="checked" noStyle>
          <Checkbox>Remember me</Checkbox>
        </Form.Item>
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" className="login-form-button">
          Log in
        </Button>
      </Form.Item>
    </Form>
      
    </>
  )
}


export default LoginComponent
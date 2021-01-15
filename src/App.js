import React,{Component} from 'react';
import './App.css';
import { Layout, Menu, Row, Col,Divider, message } from 'antd';
import {
  AppstoreOutlined,
  BarChartOutlined,
  CloudOutlined,
} from '@ant-design/icons';
import tsIcon from './gitlab-logo.png';
import  BranchContent from './component/UniqueBranchContent'
import  MutiBranchContent from './component/MutiBranchContent'
import LogContent from './component/LogContent'
import JobContent from './component/JobContent';
import axios from "axios";
import { config } from "./Api.js"
import { Redirect } from "react-router-dom";

const { Header, Content, Footer, Sider } = Layout;

class App extends Component{
  constructor(props) {
    super(props);
    this.state = {
      menu: "",
      isLogin: true
    };
  } 
  
  componentDidMount(){
    this.handleMenuClick({key: "1"})
    this.getLoginInfo()
  }
  

  getLoginInfo = () => {
    axios
      .get(`${config.apiServer}/api/login`, 
      )
      .then((res)=>{
        if (res.data.state == 1) {
          this.setState({isLogin: false})
          message.error(res.data.message)
        }else {
          this.setState({isLogin: true})
        }
      })
      .catch((err)=>{
        message.error("服务异常,请稍后重试")
        console.log(err)
      })
  };
  handleMenuClick = e => {
    if (e.key === "1" ) {
      this.setState({menu: <BranchContent />})
    } else if (e.key === "2") {
      this.setState({menu: <MutiBranchContent />})
    } else if (e.key === "3") {
      this.setState({menu: <JobContent />})
    }
  }
  render (){
    
    console.log("state1: ",this.state)
    if ( this.state.isLogin){
      return (
        <Layout>
          <Sider
            style={{
              overflow: 'auto',
              height: '100vh',
              position: 'fixed',
              left: 0,
            }}
          >
            <div className="logo">
              <img src={tsIcon} alt= "" height="50" width="50"/>
            </div>
            <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']} onClick={this.handleMenuClick}>
              <Menu.Item key="1" icon={<BarChartOutlined />}>
                按单分支
              </Menu.Item>
              <Menu.Item key="2" icon={<CloudOutlined />}>
                按多分支
              </Menu.Item>
              <Menu.Item key="3" icon={<AppstoreOutlined />}>
                按任务
              </Menu.Item>
            </Menu>
            <Footer className="footer">Copyright©2020 Created by lizhifei</Footer>
          </Sider>
          <Layout className="site-layout" style={{ marginLeft: 200,height: "900px"}}>
            <Header className="site-layout-background" style={{ padding: 0 ,backgroundColor:'#FFF'}} />
            <Content style={{ margin: '24px 16px 0', overflow: 'initial' ,backgroundColor:'#FFF'}}>
              <Row>
                <Col span={14}>
                  <div id='content' className="site-layout-background" style={{ padding: 24, textAlign: 'center'}}>
                    { this.state.menu}
                  </div>
                </Col>
                <Divider type="vertical" style={{height: "700px"}}/>
                <Col span={9}>
                  <LogContent />
                </Col>
              </Row>
            </Content>
          </Layout>
        </Layout>
      )
    } else {
      return <Redirect push to="/login" />
    }
  }
}

export default App
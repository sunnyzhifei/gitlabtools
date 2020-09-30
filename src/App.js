import React,{Component} from 'react';
import ReactDOM from 'react-dom'
import './App.css';
import { Layout, Menu } from 'antd';
import {
  AppstoreOutlined,
  BarChartOutlined,
  CloudOutlined,
} from '@ant-design/icons';
import tsIcon from './gitlab-logo.png';
import  BranchContent from './component/UniqueBranchContent'
import  MutiBranchContent from './component/MutiBranchContent'
// import { BrowserRouter as Router, Route, Link } from "react-router-dom";

const { Header, Content, Footer, Sider } = Layout;

class App extends Component{

  componentDidMount(){
    this.handleMenuClick({key: "1"})
  }

  handleMenuClick = e => {
    if (e.key === "1" ) {
      ReactDOM.render(<BranchContent />,document.getElementById('content'))
    } else if (e.key === "2") {
      ReactDOM.render(<MutiBranchContent />,document.getElementById('content'))
    } else if (e.key === "3") {
      ReactDOM.render(<>key=3</>,document.getElementById('content'))
    }
  }
  render (){
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
        <Layout className="site-layout" style={{ marginLeft: 200 }}>
          <Header className="site-layout-background" style={{ padding: 0 }} />
          <Content style={{ margin: '24px 16px 0', overflow: 'initial' }}>
            <div id='content' className="site-layout-background" style={{ padding: 24, textAlign: 'center' }}>
              {/* <BranchContent />  */}
            </div>
          </Content>
        </Layout>
      </Layout>
    )
  }
}

export default App
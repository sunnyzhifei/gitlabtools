import React, { Component } from "react";
import ".././App.css";
import { Divider } from "antd";
import { apiServer } from "../Api.js"

class LogContent extends Component{
    constructor(props) {
        super(props);
        this.state={
            isScroll: true,
            intervalId:'',
            log: [],
        }
      }

    componentDidMount() {
        const source = new EventSource(`${apiServer}/stream`)
        source.addEventListener('log',(event)=>{
            const { data } = event
            // const dataString = data.replace(/^(\s|b')+|(\s|\\n')+$/g,'').replace(/^(\s|b")+|(\s|\\n")+$/g,'');
            // console.log("dataString: ",dataString)
            this.setState({
                log: [...this.state.log, data]
            }) 
        })
        this.setState({
            intervalId: setInterval(this.scrollme, 1000)
        })
    }
    
    scrollme = ()=>{ 
        var output = document.getElementById("output");
        output.scrollTop = output.scrollHeight;
    }
    handleClick = ()=>{
        if(this.state.isScroll){
            clearInterval(this.state.intervalId);
            this.setState({isScroll:false})
        }else{
            this.setState({
                isScroll: true,
                intervalId: setInterval(this.scrollme, 1000)
            })
        }
    }

    byteToString(arr) {
        //声明一个Uint8Array，经常被用来存放字节
        let bytes=new Uint8Array(arr);
        let str="";
        for(let i=0;i<bytes.length;i++){
          //用16进制表示字节
          let k=bytes[i].toString(16);
          //如果只有1位在前面补0
          if(k.length==1)k="0"+k;
          //储存为URI格式
          str += "%"+k
        }
        //output就是bytes转换后的string啦！
        let output=decodeURI(str);
        return output
    }
    
    render (){
        return (
            <div id="logs" style={{backgroundColor:"#FFF", height:"100%"}}>
                <Divider type="horizontal" orientation="center">Logs</Divider>
                <pre 
                id="output" 
                style={{backgroundColor:"#FFF",fontSize:"smaller"}} 
                onClick={this.handleClick}
                >
                    {
                        this.state.log.map((item)=>{
                            return <div>{item}</div>
                        })
                    }
                </pre>
            </div>
        )
    }
}

export default LogContent;
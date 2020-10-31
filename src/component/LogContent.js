import React, { Component } from "react";
import ".././App.css";
import { Divider } from "antd";

class LogContent extends Component{
    constructor(props) {
        super(props);
        this.state={
            isScroll: true,
            intervalId:''
        }
      }
      
    // output.scrollTop = output.scrollHeight;\
    componentDidMount() {
        let script = document.querySelector('#script');
        if (script) {
            return;
        }
        script = document.createElement('script');
        script.id = 'script';
        script.textContent='\
            var output = document.getElementById("output");\
            var xhr = new XMLHttpRequest();\
            xhr.open("GET", "http://localhost:54321/stream");\
            xhr.send();\
            setInterval(function() {\
                output.textContent = xhr.responseText ? xhr.responseText : "no content";\
            }, 1000);\
            '
        document.querySelector('#logs').appendChild(script);
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
    
    render (){
        return (
            <div id="logs" style={{backgroundColor:"#FFF", height:"100%"}}>
                <Divider type="horizontal" orientation="center">Logs</Divider>
                <pre id="output" style={{backgroundColor:"#FFF",fontSize:"smaller"}} onClick={this.handleClick}></pre>
            </div>
        )
    }
}

export default LogContent;
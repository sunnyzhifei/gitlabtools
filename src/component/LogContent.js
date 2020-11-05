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
            logtemp: ''
        }
      }
      
    // output.scrollTop = output.scrollHeight;\
    componentDidMount() {
        // let script = document.querySelector('#script');
        // if (script) {
        //     return;
        // }
        // script = document.createElement('script');
        // script.id = 'script';
        // script.textContent=`\
        //     var output = document.getElementById("output");\
        //     var source = new EventSource('${apiServer}/stream');\
        //     source.onmessage = function(event) {\
        //         output.innerHTML += "<div>" + event.data + "</div>";\
        //     }`
        // document.querySelector('#logs').appendChild(script);
        const source = new EventSource(`${apiServer}/stream`)
        source.addEventListener('log',(event)=>{
            const { data } = event
            // console.log(data.slice(-2))
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
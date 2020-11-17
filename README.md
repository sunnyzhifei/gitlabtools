## Display
![gitlabtools.png](https://s3.ax1x.com/2020/11/17/DZECgH.png)


## Available Scripts

In the project directory, you can run:

### `sh start.sh`

### `sh stop.sh`


## Devlopment

### frontend
```shell
yarn install
yarn start
yarn build
```
### backend
```shell
python3 main.py
```


## If you use nginx to proxy, config like below:
```
server {
    listen       80;
    server_name  gitlabtool.iwellmass.com;
    location ~* / {
        proxy_set_header Connection '';
        proxy_http_version 1.1;
        chunked_transfer_encoding off;
        proxy_buffering off;
        proxy_cache off;
        proxy_pass              http://192.168.10.219:54320;
    }
```
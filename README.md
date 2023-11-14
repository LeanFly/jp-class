# jp-class
This is a python project, it is designed to get torrents from onejav, then send torrents link to qbittorrents to download the videos.
### 自定义配置文件： 
- 容器默认指定了一个 config.yaml 的配置文件
- 需要自定义的可以预先创建，然后挂载给容器
- 容器的工作目录是 /code，可以将本地的配置文件挂在给 /code/config.yaml

#### 配置文件使用的 yaml 格式，分三个部分，一个是 qbit 的配置，一个是页面 url，一个是请求的频率(以天为单位)： 

```
    # 开始配置 qbit
    qbit:
      host: "172.17.0.1"
      port: 7070
      username: "admin"
      password: "admin"
      savedir: "/downloads"
    # 开始配置需要处理的页面
    torrents_page: "aHR0cHM6Ly9vbmVqYXYuY29tL3BvcHVsYXIvP2phdj0x"
    # 开始配置请求频率，单位是天
    days: 7
```


### 启动命令：
- docker run -dit --name xxx -v xxx:/code leanfly/jp-class:latest

# maa_control_api

配合[MAA远程控制协议](https://maa.plus/docs/%E5%8D%8F%E8%AE%AE%E6%96%87%E6%A1%A3/%E8%BF%9C%E7%A8%8B%E6%8E%A7%E5%88%B6%E5%8D%8F%E8%AE%AE.html)编写的HTTP API Server，基于fastAPI实现，可以满足小规模的MAA远程控制

## 服务部署

推荐使用[docker image](https://hub.docker.com/r/windoge/maa-control-api)进行部署

Docker Compose Example:
```
version: "3"
services:
  maa-api:
    container_name: maa-api
    image: windoge/maa-control-api:latest
    restart: always
    ports:
      - "8098:8098"
    tty: true
    stdin_open: true
    volumes:
      - /share/Docker/maa/ssl/:/app/maa_control_api/ssl/
      - /share/Docker/maa/config/config.yaml:/app/maa_control_api/config/config.yaml
    depends_on:
      redis: { condition: service_healthy }

  redis:
    container_name: maa-api-redis
    image: redis:alpine
    restart: always
    volumes:
      - /share/Docker/maa/redis/data:/data
      - /share/Docker/maa/redis/logs:/logs
    healthcheck:
      test: [ "CMD", "redis-cli", "PING" ]
      start_period: 10s
      interval: 5s
      timeout: 1s
```

## 使用yunzaiBot进行控制
需要使用[arknights-plugin](https://github.com/gxy12345/arknights-plugin)。部署API服务和机器人插件后，修改`plugins/arknights-plugin/config/maa.yaml`文件，将maa_api_host修改为API服务的url(含端口)

之后即可使用yunzaiBot来控制MAA

<img width="807" alt="image" src="https://github.com/gxy12345/maa_control_api/assets/13727139/3ccd54c8-207a-4f19-aa8c-7d4d5ed1e5d3">



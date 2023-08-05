# Introduction
本项目用于提供 API 供外部查询关键词为 NFT 的谷歌搜索指数

# How to deploy it
Make sure you work directory is root of the project

## build & push docker image
```
docker build -t magicalbomb/google-trends-service:latest . && docker push magicalbomb/google-trends-service:latest
```

## deploy it on k8s
```
kubectl apply -f deployment.yaml
```


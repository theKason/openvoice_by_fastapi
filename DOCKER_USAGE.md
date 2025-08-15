# OpenVoice TTS API Docker 使用说明

## 快速开始

### 方法1: 直接运行
```bash
docker run -d -p 8000:8000 4o4notloved/openvoice-tts-api:latest
```

### 方法2: 使用docker-compose
```bash
# 下载docker-compose.yml
wget https://raw.githubusercontent.com/your-repo/openvoice_api/main/docker-compose.yml

# 启动服务
docker-compose up -d
```

## API访问
- 服务地址: http://localhost:8000
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

## 数据持久化
```bash
docker run -d -p 8000:8000 \
  -v $(pwd)/user_data:/app/user_data \
  -v $(pwd)/processed:/app/processed \
  4o4notloved/openvoice-tts-api:latest
```

## 环境变量
- `CUDA_VISIBLE_DEVICES`: GPU设备ID (默认: 0)
- `PYTHONUNBUFFERED`: Python输出缓冲 (默认: 1)

## 系统要求
- Docker 20.10+
- 内存: 至少4GB
- 存储: 至少10GB可用空间
- GPU: 可选 (NVIDIA GPU + nvidia-docker)

## 故障排除
1. 检查容器状态: `docker ps`
2. 查看日志: `docker logs <container_id>`
3. 进入容器: `docker exec -it <container_id> bash`

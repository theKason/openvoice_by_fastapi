# OpenVoice FastAPI 服务

本项目基于 [OpenVoice](https://github.com/myshell-ai/OpenVoice) 进行二次封装，提供语音合成功能的 FastAPI 接口服务。

---

## 环境准备

建议使用 Conda 创建 Python 3.9 虚拟环境：

```bash
conda create -n openvoice python=3.9
conda activate openvoice
````

## 项目克隆与依赖安装
```bash
git clone git@github.com:myshell-ai/OpenVoice.git
```
注意：OpenVoice 源码将被放置在本项目根目录的 openvoice_service 文件夹内，请确保将源码放置到此目录下。
进入 openvoice_service 目录后，执行：

```bash
cd openvoice_service
pip install -e .
pip install git+https://github.com/myshell-ai/MeloTTS.git
python -m unidic download
```

## 安装项目依赖

将本项目根目录的 `requirements.txt` 文件内依赖安装：

```bash
pip install -r requirements.txt
```

## 启动 FastAPI 服务

项目源码位于 `openvoice_service` 文件夹下，执行以下命令启动服务：

```bash
uvicorn openvoice_service.main:app --reload
```

服务默认监听 `http://127.0.0.1:8000`。

## 使用说明

* 访问 `http://127.0.0.1:8000/docs` 查看 Swagger API 文档，方便调试和测试接口。
* 访问 `http://127.0.0.1:8000/redoc` 查看更详细的接口文档。

## 备注

* 请确保运行前已成功安装所有依赖并完成 `unidic` 数据下载。

---

欢迎提交 Issues 或 Pull Requests 交流和改进。

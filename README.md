# OpenVoice FastAPI Service

This project is based on [OpenVoice](https://github.com/myshell-ai/OpenVoice) for secondary encapsulation, providing FastAPI interface services for voice synthesis functionality.

---

## Environment Setup

It is recommended to use Conda to create a Python 3.9 virtual environment:

```bash
conda create -n openvoice python=3.9
conda activate openvoice
```

## Project Cloning and Dependency Installation
```bash
git clone git@github.com:myshell-ai/OpenVoice.git
```
Note: The OpenVoice source code will be placed in the openvoice_service folder in the project root directory. Please ensure the source code is placed in this directory.
After entering the openvoice_service directory, execute:

```bash
cd openvoice_service
pip install -e .
pip install git+https://github.com/myshell-ai/MeloTTS.git
python -m unidic download
```

## Install Project Dependencies

Install the dependencies in the `requirements.txt` file in the project root directory:

```bash
pip install -r requirements.txt
```

## Start FastAPI Service

The project source code is located in the `openvoice_service` folder. Execute the following command to start the service:

```bash
uvicorn openvoice_service.main:app --reload
```

The service defaults to listening on `http://127.0.0.1:8000`.

## Usage Instructions

* Visit `http://127.0.0.1:8000/docs` to view the Swagger API documentation for easy debugging and interface testing.
* Visit `http://127.0.0.1:8000/redoc` to view more detailed interface documentation.

## Notes

* Please ensure all dependencies are successfully installed and `unidic` data download is completed before running.

---

Welcome to submit Issues or Pull Requests for communication and improvements.

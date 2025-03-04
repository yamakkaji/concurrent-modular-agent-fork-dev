# Concurrent Modular Agent

This is a framework for concurrent modular agent. 
<img width="1317" alt="CMA_architecture" src="https://github.com/user-attachments/assets/c6491062-554d-4a89-a468-ae0b561075cf" />

## Setup
Install docker
https://docs.docker.com/engine/install/



It is recommended to use a virtual environment
```console
$ python -m venv .venv
$ source .venv/bin/activate
```

Install required packages and this repository.
```console
$ pip install -r requirements.txt
$ pip install -e .
```

#### Test
1. Start backend services.
```console
$ python -m concurrent_modular_agent.backend start
```

2. Set the OpenAI API Key
```console
$ export OPENAI_API_KEY="your api key"
```

3. Run test.
```console
$ pytest
```

## Start backend services
Run
```console 
$ python -m concurrent_modular_agent.backend start
```


## Examples

Please check tests directory.

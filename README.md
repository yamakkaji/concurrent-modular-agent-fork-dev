# Concurrent Modular Agent
<img width="1292" alt="cma_architecture" src="https://github.com/user-attachments/assets/07ba751e-64a9-4e34-805c-0c0ce8ef8512" />

## Setup
Install docker
https://docs.docker.com/engine/install/



It is recommended to use a virtual environment
```console
$ python -m venv .venv
$ source .venv/bin/activate
```

Install 
```console
$ pip install -e ".[dev]"
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
Examples of modules and agents are provided in `./examples`


### New CLI interface

```console
$ coma examples/project_interface/chat
```

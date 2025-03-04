This is concurrent modular agent framework.


## Setup
Install docker
https://docs.docker.com/engine/install/



It is recommended to use a virtual environment
```console
$ python3 -m venv .venv
$ source .venv/bin/activate
```

Install required packages and this repository.
```console
$ pip install -r requirements.txt
$ pip install -e .
```

Test
```console
$ pytest
```

Set the OpenAI API Key
```console
$ export OPENAI_API_KEY="your api key"
```

## Start backend services
Run `python -m concurrent_modular_agent.backend start`


## Examples

Please check tests directory.

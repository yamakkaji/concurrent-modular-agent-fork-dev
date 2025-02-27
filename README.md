


## Setup
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

Set the OpenAI API Key
```console
$ export OPENAI_API_KEY="your api key"
```

## Start backend services
Run `python -m concurrent_module_agent.backend start`

## Start example

```console
$ cd examples/plantbot
```

Execute the following in separate terminals

### 1. Start all modules except the TextChat module.
```console
$ python main.py
```

Access `http://127.0.0.1:8050/` to view the Agent Visualizer.

The TextChat module uses a CUI, so it should be executed in a separate terminal in the next step.

### 2. Start the TextChat module
```console
$ python mods/textchat.py
```


## Tips

Run only visualizer
```console
$ python -m concurrent_module_agent.visualizer
```


### generate documents
```console
$ sphinx-apidoc -f -o docs/source concurrent_module_agent 
$ sphinx-build -b html ./docs/source ./docs/build 
```
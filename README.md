# Concurrent Modular Agent
<img width="1292" alt="cma_architecture" src="https://github.com/user-attachments/assets/07ba751e-64a9-4e34-805c-0c0ce8ef8512" />

**Welcome to Concurrent Modular Agent (CoMA) Framework!** 
CoMA is designed to simplify the development of agents that collaborate in a modular and concurrent fashion. It draws inspiration from subsumption architecture, asynchronous message passing in concurrent programming, the global workspace model, and the core software design principles of modularity and reusability.

## Explore the concepts
For a detailed guide on the framework, please refer to our [paper](https://www.google.com). 

### Core ideas
- **Modularity**: The framework follows a modular design that enables developers to create and integrate various independent modules easily. Each module can be developed, tested, and reused across multiple projects.

- **Concurrency**: The framework supports concurrent execution of multiple modules, allowing them to work in parallel and share information efficiently. This is achieved through two primary mechanisms:
    - **Message Passing**: CoMA employs a message-passing system that supports asynchronous communication, allowing modules to exchange information without tight coupling. (Currently, the message passing is implemented using MQTT protocol)
    - **Shared Memory**: The framework also features a global memory component—--currently implemented as a vector store using Chroma DB--—that lets modules share and retrieve data efficiently. This mechanism is ideal for storing information that may be needed by self or different modules later.


## Installation

### Prerequisites

- **Python 3.12 or Later**  
  This implementation uses the `multiprocessing` and `asyncio` modules available in Python 3.12 and newer.
  
- **Docker**

### Tested Platforms

The framework has been validated on the following platforms:

- **MacOS**  
  - Apple M1 Max (macOS 15.4, Build 24E248)
- **Ubuntu**

### Setup
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
*Note: You may need to run Docker before starting the backend services.*

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

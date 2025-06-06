# 1. Installation

## Prerequisites
Before installing CoMA, ensure you have the following prerequisites:

* Python 3.12 or later

    CoMA uses multiprocessing and asyncio, which are fully supported in Python 3.12 and later versions.

* Docker 

    CoMA uses Docker to run modules (specifically, `MQTT` for messaging and `ChromaDB` for vector storage). Ensure you have Docker installed and running on your machine. Please refer to the [Docker installation guide](https://docs.docker.com/get-docker/) for instructions.

## Setup

It is recommended to use a virtual environment. 
```console
$ python -m venv .venv
$ source .venv/bin/activate
```
Install the required packages.
```console
$ pip install -e ".[dev]"
```

## Test
### 1. Start backend services.
```console
$ coma backend start
```
**Note: You need to run Docker before starting the backend services.**

*Tips: for MacOS users, you need to run the Docker Desktop application. Not CLI commands.*

You can use the `start`, `stop`, and `restart` commands to manage the backend services. For example, to stop the backend services, run:
```console
$ coma backend stop
```

### 2. Set the OpenAI API Key
```console
$ export OPENAI_API_KEY="your api key"
```

### 3. Run test.
```console
$ pytest
```
If you pass each test, you should see output similar to:
```console
....
```
Otherwise, you will see output indicating which tests failed or encountered errors.
```console
..!!!
```

Now you are ready to start building your agential systems with CoMA!

<div style="text-align: center; margin: 2rem 0;">
    <a href="../creating-a-new-project" class="indigo-button">
        🚀 Creating Projects
    </a>
</div>

<style>
.indigo-button {
    display: inline-block;
    padding: 12px 32px;
    background-color: #3F51B5;
    color: #FFFFFF !important;
    text-decoration: none !important;
    border-radius: 6px;
    font-weight: 600;
    font-size: 16px;
    box-shadow: 0 3px 6px rgba(63, 81, 181, 0.25);
    transition: all 0.2s ease;
    border: none;
}

.indigo-button:hover {
    background-color: #303F9F;
    box-shadow: 0 4px 8px rgba(63, 81, 181, 0.35);
    transform: translateY(-1px);
    color: #FFFFFF !important;
    text-decoration: none !important;
}

.indigo-button:visited {
    color: #FFFFFF !important;
}

.indigo-button:active {
    color: #FFFFFF !important;
}
</style>
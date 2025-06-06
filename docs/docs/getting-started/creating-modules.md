# 3. Creating Modules (CoMA Interface)

## Make a modeule

In this section, we will create three simple modules that well explain the basic concepts of CoMA modules.
These modules will be used to build a simple chat application that can respond to user input.
We will create the following modules:

1. `user_input`: A module that receives user input and sends it to the `chat` module.

2. `chat`: A module that receives messages from the `user_input` module and responds to the user.

3. `memory_organizer`: A module that organizes the memory of the agent.

![Overview of a simple CoMA agent](../img/my-first-coma.png)

### Make a new project directory with agent directory
To start your first project, create a directory named `my_project` and `my_project/agent1` or do 
```shell
mkdir -p my_project/agent1
```

### Make a new module file
Next, create a file named `user_input.py` in the `my_project/agent1` directory. This file will define your first module, which is a simple chat module that can respond to user input.

```shell
touch my_project/agent1/user_input.py
```

## Make a new module definition
Now, open `user_input.py` in your favorite text editor and add the following code:

```python
# my_project/agent1/user_input.py
import time
import concurrent_modular_agent as coma

@coma.module_main('user_input')
def mod_user_input(agent:coma.AgentInterface):
    while True:                              # continuously run this module
        m = input("User: ")
        if len(m) == 0 or m.isspace() or m is None:  # if the user input is empty, skip to the next iteration
            continue
        agent.state.add(f"user_message:{m}")
        agent.message.send("chat", "reply to user")  # send message to the "chat" module
        time.sleep(3)                        # wait for 3 seconds before next input
```

Overall, this code defines a module named `user_input` that continuously receives user inputs. When the user enters a message (`m` in the code above), it adds the message to the agent's *state* and sends a message to the "`chat`" module to reply. 

Let's disect this code to get a sense of how CoMA modules work.

### Disecting the module code

The first line imports the `concurrent_modular_agent` package, which provides the necessary functions and classes to define and run CoMA modules.

The `@coma.module_main(module_name)` decorator instantiate an `AgentInterface` object with the specified name of the module. This object provides basic functionalities for modules, state IO and messaging IO. Using this decorator turns a function which takes an `AgentInterface` object as an argument into a module function. Notice that the `module_name` is specified as `'user_input'`, which can be different from the file name or the function name. 

```python

### Module function
The `mod_user_input` function is the main function of the module. Let's break down its components:
```python
while True:
    ...
    time.sleep(3)
```
This loop ensures that the module runs continuously, allowing it to receive user inputs repeatedly. The `time.sleep(3)` line introduces a 3-second delay between each input, preventing the module from overwhelming the user with prompts.

```python
m = input("User: ")
if len(m) == 0 or m.isspace() or m is None:
    continue
```
This line receives input from the user. The input is stored in the variable `m`. 
If the user input is empty (i.e., the user just pressed Enter without typing anything), only whitespace, or `None`, the module skips to the next iteration of the loop, effectively ignoring empty inputs.

```python
agent.state.add(f'user_message:{m}')
```
This line adds the user message to the agent's state. 
The **state** is a shared memory space where modules can store and retrieve information. 
The `AgentInterface.state` object provides access to this state. 
The `AgentInterface.state.add` method is used to store new information in the state.
At this time, the received user input `user_message:{m}`, where `{m}` is the actual user input, is added to the state. 

```python
agent.message.send("chat", "reply")
```
This line sends a message "`reply`" to the "`chat`" module. 
The `message` object allows modules to communicate with each other by sending and receiving messages. 
At this time, the `send` method is used to send a message to the "`chat`" module, which is expected to handle the reply.

## Make a chat module
Next, create a file named `chat.py` in the `my_project/agent1` directory. This file will define your second module, which is a simple chat module that can respond to user input.

```shell
touch my_project/agent1/chat.py
```

Now, open `chat.py` in your favorite text editor and add the following code:

```python
# my_project/agent1/chat.py
@coma.module_main('chat')
def mod_response_to_user(agent:coma.AgentInterface):
    openai_client = OpenAI()
    while True:
        m = agent.message.receive()
        if m is None:
            continue  # If no message is received, skip to the next iteration
        messages = [
            {"role": "developer", "content": "You are a module of an autonomous agent. Your job is to respond to the user's input. You are expected to talk with the user. You are not an AI assistant, so feel free to talk freely. You do not need to help humans. You received the following messages from the user, other modules. Talk to the user in a natural way."},
        ]
        for s in agent.state.get(max_count=10).texts[::-1]:
            if s.startswith("user_message:"):
                messages.append({"role": "user", "content": s[len("user_message:"):]})
            elif s.startswith("assistant_message:"):
                messages.append({"role": "assistant", "content": s[len("assistant_message:"):]})
        messages.append({"role": "assistant", "content": f"{m}})

        completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        output_message = completion.choices[0].message.content
        print(f'ChatBot: {output_message}')
        agent.state.add(f"assistant_message:{output_message}")

        agent.message.send("user_input", 'chat response finished')
```

### Disecting the chat module code
The basics are similar to the `user_input` module. 
The module is defined with the `@coma.module_main('chat')` decorator, which allows it to be recognized as a module named "`chat`". 
The `mod_response_to_user` function is the main function of the module. 
It continuously listens for messages from the `user_input` module and sends responses back to the module like the last module.

```python
@coma.module_main('chat')
def mod_response_to_user(agent:coma.AgentInterface):
    ...
    while True:
        m = agent.message.receive()               # receive message from user_input module
        ...
        agent.message.send("user_input", 'chat response finished') # send message to user_input module to tell it finished processing
```

There are four new things in this module code.
The first is when the module activates. 
```python
while True:
    m = agent.message.receive()
    if m is None:
        continue  # If no message is received, skip to the next iteration
```
The module runs continuously, waiting for messages from the `user_input` module.
If the module receives a message, it activates and processes the message to respond to the user.

The second is LLM interface. At this moment, we use *OpenAI*'s API to interact with the LLM.
```python
openai_client = OpenAI()
...
        completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
```

The third is state retrieval. 
```python
for s in agent.state.get(max_count=10).texts[::-1]:
    if s.startswith("user_message:"):
        messages.append({"role": "user", "content": s[len("user_message:"):]})
    elif s.startswith("assistant_message:"):
        messages.append({"role": "assistant", "content": s[len("assistant_message:"):]})
```
We retrieve the latest state using `AgentInterface.state.get()`, which returns the most recent state of the agent. The `texts` property of the state object contains all text entries in the state, and we reverse it to process the most recent messages first.

The obtained state is checked for messages that start with `user_message:` or `assistant_message:`. 
If the message starts with `user_message:`, it is treated as a user message, and if it starts with `assistant_message:`, it is treated as an assistant message. 
The messages are then appended to the `messages` list, which will be sent to the LLM.

The fourth is output to the user.
```python
output_message = completion.choices[0].message.content
print(f'ChatBot: {output_message}')
agent.state.add(f'assistant_message:{output_message}')
```
The output from the LLM is stored in the `output_message` variable, which is then printed to the console. 
The output message is also added to the agent's state with the prefix `assistant_message:`.

In the end, the module sends a message to the `user_input` module to signal that it has finished processing the input and is ready for the next message.
```python
agent.message.send("user_input", 'finish')
```

## Make a memory organizer module
Next, create a file named `memory_organizer.py` in the `my_project/agent1` directory. This file will define your third module, which is a simple memory organizer module that organizes the memory of the agent.

```shell
touch my_project/agent1/memory_organizer.py
```
Now, open `memory_organizer.py` in your favorite text editor and add the following code:

```python
# my_project/agent1/memory_organizer.py
import time
import random

import concurrent_modular_agent as coma
from concurrent_modular_agent import OpenAI

@coma.module_main('memory_organizer')
def mod_organize_memory(agent: coma.AgentInterface):
    openai_client = OpenAI()
    while True:
        m = agent.message.receive()
        messages = [
            {"role": "developer", "content": "You are a module of an autonomous agent. Your job is to organize the memory of the agent. You are expected to organize the memory of the agent in a way that is helpfull to recall the past and what the agent had thought. You will be given a list of memory of received the following messages from the user, other modules."},
        ]
        organizing_range = random.randint(5, 10)  # Randomly decide how many messages to organize
        for s in agent.state.get(max_count=10).texts[::-organizing_range]:
            if s.startswith("user_message:"):
                messages.append({"role": "user", "content": s[len("user_message:"):]})
            elif s.startswith("assistant_message:"):
                messages.append({"role": "assistant", "content": s[len("assistant_message:"):]})
        messages.append({"role": "assistant", "content": f"{m}})
        
        completion = openai_client.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=messages,
        )
        output_message = completion.choices[0].message.content
        agent.state.add(f'assistant_message:{output_message}')

        time.sleep(100)  # Wait for 3 seconds before next input
```

### Disecting the memory organizer module code
The `memory_organizer` module is similar to the `chat` module, but it has a different purpose.
It organizes the memory of the agent stored in the state.

The main part of the module is collect a random numbers of states from the shared memory and send them to the LLM to organize the memory.

This part collects 5~10 states from the agent's memory:
```python
organizing_range = random.randint(5, 10)  # Randomly decide how many messages to organize
for s in agent.state.get(max_count=10).texts[::-organizing_range]:
    if s.startswith("user_message:"):
        messages.append({"role": "user", "content": s[len("user_message:"):]})
    elif s.startswith("assistant_message:"):
        messages.append({"role": "assistant", "content": s[len("assistant_message:"):]})
messages.append({"role": "assistant", "content": f"{m}})
```

The output of the LLM is stored to memory as an `assistant_message`:
```python
output_message = completion.choices[0].message.content
agent.state.add(f'assistant_message:{output_message}')
```

Notice that the `memory_organizer` module does not send any message to other modules.

### Concurrency of memory organizer module
The `memory_organizer` module is designed to run concurrently with the `user_input` and `chat` modules.
This means that it can run in parallel with the other modules, allowing it to organize the memory of the agent while the user is interacting with the agent.
Although both `user_input` and `chat` modules are designed to run continuously, `user_input` module will send messages only when the user inputs a message, and `chat` module will send messages only when it receives a message from the `user_input` module.
The `memory_organizer` module will run continuously without activating. 


<div style="text-align: center; margin: 2rem 0;">
    <a href="../running-the-agent" class="indigo-button">
        🚀 Running the Agent
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
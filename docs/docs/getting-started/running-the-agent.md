# 4. Running the Agent

Let's run the assembly of the modules you have created as an agent!

Actually, running the agent is as simple as running a single command. 

First, make sure you have directory structure like this:

```
my_project/
└── agent1
    ├── user_input.py
    ├── chat.py
    └── memory_organizer.py
```
If you have skipped the previous steps, you can go to `examples/coma_interface` directory.

Also, Docker should be running on your machine, as CoMA uses Docker to run the backend services.
```shell
coma backend start
```

Then, run the following command in the `my_project` directory:

```shell
coma run agent1
```

This command will start the agent named `agent1`, which will automatically load the modules you have created in the `agent1` directory. 
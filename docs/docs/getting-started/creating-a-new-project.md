# 2. Creating a New Project

CoMA is designed as project-oriented, meaning that you create modules and an assembly of modules (=agent) within a project. You can make either of the following two styles of projects:
1. **CoMA Interface Project**: you write definitions of modules and run them as a single agent with `coma run` command. This is the simplest way to use CoMA.
2. **Python Interface Project**: you write definitions of modules and agents and run them as more than one agent with `python` command. This is the most flexible way to use CoMA. 

Regardless of the styles of project, you can create a new project simply making a directory. For **Python Interface Project**, this directory stores `python` scripts that define modules and agents. For **CoMA Interface Project**, you need to create one more depth of directory which corresponds to an agent and stores definitions of modules comprising the agent.

For instance, your **CoMA Interface Project** style `sample_project` directory can look like this:

```shell
sample_project/    # Project directory
├── agent1/        # Agent directory
│   ├── module1.py # Defines module1
│   ├── module2.py # Defines module2
│   └── module3.py # Defines module3
└── agent2/
    ├── module1.py
    ├── module2.py
    └── module3.py
```

For **Python Interface Project**, it can look like this:

```shell
sample_project/ # Project directory
├── module1.py  # Defines module1
├── module2.py  # Defines module2
└── module3.py  # Defines module3
├── agent1.py   # Defines an agent that uses module1, module2, and module3
└── agent2.py   # Defines another agent that uses module1, module2, and module3
```

To start with, we will introduce the **CoMA Interface Project** style, which is simpler and more straightforward for beginners. You can skip to the **Python Interface Project** style if you are already familiar with Python and want to use CoMA in a more flexible way.

<div style="text-align: center; margin: 2rem 0;">
    <a href="../creating-modules" class="indigo-button">
        🚀 Creating Modules (CoMA Interface)
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
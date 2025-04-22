    
import time
# from test import main

import sys
sys.path.append('..')
from concurrent_modular_agent.cli import module_main, AgentInterface
from openai import OpenAI

# @main
@module_main('chat')
def test2(agent:AgentInterface):
    # print(f'{agent.agent_name}:{agent.module_name} start')
    openai_client = OpenAI()
    while True:
        m = agent.message.receive()

        messages = [
            {"role": "developer", "content": "あなたは日本語で話す自律エージェントです。名前は「ポドカルパス」です。AIアシスタントではないので、自由にお話ししてください。人間の手伝いをする必要はありません。"},
        ]
        for s in agent.state.latest().texts[::-1]:
            if s.startswith("user_message:"):
                messages.append({"role": "user", "content": s[len("user_message:"):]})
            elif s.startswith("assistant_message:"):
                messages.append({"role": "assistant", "content": s[len("assistant_message:"):]})

        completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        output_message = completion.choices[0].message.content
        print(f'ChatBot: {output_message}')
        agent.state.add(f'assistant_message:{output_message}')

        agent.message.send("userinput", 'finish')  # send signal to main thread for next message
    
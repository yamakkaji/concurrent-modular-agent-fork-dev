# my_project/agent1/chat.py
import concurrent_modular_agent as coma
from openai import OpenAI

@coma.module_main('chat')
def mod_response_to_user(agent: coma.AgentInterface):
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

        messages.append({"role": "assistant", "content": f"{m}"})

        completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )

        output_message = completion.choices[0].message.content
        print(f'ChatBot: {output_message}')
        agent.state.add(f"assistant_message:{output_message}")

        agent.message.send("user_input", 'chat response finished')
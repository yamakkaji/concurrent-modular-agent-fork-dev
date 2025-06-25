# my_project/agent1/memory_organizer.py
import time
import random
import concurrent_modular_agent as coma
from openai import OpenAI

@coma.module_main('memory_organizer')
def mod_organize_memory(agent: coma.AgentInterface):
    openai_client = OpenAI()
    while True:
        time.sleep(100)  # Wait for 100 seconds between memory organization cycles

        messages = [
            {"role": "developer", "content": "You are a module of an autonomous agent. Your job is to organize the memory of the agent. You are expected to organize the memory of the agent in a way that is helpful to recall the past and what the agent had thought. You will be given a list of memory entries from the user and other modules."},
        ]

        organizing_range = random.randint(5, 10)  # Randomly decide how many messages to organize
        recent_states = agent.state.get(max_count=organizing_range).texts[-organizing_range:]

        for s in recent_states:
            if s.startswith("user_message:"):
                messages.append({"role": "user", "content": s[len("user_message:"):]})
            elif s.startswith("assistant_message:"):
                messages.append({"role": "assistant", "content": s[len("assistant_message:"):]})

        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

        output_message = completion.choices[0].message.content
        agent.state.add(f'memory_summary:{output_message}')
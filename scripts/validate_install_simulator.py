import mineland
from mineland.alex.alex_agent import Alex
from mineland.alex.human_agent import HumanAgent


# Create the environment with 2 agents
mland = mineland.make(
    task_id="survival_0.01_days",
    agents_count=2,
)

# Initialize your agents: one human and one ALEX agent
agents = []
human_agent = HumanAgent()
agents.append(human_agent)

alex_agent = ALEX(
    personality='None',
    llm_model_name='gpt-4o',
    vlm_model_name='gpt-4o',
    bot_name='MineflayerBot0',
    temperature=0.1
)
agents.append(alex_agent)

# Reset the environment and get the initial observations
obs = mland.reset()

# Main simulation loop
for i in range(5000):
    if i == 0:
        # First step: use a no-op for all agents
        actions = mineland.Action.no_op(len(agents))
    else:
        actions = []
        # For each agent, call its run() method with its observation.
        # For parameters not used in this simple demo, we pass None or False.
        for idx, agent in enumerate(agents):
            action = agent.run(obs[idx], code_info=None, done=False, task_info={}, verbose=True)
            actions.append(action)
    obs, code_info, event, done, task_info = mland.step(action=actions)
    if done:
        break

mland.close()
print("Validation passed! The simulator is installed correctly.")

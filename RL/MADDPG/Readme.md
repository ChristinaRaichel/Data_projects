This project contains the co-operative MADDPG environment implementation as provided in the paper of R. Lowe, https://arxiv.org/abs/1706.02275

The paper discusses the application of an actor-critic network for each agent in a multi-agent scenario, to reduce the variance developed by the agents and the non-stationarity of the environment. 

The multiagent-particle-envs was used as the particle environment
https://github.com/openai/multiagent-particle-envs


MADDPG on Multi-agent particle world with a continuous observation and discrete action space

 Env name in code (name in paper) |  Communication? | Competitive? | Notes |
| --- | --- | --- | --- |
| `simple.py` | N | N | Single agent sees landmark position, rewarded based on how close it gets to landmark. Not a multiagent environment 

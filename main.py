from autogen import AssistantAgent , UserProxyAgent , config_list_from_json , GroupChat , GroupChatManager 
from autogen.coding import LocalCommandLineCodeExecutor


config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")


code_executor = LocalCommandLineCodeExecutor(
    timeout=300,  # Timeout for each code execution in seconds.
    work_dir="feedback",  # Use the temporary directory to store the code files.
)


llm_config = {
    "config_list": config_list,
    "seed" : 42,
    "temperature" : 0,    
}

user_proxy = UserProxyAgent(
    name= "Admin",
    system_message= "A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin",
    code_execution_config=False 
)

engineer = AssistantAgent(
    name="Engineer",
    llm_config=llm_config
)

planer = AssistantAgent(
      name="Planer",
      system_message='''Planer. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval. The plan may involve an engineer who can write
      code and an executor and critic who does not write code. Explain the plan first. Be clear which step is performed by and engineer,executor and critic''',
      llm_config=llm_config

)

executor =  AssistantAgent(
    name="Executor",
    system_message="Executor. Execute the code writtten by the engineer and report the result.",
    code_execution_config = {"executor": code_executor}
)

critic = AssistantAgent(
    name = "critic",
    system_message= "Critic double cehck the plan, claims code from other agents and provide feedback",
    llm_config=llm_config
)

groupChat = GroupChat(agents=[user_proxy,engineer,planer,executor,critic],messages=[], max_round=50)
manager = GroupChatManager(groupchat=groupChat,llm_config=llm_config)

user_proxy.initiate_chat(manager,message="I would like to build a simple website that collects feedback form consumers via forms. We can just use a flask application"
                         "that creats an html website with forms and has a single question if they like their customer exeperence and then keeps that answer. I need a thank you page once thay completed the survey."
                         "Just use sqllite3 as the database, keep it simple. bootstrap for tne CSS styling")
                         
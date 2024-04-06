from autogen import AssistantAgent , UserProxyAgent , config_list_from_json , GroupChat , GroupChatManager

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")



llm_config = {
    "config_list": config_list,
    "seed" : 42,
    "temperature" : 0,
    "request_timeout":300
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

# planer = AssistantAgent(
#       name="Planer",
#       system_message=''
#       llm_config=llm_config
# )

print(engineer.system_message)
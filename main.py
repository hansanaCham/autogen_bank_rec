import csv
from autogen import AssistantAgent, UserProxyAgent , config_list_from_json ,GroupChat ,GroupChatManager ,ConversableAgent
from autogen.agentchat import register_function

config_list  = config_list_from_json(env_or_file="OAI_CONFIG_LIST")


def get_bank_details() -> list[dict]:
  """
  Reads a csv file with bank details,
  suitable for use with llm.


  Returns:
      list: A list of dictionaries, where each dictionary represents
          a row in the CSV file and the keys are the column names.

  Raises:
      FileNotFoundError: If the CSV file is not found.
  """

  try:
    with open('feedback/files/bank.csv', 'r') as csvfile:
      csv_reader = csv.reader(csvfile)
      data = ""
      for row in csv_reader:
          data += ",".join(row) + "\n"  # Join row elements with commas
      return data.rstrip("\n")  # Remove trailing newline character

  except FileNotFoundError:
      raise FileNotFoundError("CSV file not found")

def get_company_details() -> list[dict]:
  """
  Reads a csv file with company details,
  suitable for use with llm.


  Returns:
      list: A list of dictionaries, where each dictionary represents
          a row in the CSV file and the keys are the column names.

  Raises:
      FileNotFoundError: If the CSV file is not found.
  """

  try:
    with open('feedback/files/company.csv', 'r') as csvfile:
      csv_reader = csv.reader(csvfile)
      data = ""
      for row in csv_reader:
          data += ",".join(row) + "\n"  # Join row elements with commas
      return data.rstrip("\n")  # Remove trailing newline character

  except FileNotFoundError:
      raise FileNotFoundError("CSV file not found")

proxey = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config=False
)

accoutant = ConversableAgent(
  name= "accoutant",
  human_input_mode = '''You are a accountant and you do bank reconsiliations respond outputs only relation the spscific bank rec only when rec is done say TERMINATE''',
  llm_config={"config_list":config_list}                    

)

accoutant_assistant = ConversableAgent(
  name= "assistant_accountant",
  human_input_mode = "only use the functions you have been provided with.",
  llm_config={"config_list":config_list}                    

)


register_function(
  get_bank_details,
  caller=accoutant_assistant,
  executor= proxey,
  description="get bank statement for reconsiliation"
)

register_function(
  get_company_details,
  caller=accoutant_assistant,
  executor= proxey,
  description="get company financial statement for reconsiliation"
)


# print(accoutant.system_message)


groupchat = GroupChat(
        agents=[proxey, accoutant, accoutant_assistant], messages=[], max_round=12
    )


manager = GroupChatManager(
        groupchat=groupchat, llm_config={"config_list": config_list, "timeout": 100, "temperature": 0}
    )


# print(get_bank_details())

proxey.initiate_chat(manager,message=''' Reconsibe bank statement and Company statement use follwong steps
                      1 - get the bank details form assistant_accountant
                      2 - get the bank details form assistant_accountant
                      3 - accountant do the reconsiliation in folling manner :
                        1 - Recods Found in the bank but not in the company (credits)
                        2 - Recods Found in the bank but not in the company (debits)
                        3 - Records found in the compnay but not in the bank (credits)
                        4 - Records found in the compnay but not in the bank (debits)
                        5 - Show the reconsiled report
                        ")'''

)

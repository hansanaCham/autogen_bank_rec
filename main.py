import csv
from autogen import AssistantAgent, UserProxyAgent , config_list_from_json

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
      headers = next(csv_reader)  # Read headers (column names)
      data = []
      for row in csv_reader:
        row_dict = dict(zip(headers, row))  # Create dictionary from row
        data.append(row_dict)
      return data

  except FileNotFoundError:
    raise FileNotFoundError(f"CSV file not found")

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
      headers = next(csv_reader)  # Read headers (column names)
      data = []
      for row in csv_reader:
        row_dict = dict(zip(headers, row))  # Create dictionary from row
        data.append(row_dict)
      return data

  except FileNotFoundError:
    raise FileNotFoundError(f"CSV file not found")  
  

proxey = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config=False
)

accoutant = AssistantAgent(
  name= "accoutant",
  human_input_mode = '''You are a accountant your job is to reconsille bank and company finansial statement use the tools get bank details and 
                      get company details only to get data then reconsile and put mis matching records be below buckets
                      1 - Recods Found in the bank but not in the company (credits)
                      1 - Recods Found in the bank but not in the company (debits)
                      3 - Records found in the compnay but not in the bank (credits)
                      4 - Records found in the compnay but not in the bank (debits)

                      Finally create the reconsiliation report
                      Reply TERMINATE when the task is done.        
                      ''',
  llm_config={"config_list":config_list}                    

)


proxey.register_for_execution(name="get_bank_details")(get_bank_details)
accoutant.register_for_llm(name="get_bank_details",description="get bank statement for reconsiliation")(get_bank_details)


proxey.register_for_execution(name="get_company_details")(get_company_details)
accoutant.register_for_llm(name="get_company_details",description="get company financial statement for reconsiliation")(get_company_details) 


proxey.initiate_chat(accoutant,message="reconsile bank statement and company finaicial statment")



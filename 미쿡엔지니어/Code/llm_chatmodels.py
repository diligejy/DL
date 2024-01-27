from langchain.llms import OpenAI 
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# export OPEN_API_KEY=""

llm = OpenAI()
chat_model = ChatOpenAI()


text = "What would be a good company name for a company that makes colorful socks?"
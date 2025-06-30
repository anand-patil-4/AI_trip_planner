import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


class ConfigLoader:
    def __init__(self):
        print(f"Loading config.....")
        self.config = load_config()

    def __getitem__(self,key):
        return self.config[key]



class ModelLoader(BaseModel):
    model_provider: Literal["groq","openai"]="groq" 
    #Literal is a special type from Python’s typing module (specifically: from typing import Literal) that restricts a variable to specific fixed values.
    config: Optional[ConfigLoader]=Field(default = None, exclude = True)
    #exclude = True - Do not include config in the output when you convert this model to .json() or .dict().

    def model_post_init(self, __context: Any)-> None:
        self.config = ConfigLoader()
        #After ModelLoader is created,It will automatically create a ConfigLoader object and assign it to self.config.

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        print("LLM Loading.....")
        print(f"Loading model from provider : {self.model_provider}")
        if self.model_provider=="groq":
            print("Loading LLM from Groq.....")
            groq_api_key = os.getenv("GROQ_API_KEY")
            model_name = self.config["llm"]["groq"]["model_name"]
            llm = ChatGroq(model = model_name , api_key = groq_api_key)
        elif self.model_provider == "openai":
            print("Loading LLM from OpenAI.....")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            model_name = self.config["llm"]["openai"]["model_name"]
            llm = ChatOpenAI(model = "o4-mini" , api_key = openai_api_key)

        return llm


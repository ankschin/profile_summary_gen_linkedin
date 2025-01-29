import os 
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (create_react_agent, AgentExecutor)
from langchain import hub

from tools.tools import get_profile_url_tavily

def lookup(name:str) -> str:
    #return "https://www.linkedin.com/in/eden-marco/"
    llm= ChatOpenAI(temperature=0, model='gpt-4o-mini')

    template= """given the full name {name_of_person} I want you to get the url link of their profile page.
                Answer should contain only a URL."""
    

    prompt_template= PromptTemplate(template=template, input_variables=['name_of_person'])

    tools_for_agent= [
        Tool(name='Crawl google for linkedin profile page',
             func=get_profile_url_tavily,
             description="useful for when you need to get the linkedin page")
    ]

    react_prompt= hub.pull('hwchase17/react')
    agent= create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    
    executor= AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result= executor.invoke(
        input={"input":prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url= result['output']  
    return linkedin_profile_url


if __name__=="__main__":
    linkedin_url= lookup(name="Sachin Kumar data scientist infosys")
    print(linkedin_url)

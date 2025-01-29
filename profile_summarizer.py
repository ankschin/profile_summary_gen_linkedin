import os
from dotenv import load_dotenv 
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from third_parties.linkedin import scrape_linkedin_profile

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parser import summary_parser, Summary
from typing import Tuple

information="""
Samuel Harris Altman (born April 22, 1985) is an American entrepreneur and investor best known as the chief executive officer of OpenAI since 2019 (he was briefly dismissed and reinstated in November 2023).[1] He is also the chairman of clean energy companies Oklo Inc. and Helion Energy.[2]

Altman is considered to be one of the leading figures of the AI boom.[3][4][5] He dropped out of Stanford University after two years and founded Loopt, a mobile social networking service, raising more than $30 million in venture capital. In 2011, Altman joined Y Combinator, a startup accelerator, and was its president from 2014 to 2019.[6] Altman's net worth was estimated at $1.1 billion in January 2025.[7]
"""

def get_profile_with(name:str) -> Tuple[Summary, str]:
    ## get linkedin url using agent(which uses a tool tavilysearch to search internet for a profile page of a certain name)
    linkedin_url= linkedin_lookup_agent(name=name)

    print(linkedin_url)
    linkedin_data= scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=True)

    print("="*100)
    print(linkedin_data)

    print("*"*100)

    summary_template= """
        given the information {info} about a person, I want you to create:
        1. a short summary
        2. two interesting facts about them
        \n{format_instructions}
        """
    
    summary_prompt_template= PromptTemplate(input_variables=["info"], 
                                            template=summary_template,
                                            partial_variables={"format_instructions": summary_parser.get_format_instructions()})

    llm= ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    chain= summary_prompt_template | llm | summary_parser 

    # result= chain.invoke(input={"info":information})
    result:Summary= chain.invoke(input={"info":linkedin_data})

    print(result)
    print("done!!")
    return result, linkedin_data.get("profile_pic_url")

    

if __name__=="__main__":
    load_dotenv()

    print('hello Langchain')
    
    print(os.environ['OPENAI_API_KEY'])
    
    # linkedin_data= scrape_linkedin_profile(
    #         linkedin_profile_url="https://www.linkedin.com/in/eden-marco/", mock=True
    #     )
    get_profile_with(name="Sachin Kumar data scientist infosys")
    
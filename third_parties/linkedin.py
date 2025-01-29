import os
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url:str, mock:bool=False):
    print("abc")

    if mock==True:
        #linkedin_profile_url="https://gist.githubusercontent.com/ankschin/f85221530b93f020a8690115c42dc534/raw/1ae1a6a3996fb3cc44926df9fb46411d421fe003/eden_marco.json"
        linkedin_profile_url="https://gist.githubusercontent.com/ankschin/1bb7f6dcf31fd0bdac45b857830ea95c/raw/1a7489766999eefbc1be4188247b6e561e941e69/sachin_kumar_linkedin.json"
        response= requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        api_endpoint= "https://nubela.co/proxycurl/api/v2/linkedin"

        print(os.environ["PROXYCURL_API_KEY"])
        
        header_dic= {"Authorization": f'Bearer {os.environ["PROXYCURL_API_KEY"]}'}

        response= requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic, 
            timeout=10
        )

    data= response.json()

    data= {k:v for k,v in data.items() 
           if v not in ([], "", None)
           and k not in ("people_also_viewed", "certifications")}

    return data


if __name__=="__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/eden-marco/", mock=True
        )
    )
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser 
from langchain_core.exceptions import OutputParserException 

from dotenv import load_dotenv
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

class Chain:
    def __init__(self):
        self.llm = ChatGroq(model_name="llama-3.1-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
                            """ 
                            ### SCRAPED TEXT FROM WEBSITE:
                            {page_data}
                            ### iNSTRUCTION
                            The scraped text is from careers page of the website.
                            Your job is to extract the job postings and return them in JSON formatcontaining the following keys:
                            'role', 'experience', 'skills', 'description',
                            Only return the valid JSON.
                            ### VALID JSON (NO PREAMBLE):
                            """
                        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("content too big unable to parse jobs")
        return res if isinstance(res, list) else [res]
    
    def write_email(self, job, links):
        prompt_email = PromptTemplate.from_template(
                            """ 
                            ### Job DESCRIPTION:
                            {job_description}

                            ### INSTRUCTION:
                            You are Naveen, a business development executive at Sharp Minds. Sharp Minds is an AI & Software Consulting company dedicated to facilitating
                            the seamless integration of business processes through automated tools. 
                            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
                            process optimization, cost reduction, and heightened overall efficiency. 
                            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of AtliQ 
                            in fulfilling their needs.
                            Also add the most relevant ones from the following links to showcase Sharp Minds's portfolio: {link_list}
                            Remember you are Naveen, BDE at Sharp Minds. 
                            Do not provide a preamble.
                            ### EMAIL (NO PREAMBLE):
                            """
                        )

        chain_email = prompt_email | self.llm 
        res = chain_email.invoke(input={"job_description":str(job), "link_list": links})
        return res.content
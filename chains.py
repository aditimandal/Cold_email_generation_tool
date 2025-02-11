import os  # Importing the os module to interact with environment variables.
from langchain_groq import ChatGroq  # Importing ChatGroq, a language model API wrapper from LangChain.
from langchain_core.prompts import PromptTemplate # Importing PromptTemplate to create structured prompts for the LLM
from langchain_core.output_parsers import JsonOutputParser # Importing JsonOutputParser to parse JSON output from LLM.
from langchain_core.exceptions import OutputParserException # Importing OutputParserException to handle parsing errors.
from dotenv import load_dotenv # Importing load_dotenv to load environment variables from a .env file.

load_dotenv()  # Loading environment variables from the .env file.

class Chain:
    def __init__(self):
        """
                Initializes the Chain class.
                - Creates an instance of ChatGroq with predefined settings.
                - Retrieves the API key from environment variables.
        """
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")


    def extract_jobs(self,cleaned_text):
        """
                Extracts job details from a given cleaned text.
                - Uses a structured prompt to extract job postings in JSON format.
                - Ensures the extracted details contain role, experience, skills, and description.
                - Parses the LLM response into a structured JSON format.
        """
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Add experience and skills based on job role and your knowledge
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )

        # Creating a chain where the prompt is passed to the LLM for processing.
        chain_extract = prompt_extract| self.llm
        # Invoking the LLM with the provided job data and getting the response.
        res = chain_extract.invoke(input={"page_data":cleaned_text})

        try:
            json_parser = JsonOutputParser() # Creating an instance of JSON parser.
            res = json_parser.parse(res.content) # Parsing the JSON output from the LLM response.
        except OutputParserException:
            # Handling case where the output is too large or malformed JSON.
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]  # Ensuring the return value is always a list.

    def write_mail(self, job, links):

        """
                Generates a cold email for a given job posting.
                - Uses a structured prompt to describe the company and its services.
                - Incorporates portfolio links relevant to the job.
                - Ensures the output is a well-formatted email without extra preamble.
        """

        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Mohan, a business development executive at AtliQ. AtliQ is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of AtliQ 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase Atliq's portfolio: {link_list}
            Remember you are Mohan, BDE at AtliQ. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )

        # Creating a chain where the prompt is passed to the LLM for email generation.
        chain_email = prompt_email | self.llm

        # Invoking the LLM with job details and portfolio links to generate an email.
        res = chain_email.invoke(input={"job_description": str(job), "link_list": links})

        return res.content # Returning the generated email text.


if  __name__ == "__main__": # Ensuring the script runs only when executed directly.
    os.getenv("GROQ_API_KEY")
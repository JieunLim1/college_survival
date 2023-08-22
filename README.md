![CollegeSurvival](image.png)
# college_survival
To assist you survive in college
## QA Generator
QA Generator is an application that utilizes GPT to create questions and checks the answers.

It provides a series of questions, marks the answers, and finally gives you essential questions to review at the final moment before your test. Read more about how it helps your college life here.
https://jieunlim1.github.io//posts/2012/08/blog-post-1/

You can run your own instance of the bot by following the instructions below. 

## Getting Started
This app requires you to have a few different environment variables set. Create a .env file from the .env.template.

OPENAI_API_KEY: Go to OpenAI to generate your own API key.

 * To ensure not to upload or release your API Key, create a .env file by using dotenv to manage your key safely.
   ```bash
   pip install python-dotenv
   from dotenv import load_dotenv
  ```
  * To connect with OpenAI,
    ```bash
      load_dotenv()
      os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_API_KEY")
      chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.9)
    ```
    * Run
    
    `streamlit run (head_file_name).py`






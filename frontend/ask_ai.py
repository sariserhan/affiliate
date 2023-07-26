import os
import time
import openai
import logging
import streamlit as st

from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

openai.organization = "org-KAv10qRlhbdtXmwkdkuET5TP"
openai.api_key = os.getenv("OPENAI_API_KEY")
models = openai.Model.list()

load_dotenv()

def ask_ai(name: str):
    ask_ai_button = st.form_submit_button('Not Sure? Ask AI')
            
    if ask_ai_button:
        logging.info(models.data[0].id)
        my_bar = st.empty()
        progress_text = "Searching... Please wait..."
        my_bar.progress(0, text=progress_text)
        # create a chat completion
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                                    messages=[{"role": "user", 
                                                                "content": os.getenv('AI_ASK').format(name)
                                                              }])

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        my_bar.progress(100, text='Completed')
        time.sleep(1)
        my_bar.empty()
        
        answer = chat_completion.choices[0].message.content.split('\n')
        logging.info(f'--------> AI ANSWER:{answer}')
        buy_paragraph, dont_buy_paragraph = answer[0], answer[2]
        logging.info(f'--------> AI ANSWER BUY:{buy_paragraph}')
        logging.info(f'--------> AI ANSWER DONT BUY:{dont_buy_paragraph}')
        
        st.subheader("You should consider because ✅")
        st.write(buy_paragraph)
        st.write('---')
        st.subheader("You shouldn't because ❌")
        st.write(dont_buy_paragraph)
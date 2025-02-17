import streamlit as st
import pandas as pd
import os
from openai import OpenAI

aiclient = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
st.markdown("<h1 style='text-align: center; color: white;'>NoA Content Generator</h1>", unsafe_allow_html=True)

st.image('LUMENE_LOGO_EMOTIVE_WOL.png',use_container_width=True)

content_type_filter = st.sidebar.selectbox(
    'What category of content would you like to create?',
     ['Email/Newsleter', 'SMS', 'DTC']
     )

content_filter = st.sidebar.selectbox(
    'What category of content would you like to create?',
     ['Offers', 'Product Focused', 'Educational']
     )

country_filter = st.sidebar.selectbox(
    'Which langugage are you working with?',
    ['English', 'Finnish']
    )

if content_filter =='Offers':
    examples = pd.read_csv('offers_examples.csv')
elif content_filter == 'Product Focused':
    examples = pd.read_csv('product_focused_examples.csv')
elif content_filter == 'Educational':
    examples = pd.read_csv('educational_examples.csv')
examples = examples.fillna('empty')

products_filter = st.sidebar.selectbox(
    "Which product(s) would you like to use?",
    examples['Product Name / Category'].unique()
)

if country_filter == 'English':
    language = 'EN'
elif country_filter == 'Finnish':
    language = 'FI'


examples_language_filtered = examples[[f'{language}','Product Name / Category']]
examples_language__product_filtered = examples_language_filtered[examples_language_filtered['Product Name / Category']== products_filter]


examples_for_ai = examples_language__product_filtered[f'{language}'].sum()

st.text(print(examples_for_ai))

text = st.text_area(
        "Enter any additional information here:"
    )

do_it = st.button('Generate Content')

email_parameters =  ["Header: Max 50 characters",
                            "Intro text: Max around 350 characters",
                            "Call to Action as a text, max 25 characters",
                            "Header if needed: Max 28 characters",
                            "Text: Max 180 characters",
                            "Call to Action as a text, max 10 characters",
                            "Inbox subject line under 50 characters (A/B testing with for example offer focused or benefit focused)",
                            "Inbox preview text 40 to 90 characters"]

d2c_prameters = ["Title: max 60 characters",
                "Text: max 280 characters"
                "Call to action button text: max 25 characters"]

def create_email_content():
    completion = aiclient.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are creating a {content_filter} for a Lumene, a Swedish brand."},
            {
                
                "role":"user",
                "content":f"The audience you are providing this content for to speaks {country_filter}'"

            },
            {
                "role":"user",
                "content":f"Here are some examples of tone of voice: {examples_for_ai}, if this is empty disregarde these instructions"

            },
            {
                "role":"user",
                "content":f"The parameters of are as follows:{email_parameters}"
                            
            },
             {
                "role":"user",
                "content":"Remove the names of the parameters"
                            
            },
            {
                "role":"user",
                "content": f"Here are some additional conditions for the {content_filter}: {text}"

            },
            {
                "role":"user",
                "content":f"return a {content_filter}"

            },

        ],
    temperature=0.01
    )

    return completion.choices[0].message.content

def create_sms_content():
    completion = aiclient.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are creating a {content_filter} for a Lumene, a Swedish brand."},
            {
                
                "role":"user",
                "content":f"The audience you are providing this content for to speaks {country_filter}'"

            },
            {
                "role":"user",
                "content":f"Here are some examples of tone of voice: {examples_for_ai}, if this is empty disregarde these instructions"

            },
            {
                "role":"user",
                "content":"For SMS we have a limited budget so if we could also use it to write as short as possible but engaging copy"
                            
            },
            {
                "role":"user",
                "content": f"Here are some additional conditions for the {content_filter}: {text}"

            },
            {
                "role":"user",
                "content":f"return a only the {content_filter} and no other gpt output with 160 maximum characters"

            },

        ],
    temperature=0.01
    )

    return completion.choices[0].message.content

def create_d2c_content():
    completion = aiclient.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are creating a banner advertisement for a Lumene, a Swedish brand."},
            {
                
                "role":"user",
                "content":f"The audience you are providing this content for to speaks {country_filter}'"

            },
            {
                "role":"user",
                "content":f"Here are some examples of tone of voice: {examples_for_ai}, if this is empty disregarde these instructions"

            },
            {
                "role":"user",
                "content":f"The parameters of are as follows:{d2c_prameters}"
                            
            },
             {
                "role":"user",
                "content":"Remove the names of the parameters"
                            
            },
            {
                "role":"user",
                "content": f"Here are some additional conditions for the {content_filter}: {text}"

            },
            {
                "role":"user",
                "content":f"return a {content_filter}"

            },

        ],
    temperature=0.01
    )

    return completion.choices[0].message.content


if do_it and content_type_filter=='Email/Newsleter':
    content = create_email_content()
elif do_it and content_type_filter == 'SMS':
    content = create_sms_content()
elif do_it and content_type_filter == 'DTC':
    content = create_d2c_content()

st.write(content)
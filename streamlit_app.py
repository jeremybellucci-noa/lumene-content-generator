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

product_description_filter = st.sidebar.selectbox(
    "Which type of product would you like to sell?",
    ['Ranges', 'Best Sellers']
)

if country_filter == 'English' and product_description_filter == 'Ranges':
    products = pd.read_csv('lumene_product_descriptions_ranges_en.csv')
elif country_filter == 'English' and product_description_filter == 'Best Sellers':
    products = pd.read_csv('lumene_product_descriptions_best_sellers_en.csv')
elif country_filter == 'Finnish' and product_description_filter == 'Best Sellers':
    products = pd.read_csv('lumene_product_descriptions_best_sellers_fi.csv')
elif country_filter == 'Finnish' and product_description_filter == 'Ranges':
    products = pd.read_csv('lumene_product_descriptions_ranges_fi.csv')


if content_filter =='Offers':
    examples = pd.read_csv('offers_examples.csv')
elif content_filter == 'Product Focused':
    examples = pd.read_csv('product_focused_examples.csv')
elif content_filter == 'Educational':
    examples = pd.read_csv('educational_examples.csv')
examples = examples.fillna('empty')

products_filter = st.sidebar.selectbox(
    "Which product(s) would you like to use for tone of voice?",
    examples['Product Name / Category'].unique()
)

specific_product_filter = st.sidebar.selectbox(
    "Which specific product would you like to sell?",
    products['Product'].unique()
)

if country_filter == 'English':
    language = 'EN'
elif country_filter == 'Finnish':
    language = 'FI'


examples_language_filtered = examples[[f'{language}','Product Name / Category']]
examples_language__product_filtered = examples_language_filtered[examples_language_filtered['Product Name / Category']== products_filter]


examples_for_ai = examples_language__product_filtered[f'{language}'].sum()

text = st.text_area(
        "Enter any additional information here:"
    )

do_it = st.button('Generate Content')

copy_parameters = ["Be Warm: DO Keep it personal, kind and human: we are a brand that cares.  When relevant, add an emotional layer to messaging. Examples: Radiance Suits You, Beauty That Cares, Glow With Confidence, Skin-Loving Formula",
                   "Be Expressive: Use emotional and sensorial language: describe how it feels. Examples: That Feel-Good GlowWild Volume, Untamed Energy, All-round Radiance, Beauty Sleep, Reinvented, Shake Up The Glow, Feel Wild… Strong… Radiant… Feel you.",
                    "Be Fresh: Use current, inspiring language. Always give a positive spin and use language that focuses on the desired outcome. Examples: Enter Your Ageless Era, Naturally Supercharged Finish, Bounce Back With Bloom, Illuminate The Everyday, Your Skin, In Full Bloom",
                    "Be Authentic: Use truthful language that inspires trust. Relate to the audience with openness. Use language that is straightforward and easy to understand. Examples: Let Your True Skin Glow, Skin-Loving Beauty That Really Works, We Believe In Beauty That Comes Naturally",
                    "Be Inclusive: Use welcoming, people-focused language. When relevant, use collective phrasing to signal a sense of community: ‘we’, ‘our’, and ‘us’. Examples: For Every Shade of Us, Beauty Has No Age Limit, Express Yourself, However It Comes To You, Join Our Skin-Loving Beauty Community",
                    "Own our Nordic Nature wih this Lexicon: Dive Into Hydration, Light Charged, Nordic Actives, ‘Nordic Nature is like us: a little bit wild, inherently powerful’, Nordic Nature Knows Best, Supercharged, Water Fresh, Wild-Crafted Ingredients, Wild By Name, Wild By Nature, Wild Forces, Wild Nordic Nature"

]

email_parameters =  ["Header: Max 50 characters",
                            "Intro text: Max around 350 characters",
                            "Call to Action as a text, max 25 characters",
                            "Header if needed: Max 28 characters",
                            "Text: Max 180 characters",
                            "Call to Action as a text, max 10 characters",
                            "Two Inbox subject lines under 50 characters for A/B testing with for example offer focused or benefit focused",
                            "Inbox preview text 40 to 90 characters"]

d2c_prameters = ["Title: max 60 characters",
                "Text: max 280 characters"
                "Call to action button text: max 25 characters"]


product_description = products[products['Product'] == specific_product_filter]['Description']

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
                "content":f"Encorporate this product {specific_product_filter} description: {product_description}"

            },
            {
                "role":"user",
                "content":f"When writing this copy, use these instructions: {copy_parameters}"

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
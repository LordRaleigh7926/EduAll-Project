import google.generativeai as genai
import json


# Loading the JSON configuration file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)


API_KEY = config['API_Key']
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

def get_gemini_response(text):
    response = model.generate_content(text)
    return response.text



def get_response_initial(topic:str, time_constraint:str = "None", sub_topic:str = "None"):


    link_prompt = f'''
    I want to learn this - {topic}.
    Only provide me links which help me to learn this.
    Make sure the links work and there aren't any spaces in them.
    Also provide links to YouTube videos.
    Make sure the links work and give the right website.
    Also format the links so that by clicking them I get to the site.
    FORMAT ALL THE LINKS IN MARKDOWN SO THAT WHEN I CLICK THEM I GET TO THE LINKS.
    Make sure each link in different and no links are the same.
    '''
    
    roadmap_prompt = f'''Provide me a roadmap to learn - {topic}.
    Give me a detailed roadmap.
    Make it very very detailed.
    Also mention how much time I should spend on each phase.
    I am in a time contraint of {time_constraint}.
    Also make sure that along with all the topics necessary you also include these topics - {sub_topic} in the learning roadmap.
    '''

    book_prompt = f'''
    I want to learn this - {topic}.
    Only provide me book names which help me to learn this.
    Only provide names of books and nothing else.
    Mention the author's name. 
    '''

    quote1 = get_gemini_response(f"Give me a single quotes on {topic}. Include the author if you can. Do not tell me that you cannot. ")
    
    quote2 = get_gemini_response(f"Give me a single quotes on {topic}. Include the author if you can. Do not tell me that you cannot. Do not give me this one - {quote1}")

    links = get_gemini_response(link_prompt)

    roadmap = get_gemini_response(roadmap_prompt)
    
    books = get_gemini_response(book_prompt)



    return roadmap, books, links, quote1, quote2


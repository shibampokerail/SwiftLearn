import json
import openai
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


def save_mind_map_image(summary_data):
    G = nx.DiGraph()
    G.add_nodes_from(summary_data['Nodes'])

    for edge, attribute in zip(summary_data['Edges'], summary_data['Attributes']):
        G.add_edge(*edge, label=attribute)

    pos = nx.spring_layout(G, seed=42, k=1) 
    plt.figure(figsize=(16, 10))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=12, font_color='black',
            font_weight='bold', edge_color='gray', linewidths=0.5, edgecolors='black', alpha=0.7, arrowsize=20)

    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title('Mind Map', fontsize=16)
    plt.tight_layout()
    plt.savefig('static/mind_map.png', format='png')  
    # plt.show()
    return summary_data


openai.api_key = '<api_key>'
messages = [ {"role": "system", "content":
              "You are a intelligent assistant."} ]

def generate_mind_map_json(transcript):
    # message = input("User : ")
    if transcript=="":
        raise Exception("No transcript was given")
    mind_map_message = '''
    #loading the summary text
    summary_text = """
    The passage describes the city of Metropolis. It notes that the population has steadily grown over the past decade, currently reaching around 500,000 residents. The local economy has also flourished, with 10% annual growth in the last five years. The city is characterized by modern skyscrapers and green spaces. Metropolis has a high literacy rate of 95% and its university attracts students from across the country for its diverse academic programs. Central Park, a popular destination, sees an average of 1,000 visitors daily and provides recreation for both locals and tourists.
    """
    
    #creating summary data in json format from the summary_text above
    summary_data = {
        'Nodes': ['Metropolis', 'Population', 'Economy', 'Cityscape', 'Education', 'Recreation'],
        'Edges': [
            ('Metropolis', 'Population'),
            ('Metropolis', 'Economy'),
            ('Metropolis', 'Cityscape'),
            ('Metropolis', 'Education'),
            ('Metropolis', 'Recreation')
        ],
        'Attributes': [
            '500,000 residents',
            '10% annual growth',
            'modern skyscrapers and green spaces',
            '95% literacy rate, university',
            'Central Park, 1,000 visitors daily'
        ],
        summary:
        "Metropolis, a thriving city, has seen consistent population growth, reaching 500,000 residents. The robust local economy boasts a 10% annual growth, complemented by modern architecture, green spaces, and a 95% literacy rate. The city's university attracts students nationwide, while Central Park remains a daily destination for recreation."
    }
    This was an example of how to create a summary_data from summary_text in json format now give me the summary_data in json format, Include exactly 5 Nodes, 5 Edges, and 5 Attributes, and a summary section in the json data where summary will have a short (4 sentences max) summary, if summary_text=
    '''
    message = mind_map_message+transcript
    # print(transcript)
    print(message)
    if message:
        try:
            messages.append(
                {"role": "user", "content": message},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-1106", messages=messages, response_format={"type": "json_object"}
            )
        except:
            message = mind_map_message + transcript[:len(transcript/2)]
            messages.append(
                {"role": "user", "content": message},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-1106", messages=messages, response_format={"type": "json_object"}
            )

    reply = chat.choices[0].message.content
    print(f"{reply}")


    try:
        json_data = reply
        return_data = save_mind_map_image(json_data)
    except:
        json_data = json.loads(reply)
        return_data = save_mind_map_image(json_data)

    return return_data


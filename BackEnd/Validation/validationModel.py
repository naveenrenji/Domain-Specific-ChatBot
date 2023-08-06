from transformers import pipeline
import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)


#nlp = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
nlp = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

context = """
Introduce a washing machine that features a built-in garment sharing and swapping hub  allowing users to connect and exchange clothes with others worldwide.
Develop a washing machine with a built-in fabric pattern generator  creating unique patterns and designs on clothes during the wash cycle.
Design a washing machine that incorporates a built-in garment lifecycle tracker  informing users about the environmental impact of their clothing choices.
Create a washing machine with a built-in fabric temperature therapy feature  offering heat or cold treatments to clothes for specific therapeutic purposes.
Introduce a washing machine that features a built-in fabric upcycling program  guiding users to repurpose old clothes into new and fashionable garments.
Develop a washing machine with a built-in fabric scent customization system  allowing users to choose and mix scents for personalized laundry aromas.
Design a washing machine that incorporates a built-in garment sharing and rental network  connecting users worldwide to borrow and lend clothes.
Create a washing machine with a built-in fabric memory restoration function  reviving clothes' memory of their original shape and fit during the wash cycle.
Introduce a washing machine that features a built-in fabric carbon footprint tracker  measuring and displaying the environmental impact of each wash cycle.
Develop a washing machine with a built-in fabric relaxation mode  simulating gentle movements to relax and de-stress clothes during the wash cycle.
Design a washing machine that incorporates a built-in garment upcycling workshop  providing tools and resources for users to transform old clothes into new creations.
Create a washing machine with a built-in fabric color customization system  allowing users to change the color of their clothes during the wash cycle.
Introduce a washing machine that features a built-in garment donation tracking platform  connecting users with the journey and impact of their donated clothes.
Develop a washing machine with a built-in fabric mood-enhancing feature  infusing clothes with scents and textures to uplift the wearer's mood.
Design a washing machine that incorporates a built-in garment fit adjuster  using gentle stretching and reshaping techniques to modify the fit of clothes.
Create a washing machine with a built-in fabric wellness program  applying treatments and textures to promote physical and emotional well-being through clothing.
Introduce a washing machine that features a built-in garment exchange marketplace  facilitating direct transactions and swaps between users for preloved clothes.
Develop a washing machine with a built-in fabric emotion synchronization system  aligning the garment's properties with the wearer's emotional state during the wash cycle.
Design a washing machine that incorporates a built-in garment sustainability rating  providing users with information about the environmental impact of their clothing choices.
Create a washing machine with a built-in fabric energy channeling feature  infusing clothes with positive energy or intentions during the wash cycle.
Introduce a washing machine that features a built-in garment repair and alteration workshop  equipping users with tools and resources to mend and modify their clothes.
Develop a washing machine with a built-in fabric self-expression mode  allowing users to create personalized patterns and designs directly on their clothes during the wash cycle.
Design a washing machine that incorporates a built-in garment material traceability system  providing users with information about the origin and production process of their clothes.
Create a washing machine with a built-in fabric mood analyzer  detecting the wearer's emotional state based on clothing and recommending appropriate care treatments during the wash cycle.
Introduce a washing machine that features a built-in garment sharing and recycling ecosystem  connecting users to share  recycle  and repurpose clothes within their community.
Develop a washing machine with a built-in fabric energy cleansing feature  using special treatments to remove negative energy or emotions from clothes during the wash cycle.
Design a washing machine that incorporates a built-in garment eco-certification program  identifying and promoting clothes made with sustainable materials and practices.
Create a washing machine with a built-in fabric aura enhancer  infusing clothes with positive vibrations and energy to support the wearer's well-being during the wash cycle.
Introduce a washing machine that features a built-in garment storytelling platform  allowing users to share the stories and memories associated with their clothes.
Develop a washing machine with a built-in fabric emotion synchronization feature  adjusting the garment's properties to align with the wearer's emotional state and enhance their mood during the wash cycle.
Design a washing machine that incorporates a built-in garment circular economy platform  connecting users to repair  reuse  resell  and recycle clothes within a global network.
Create a washing machine with a built-in fabric intention setting feature  enabling users to infuse their clothes with positive intentions and affirmations during the wash cycle.
Introduce a washing machine that features a built-in garment carbon offset program  allowing users to contribute to offsetting the environmental impact of their clothing choices.
Develop a washing machine with a built-in fabric self-care mode  providing treatments and textures that promote relaxation  rejuvenation  and self-care through clothing during the wash cycle.
Design a washing machine that incorporates a built-in garment emotional history log  capturing and visualizing the emotional journey and memories associated with each piece of clothing.
Create a washing machine with a built-in fabric energy alignment feature  infusing clothes with harmonizing energies or frequencies to support the wearer's well-being and balance during the wash cycle.
Introduce a washing machine that features a built-in garment emotional connection hub  allowing users to connect with the emotional stories and experiences shared by others through their clothes.
Develop a washing machine with a built-in fabric intention activation feature  amplifying and activating the positive intentions and affirmations infused in clothes during the wash cycle.
Design a washing machine that incorporates a built-in garment circular fashion marketplace  enabling users to buy  sell  rent  and exchange clothes within a community dedicated to sustainable fashion.
Create a washing machine with a built-in fabric energy harmonization mode  balancing and aligning the energetic frequencies of clothes to promote a sense of calm and well-being for the wearer during the wash cycle.
Introduce a washing machine that features a built-in garment emotional healing program  using specially designed treatments and textures to support emotional healing and growth through clothing.
Develop a washing machine with a built-in fabric manifestation feature  utilizing the power of intention and energy to manifest desired outcomes and experiences through clothes during the wash cycle.
Design a washing machine that incorporates a built-in garment transparency platform  providing users with detailed information about the social and environmental impact of their clothing choices.
Create a washing machine with a built-in fabric energy purification function  clearing and removing negative or stagnant energies from clothes to promote a sense of vitality and positivity for the wearer during the wash cycle.
Introduce a washing machine that features a built-in garment emotional connection network  enabling users to connect and share emotional experiences associated with their clothes  fostering empathy and human connection.
Develop a washing machine with a built-in fabric energy infusion capability  allowing users to infuse clothes with specific energetic qualities  such as peace  abundance  or creativity  to support the wearer's desired intentions and experiences during the wash cycle.
"""

questions = ["a machine that uses solar and clean energy", "a mountain that is made of gold"]
results = []

# Process the predefined questions
for question in questions:
    answer = nlp(question=question, context=context)['answer']
    results.append(f"{answer}")


# Create a pandas DataFrame for visualisation
df = pd.DataFrame(list(zip(questions, results)), columns=["Question", "Answer"])
print(df)

# Interactive chat session
while True:
    user_query = input("\nPlease enter your question: ")
    
    if user_query.lower() == 'end':
        print("Ending the session.")
        break
    
    answer = nlp(question=user_query, context=context)['answer']
    print(f"Answer: {answer}")
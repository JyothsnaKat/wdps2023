from ctransformers import AutoModelForCausalLM
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import wikipedia

# data/word_vectors/glove.6B.100d.zip
# Step 1: Get the answer from llama
def query_language_model(textA):
    repository="TheBloke/Llama-2-7B-GGUF"
    model_file="llama-2-7b.Q4_K_M.gguf"
    llm = AutoModelForCausalLM.from_pretrained(repository, model_file=model_file, model_type="llama")

    textB = llm(textA)
    # print(f"Text returned by the language model (B)(llama 2, 70B): {textB}\n")
    return textB

    
# Step 2: Extract answer, yes or no or entity


def extract_wikipedia_title_and_pattern(text):
    # Check if the word "Wikipedia" is in the text
    # task: wikipedia entity link
    return None

def extract_yes_no_answer(text):
    # Load the spaCy English model
    nlp = spacy.load("en_core_web_sm")

    # Process the input text
    doc = nlp(text)

    # Define a list of positive and negative keywords
    positive_keywords = ["yes", "true", "correct", "affirmative", "not false"]
    negative_keywords = ["no", "false", "incorrect", "negative", "not", "not true"]

    # Check for the presence of positive or negative keywords in the processed text
    for token in doc:
        if token.text.lower() in positive_keywords:
            return "yes"
        elif token.text.lower() in negative_keywords:
            return "no"

    # If no keywords are found, return None
    return None

# Example text
text = "" #task pass the illama extracted text

wikipedia_title, search_pattern = extract_wikipedia_title_and_pattern(text)

# Check if the extracted title is a Wikipedia entity
if wikipedia_title:
    print(wikipedia_title)
else:
    
# Extract yes/no answer
    extracted_answer = extract_yes_no_answer(text.lower())

# Print the result
    if extracted_answer is not None:
        print(f"Extracted answer: {extracted_answer}")
    else:
        print("No yes/no answer was found.")    
# Step 3: Fact checking
# def fact_checking(textB):
#     return checked_fact, confidence

def get_wikipedia_content(title):
    wikipedia.set_lang("en")
    try:
        page = wikipedia.page(title)
        return page.content
    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation by selecting the first option
        page = wikipedia.page(e.options[0])
        return page.content
    except wikipedia.exceptions.PageError:
        print(f"Error: Wikipedia page for '{title}' not found.")
        return None

def calculate_cosine_similarity(text1, text2):
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    similarity = cosine_similarity(vectors)
    return similarity[0, 1]

# Example extracted data from the Llama model
llama_extracted_data =  "" #task: illama extracted data
wikipedia_title = "Managua" #task: pass entity extracted  

# Get content from Wikipedia
wikipedia_content = get_wikipedia_content(wikipedia_title)

if wikipedia_content:
    # Calculate cosine similarity
    similarity_score = calculate_cosine_similarity(llama_extracted_data, wikipedia_content)

    # Define a threshold for similarity
    similarity_threshold = 0.7

    # Compare the similarity score with the threshold
    if similarity_score >= similarity_threshold:
        print("Correctness of the answer: Correct")
        print(similarity_score)
    else:
        print("Correctness of the answer: Incorrect")
        print(similarity_score)
else:
    print("Error: Unable to retrieve information from Wikipedia.")

def get_wikipedia_content(title):
    wikipedia.set_lang("en")
    try:
        page = wikipedia.page(title)
        return page.content
    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation by selecting the first option
        page = wikipedia.page(e.options[0])
        return page.content
    except wikipedia.exceptions.PageError:
        print(f"Error: Wikipedia page for '{title}' not found.")
        return None

def calculate_cosine_similarity(text1, text2):
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    similarity = cosine_similarity(vectors)
    return similarity[0, 1]

# Example extracted data from the Llama model
llama_extracted_data = "Yes, Managua is the capital city of Nicaragua. It is located in the southwestern part of the country and is home to many important government buildings and institutions, including the President's office and the National Assembly. The city has a population of over one million people and is known for its vibrant cultural scene, historic landmarks, and beautiful natural surroundings."
wikipedia_title = "Managua"

# Get content from Wikipedia
wikipedia_content = get_wikipedia_content(wikipedia_title)

if wikipedia_content:
    # Calculate cosine similarity
    similarity_score = calculate_cosine_similarity(llama_extracted_data, wikipedia_content)

    # Define a threshold for similarity
    similarity_threshold = 0.7

    # Compare the similarity score with the threshold
    if similarity_score >= similarity_threshold:
        print("Correctness of the answer: Correct")
        print(similarity_score)
    else:
        print("Correctness of the answer: Incorrect")
        print(similarity_score)
else:
    print("Error: Unable to retrieve information from Wikipedia.")        
        

# Step 4: Using spacy to recognize entities
def extract_entities(textA, textB):
    # Load the spaCy English model
    nlp = spacy.load("en_core_web_sm")
    # Combine the two texts
    combined_text = textA + " " + textB
    # Process the combined text
    doc = nlp(combined_text)
    # Extract entities and their Wikipedia URLs
    entities = set()  # Using set to avoid duplicates
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC", "ORG"]:  # Consider entities like geopolitical entities, locations, and organizations
            normalized_text = ent.text.capitalize()   # Normalize the text to first letter uppercase and others lowercase
            entities.add((normalized_text, f"https://en.wikipedia.org/wiki/{normalized_text.replace(' ', '_')}"))
    # Converting the set back to a list to return it
    # print("Extracting")
    return list(entities)


# Process a txt as input and format the output

def process_input(input_line):
    print("Processing input")
    question_id, question_textA = input_line.split("\t")
    question_textB = query_language_model(question_textA)
    entities = extract_entities(question_textA, question_textB)
    # correctness = check_correctness(extracted_answer)
    # return question_id, question_textB, extracted_answer, correctness, entities
    # print("Processing input finished")
    return question_id, question_textB, entities

# def format_output(question_id, response, extracted_answer, correctness, entities):
def format_output(question_id, question_textB, entities):
    output = []
    output.append(f"{question_id}\tR\"{question_textB}\"")
    # output.append(f"{question_id}\tA\"{extracted_answer}\"")
    # output.append(f"{question_id}\tC\"{correctness}\"")
    for entity, url in entities:
        output.append(f"{question_id}\tE\"{entity}\"\t\"{url}\"")
    print("Formatting")
    return "\n".join(output)

# Main execution
input_file = "/app/project/question_lists.txt"
with open(input_file, "r") as file:
    for line in file:
        print("Reading file")
        # question_id, question_textB, extracted_answer, correctness, entities = process_input(line.strip())
        # formatted_output = format_output(question_id, question_textB, extracted_answer, correctness, entities)
        question_id, question_textB, entities = process_input(line.strip())
        formatted_output = format_output(question_id, question_textB, entities)
    print(formatted_output)


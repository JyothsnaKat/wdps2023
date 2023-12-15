from ctransformers import AutoModelForCausalLM
import spacy
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

# Step 3: Fact checking
# def fact_checking(textB):
#     return checked_fact, confidence

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


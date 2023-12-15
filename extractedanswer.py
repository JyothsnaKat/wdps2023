import spacy

def extract_wikipedia_title_and_pattern(text):
    # Check if the word "Wikipedia" is in the text
    if "Wikipedia" in text:
        text = "Wikipedia entity"
        return text, None
    else:
        return None, None

def is_wikipedia_entity(entity):
    # Placeholder function; you can implement a more sophisticated check here
    # For simplicity, it checks if the entity is in lowercase (as Wikipedia URLs often are)
    return entity and entity.islower()

def extract_yes_no_answer(text):
    # Load the spaCy English model
    nlp = spacy.load("en_core_web_sm")

    # Process the input text
    doc = nlp(text)

    # Define a list of positive and negative keywords
    positive_keywords = ["yes", "true", "correct", "affirmative"]
    negative_keywords = ["no", "false", "incorrect", "negative", "not"]

    # Check for the presence of positive or negative keywords in the processed text
    for token in doc:
        if token.text.lower() in positive_keywords:
            return "yes"
        elif token.text.lower() in negative_keywords:
            return "no"

    # If no keywords are found, return None
    return None

# Example text
text = "Most people think Managua is the capital of Nicaragua. However, Managua is not the capital of Nicaragua.The capital of Nicaragua is Managua. The capital of Nicaragua is Managua. Managua is the capital of Nicaragua. The capita"

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



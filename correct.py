from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import wikipedia

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
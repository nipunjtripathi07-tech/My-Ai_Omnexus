import pyttsx3
import wikipedia
from duckduckgo_search import DDGS
import datetime
from transformers import pipeline

nlp = pipeline("text2text-generation", model="google/flan-t5-small")

while True:
    cmd = input("Query: ").lower()
    if 'exit' in cmd: break

    # Extract & Merge
    try:
        src = wikipedia.summary(cmd, sentences=1)
    except:
        src = ""
    with DDGS() as ddgs:
        src += " ".join([r['body'] for r in ddgs.text(cmd, max_results=2)])

    # Transform & Speak
    res = nlp(f"Summarize: {src}")[0]['generated_text']
    print(f"Omnexus: {res}");
    pyttsx3.speak(res)

    # 1. MOVE INPUT INSIDE THE LOOP
    command = input("Omnexus here, how can I assist you today: ").lower()

    if 'time' in command:
        x = datetime.now().strftime("%H:%M:%S")
        y = f"Current time is {x}"
        print(f"Omnexus: {y}")
        speak(y)


    def fast_ddgs_search():
        """
        Takes user input, searches DDGS, and displays results.
        """
        query = input("Enter search query (or 'q' to quit): ")
        if query.lower() == 'q':
            return False

        print(f"\nSearching for: {query}...\n")

        # Perform the search
        with DDGS() as ddgs:
            # 'max_results' limits results for speed
            results = ddgs.text(query, max_results=3)

            if not results:
                print("No results found.")
            else:
                for i, result in enumerate(results, 1):
                    print(f"{i}. {result['title']}")
                    print(f"   {result['href']}")
                    print(f"   {result['body'][:100]}...\n") # Snippet preview
        return True

    if __name__ == "__main__":
        while True:
            if not fast_ddgs_search():
                break
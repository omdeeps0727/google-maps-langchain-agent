from dotenv import load_dotenv
from agents.maps_agent import GoogleMapsAgent

load_dotenv()

agent = GoogleMapsAgent()

queries = [
    "Where is the Eiffel Tower?",
    "How do I get from Paris to London?",
    "Find coffee shops near Times Square",
    "What's the address of the White House?",
    "Find hotels within 1km of the Sydney Opera House"
]

for query in queries:
    print(f"User: {query}")
    response = agent.run(query)
    print(f"Agent: {response}\n")
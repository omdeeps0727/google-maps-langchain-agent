from dotenv import load_dotenv
from agents.maps_agent import GoogleMapsAgent

def main():
    load_dotenv()
    agent = GoogleMapsAgent()
    
    print("Google Maps LangChain Agent")
    print("Type 'exit' to quit\n")
    
    while True:
        query = input("You: ")
        if query.lower() == 'exit':
            break
            
        response = agent.run(query)
        print(f"Agent: {response}\n")

if __name__ == "__main__":
    main()
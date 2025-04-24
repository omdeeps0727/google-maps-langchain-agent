from langchain.agents import AgentExecutor, Tool, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from .tools import (
    get_place_details,
    get_directions,
    find_nearby_places,
    geocode_address
)

class GoogleMapsAgent:
    def __init__(self, model="gpt-3.5-turbo"):
        self.llm = ChatOpenAI(model=model, 
        temperature=0,
        max_retries=2,  # Add retries
    request_timeout=30  # Add timeout
    )
        self.tools = self._setup_tools()
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True,input_key="input"  # Explicit input key
        )
        self.agent = self._create_agent()
    
    def _setup_tools(self):
        return [
            Tool(
                name="GetPlaceDetails",
                func=get_place_details,
                description="Useful for getting details about a specific place or business."
            ),
            Tool(
                name="GetDirections",
                func=get_directions,
                description="Useful for getting directions between two locations."
            ),
            Tool(
                name="FindNearbyPlaces",
                func=find_nearby_places,
                description="Useful for finding places near a location."
            ),
            Tool(
                name="GeocodeAddress",
                func=geocode_address,
                description="Useful for converting addresses to geographic coordinates."
            )
        ]
    
    def _create_agent(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant that interacts with Google Maps. Use the provided tools to answer user questions about locations, directions, and places."),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad")
        ])
        
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, memory=self.memory, verbose=True)
    
    def run(self, query):
        return self.agent.invoke({"input": query})["output"]
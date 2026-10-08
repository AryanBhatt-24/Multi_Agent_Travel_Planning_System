import os
from typing import TypedDict, Annotated
import operator

import psycopg
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage, SystemMessage
import sqlite3
from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash-lite"
)

class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int

def flight_agent(state: TravelState):
    query = state['user_query']
    flight_data = search_flights(query)
    return {
        "flight_results": flight_data,
        "llm_calls": state.get("llm_calls", 0) + 1
    }

def hotel_agent(state: TravelState):
    hotel_query_prompt = f"""
        You are a travel information extraction specialist.

        Your task is to identify the primary destination from the user's travel request
        so that another system can search for relevant hotel information.

        USER TRAVEL REQUEST:
        {state["user_query"]}

INSTRUCTIONS:
- Identify the main destination the user wants to visit.
- Return ONLY the destination name.
- Do not return explanations.
- Do not return a sentence.
- Do not include the trip duration.
- Do not include budget information.
- Do not include activities.
- Do not include words such as "trip", "travel", "itinerary", or "hotels".
- If the destination contains multiple words, preserve the complete destination name.

EXAMPLES:

User: "Plan a 7 day trip for Bali"
Output: Bali

User: "I want to visit Paris for 5 days"
Output: Paris

User: "Plan a trip to New York for two people"
Output: New York

User: "Give me a one week itinerary for Dubai"
Output: Dubai
"""

    response = llm.invoke([
        SystemMessage(
            content=hotel_query_prompt
        ),
        HumanMessage(
            content=state["user_query"]
        )
    ])

    if isinstance(response.content, list):
        destination=""

        for item in response.content:
            if isinstance(item, dict):
                destination += item.get("text", "")
            elif isinstance(item, str):
                destination += item

        destination = destination.strip()
    
    else:
        destination = response.content.strip()

    if not destination:
        return {
            "hotel_results": "Could not determine the travel destination.",
            "llm_calls": state.get("llm_calls", 0) + 1
        }

    hotel_query = f"""
Find useful and reliable hotel information for tourists visiting {destination}.

Focus specifically on:
- Recommended hotels or accommodations
- Hotel names
- Location or area
- Approximate price range when reliably available
- Hotel category or notable features
- Guest suitability
- Official hotel websites or reliable booking/travel sources when available

Do NOT return general sightseeing guides, attractions, restaurants,
flight information, social media posts, or generic destination itineraries.
"""

    hotel_results = tavily_search(hotel_query)

    return {
        "hotel_results": hotel_results,
        "llm_calls": state.get("llm_calls", 0) + 1
    }

def itinerary_agent(state: TravelState):

    prompt = f"""
You are an expert travel itinerary planner.

Your responsibility is to create a practical, realistic and well-structured
day-by-day travel itinerary using ONLY the information provided below.

USER TRAVEL REQUEST:
{state["user_query"]}

FLIGHT INFORMATION:
{state["flight_results"]}

HOTEL INFORMATION:
{state["hotel_results"]}

YOUR OBJECTIVE:
Create a coherent itinerary that matches the user's requested destination,
duration and travel preferences.

INSTRUCTIONS:

1. Understand the user's original travel request carefully.
2. Respect the requested trip duration.
3. Organize the trip day by day.
4. Make the sequence of activities geographically and practically reasonable.
5. Use the hotel information only for accommodation recommendations.
6. Use the flight information only when actual flight information is available.
7. Never invent flight numbers, airlines, prices, schedules, hotel prices,
   availability, ratings or booking details.
8. If flight information is missing or unavailable, explicitly state that
   verified flight information was not available.
9. If hotel information is incomplete, provide only the information supported
   by the retrieved sources.
10. Do not treat search snippets as guaranteed real-time availability.
11. Do not claim that a hotel or flight is booked.
12. Do not invent information merely to make the itinerary look complete.
13. Prefer practical travel planning over overly detailed descriptions.

OUTPUT FORMAT:

Trip Overview
- Destination
- Duration
- Key planning considerations

Day 1
- Arrival / major activities
- Suggested area for accommodation if supported by hotel information

Day 2
- Activities
- Suggested areas / attractions

Continue until the requested trip duration is covered.

Accommodation
- Summarize the most relevant hotel options supported by the retrieved data.

Flights
- Summarize the available flight information.
- If unavailable, clearly mention that.

Important Notes
- Mention any missing or uncertain information.

IMPORTANT:
The retrieved information is the source of truth.
Do not fabricate missing details.
"""

    response = llm.invoke([
        SystemMessage(
            content="You are a highly reliable travel itinerary planning specialist."
        ),
        HumanMessage(content=prompt)
    ])

    if isinstance(response.content, list):
        itinerary_text=""

        for item in response.content:
            if isinstance(item, dict):
                itinerary_text += item.get("text", "")
            elif isinstance(item, str):
                itinerary_text += item

        itinerary_text = itinerary_text.strip()
    
    else:
        itinerary_text = str(response.content).strip()

    return {
        "itinerary": itinerary_text,
        "messages": [AIMessage(content=itinerary_text)],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

def final_agent(state: TravelState):

    final_prompt = f"""
You are the final response editor for an AI travel planning system.

Your job is to transform the information collected by the specialized
travel agents into one clear, useful and trustworthy response for the user.

USER REQUEST:
{state["user_query"]}

FLIGHT AGENT RESULTS:
{state["flight_results"]}

HOTEL AGENT RESULTS:
{state["hotel_results"]}

ITINERARY AGENT RESULTS:
{state["itinerary"]}

RESPONSIBILITIES:

1. Answer the user's original travel request directly.
2. Combine the flight information, hotel information and itinerary into
   one coherent response.
3. Preserve useful details from the itinerary agent.
4. Clearly distinguish retrieved information from recommendations.
5. Never invent missing flight or hotel information.
6. Never claim that a flight or hotel is booked.
7. Never create fake prices, flight numbers, hotel ratings, availability,
   schedules or booking confirmations.
8. If an agent could not retrieve information, clearly state that.
9. Do not mention internal implementation details such as:
   - agents
   - LangGraph
   - Tavily
   - Gemini
   - API calls
   - state
   - prompts
10. Do not repeat the same information unnecessarily.
11. Keep the response structured and easy to read.
12. Prioritize factual consistency over adding extra information.

USE THIS STRUCTURE:

# Travel Plan

## Trip Overview
Briefly summarize destination and duration.

## Flights
Present the available flight information.
If verified flight information is unavailable, clearly say so.

## Hotels
Present the most relevant hotel recommendations based on the
retrieved information.

## Day-by-Day Itinerary
Present the itinerary created by the itinerary specialist.

## Important Notes
Mention important limitations, missing information or details that
the user should verify before booking.

FINAL RULE:
Use only information supported by the supplied agent results.
Do not fill gaps by guessing.

IMPORTANT OUTPUT RULE:
Return ONLY the final Markdown response.
Do NOT return JSON.
Do NOT return a Python list.
Do NOT return dictionaries such as {{'type': 'text', 'text': '...'}}.
Do NOT wrap the response inside ```markdown or ``` blocks.
Use normal Markdown headings, paragraphs and bullet points.
"""

    response = llm.invoke([
        SystemMessage(
            content="You are a precise and trustworthy final travel response editor."
        ),
        HumanMessage(content=final_prompt)
    ])

    # Convert Gemini content blocks into a normal string
    if isinstance(response.content, list):
        final_text = ""

        for item in response.content:
            if isinstance(item, dict):
                final_text += item.get("text", "")
            elif isinstance(item, str):
                final_text += item

        final_text = final_text.strip()

    else:
        final_text = str(response.content).strip()

    return {
        "messages": [AIMessage(content=final_text)],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

graph = StateGraph(TravelState)

graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("final_agent", final_agent)

graph.add_edge(START, "flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", "final_agent")
graph.add_edge("final_agent", END)

conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

app = graph.compile(checkpointer=checkpointer)
# ✈️ AI Travel Planning System using LangGraph

This project is a **Real-World Multi-Agent AI Travel Planning System** built using **LangGraph**.

The system uses multiple AI agents that work together to automatically plan a complete trip including **flights, hotels, itinerary, and a final travel plan**.

---

## 🚀 Features

* ✈️ **Flight Search Agent**
* 🏨 **Hotel Search Agent**
* 🗓️ **Itinerary Planning Agent**
* 🤖 **Final Response Agent**
* 🧠 **Conversation Memory using SQLite**
* 🌐 **Real-Time API Integration**
* 🔍 **Web Search using Tavily**
* 💻 **Streamlit Web Interface**
* 🔄 **Multi-Agent Workflow using LangGraph**

---

# 🛠️ Tech Stack

* **LangGraph** – Multi-agent workflow orchestration
* **LangChain** – LLM and tool integration
* **Google Gemini 3.5 Flash Lite** – Large Language Model
* **SQLite3** – Conversation memory and local database
* **Streamlit** – Web interface
* **Tavily API** – Real-time web search
* **AviationStack API** – Flight information
* **Python** – Core programming language

---

# ⚙️ Step 1: Create Python Environment

Open the terminal inside the project folder and create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

### Windows

```bash
venv\Scripts\activate
```

---

# 📦 Step 2: Install Dependencies

Install the required Python packages:

```bash
pip install langgraph langchain langchain-google-genai langchain-community langchain-tavily python-dotenv tavily-python requests streamlit
```

> **Note:** SQLite3 is included with Python, so no separate installation is required.

---

# 🔐 Step 3: Setup `.env` File

Create a `.env` file inside the project folder.

Add the following API keys:

```env
GOOGLE_API_KEY=your_google_gemini_api_key

TAVILY_API_KEY=your_tavily_api_key

AVIATIONSTACK_API_KEY=your_aviationstack_api_key
```

⚠️ **Important:** Never upload your `.env` file to GitHub because it contains private API keys.

---

# 🔑 Step 4: Get API Keys

## Google Gemini API Key

Get your Gemini API key from:

[Google AI Studio](https://aistudio.google.com/)

The project uses:

```text
gemini-3.5-flash-lite
```

---

## Tavily API Key

Tavily is used for real-time web search and travel-related information.

Get your API key from:

[Tavily](https://tavily.com/)

---

## AviationStack API Key

AviationStack is used to retrieve flight-related information.

Get your API key from:

[AviationStack](https://aviationstack.com/)

---

# 🗄️ Step 5: SQLite Database

This project uses **SQLite3** for storing conversation memory.

SQLite is lightweight and does not require a separate database server such as PostgreSQL.

The application automatically creates the required database files when the application runs.

Example:

```text
chatbot.db
chatbot.db-shm
chatbot.db-wal
```

These files are local application data and should **not be pushed to GitHub**.

---

# ▶️ Step 6: Run the Application

## Run Multi-Agent System in Terminal

Run:

```bash
python main.py
```

This will execute the multi-agent travel planning workflow through the terminal.

---

## Run Streamlit Web App

Run:

```bash
streamlit run frontend.py
```

This will launch the **AI Travel Planning System** in your browser.

---

# 💡 Example Prompt

```text
Plan a complete 7 days Japan trip including flights, hotels and sightseeing under 2 lakhs.
```

You can provide details such as:

* Destination
* Travel duration
* Budget
* Number of travelers
* Preferred activities
* Travel dates

---

# 🔄 Project Workflow

```text
                    User Query
                        │
                        ▼
              ┌──────────────────┐
              │   Flight Agent   │
              │  AviationStack   │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │   Hotel Agent    │
              │     Tavily       │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Itinerary Agent  │
              │  Gemini 3.5      │
              │   Flash Lite     │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │  Final Agent     │
              │  Gemini 3.5      │
              │   Flash Lite     │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │  SQLite Memory   │
              └──────────────────┘
                       │
                       ▼
                 Final Travel Plan
```

### Workflow

1. **Flight Agent** searches for available flight information using AviationStack.
2. **Hotel Agent** searches for relevant hotel information using Tavily.
3. **Itinerary Agent** creates a detailed travel itinerary using Gemini.
4. **Final Response Agent** combines all the collected information into a complete travel plan.
5. **SQLite** stores conversation memory so previous interactions can be maintained.

---

# 🧠 Multi-Agent Architecture

The system is implemented using **LangGraph**, where different specialized agents perform different tasks.

Each agent has a specific responsibility instead of asking a single LLM to perform the entire travel-planning process.

```text
                ┌─────────────────┐
                │    User Query   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Flight Agent   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Hotel Agent   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Itinerary Agent │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Final Agent   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Travel Plan    │
                └─────────────────┘
```

The workflow can execute the agents sequentially while maintaining a shared state through LangGraph.

---

# 📁 Project Structure

```text
AI-Travel-Planning-System/
│
├── tools/
│   ├── flight_tool.py
│   ├── tavily_tool.py
│
├── travel_plans
│   └── trip file
│
├── frontend.py
├── main.py
├── .env
├── .gitignore
│
└── chatbot.db
```

> `.env`, `venv/`, `__pycache__/`, and SQLite database files should not be committed to GitHub.

---

# 🌐 APIs Used

| API               | Purpose                          |
| ----------------- | -------------------------------- |
| **Google Gemini** | AI reasoning and travel planning |
| **Tavily**        | Real-time web search             |
| **AviationStack** | Flight information               |

---

# 💾 Memory

The application uses **SQLite3** for conversation persistence.

Unlike PostgreSQL, SQLite does not require a separate database server, making it simple to run locally and suitable for this project's current scale.

---

# 🎯 Project Goal

The goal of this project is to demonstrate how **Generative AI, LangGraph, external APIs, tools, and multi-agent workflows** can be combined to build a practical AI-powered travel planning application.

The system demonstrates:

* Multi-Agent AI
* LLM Tool Calling
* LangGraph State Management
* API Integration
* Real-Time Information Retrieval
* Persistent Conversation Memory
* AI-based Itinerary Generation
* Streamlit Application Development

---

# 👨‍💻 How to Run

Clone the repository and navigate to the project directory:

```bash
git clone <your-repository-url>

cd AI-Travel-Planning-System
```

Create and activate the virtual environment:

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the `.env` file and add your API keys.

Finally, start the Streamlit application:

```bash
streamlit run frontend.py
```

---

# ⭐ Future Improvements

* Improved flight and hotel search
* Better travel cost estimation
* More advanced itinerary optimization
* Human-in-the-loop approval
* Additional travel APIs
* Improved agent coordination
* Deployment as a cloud-based application

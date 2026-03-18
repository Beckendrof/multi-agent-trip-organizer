### Project Title: Multi-Agent Trip Concierge & Logic Supervisor

**The Problem**
Organizing group travel—like a weekend stargazing trip to Joshua Tree with flatmates—generates conflicting data. You have messy, unstructured group chats ("Let's blast music and grill at midnight!"), strict venue regulations ("10 PM noise curfew; no open fires"), and complex budget constraints. Parsing this manually leads to logistical disasters and rule violations. 

**The Solution**
This project deploys a supervised multi-agent AI system. It autonomously ingests unstructured travel data, cross-references proposed plans against RAG-retrieved venue rules, and uses a dedicated "Conflict Resolution Agent" to catch and fix logical errors before finalizing the itinerary.

---

### System Architecture 

1. **Data Ingestion & RAG:** The user uploads a venue rule PDF (e.g., Airbnb rules, National Park guidelines) and a text export of the group chat. The PDF is chunked, vectorized, and stored in a Pinecone database.
2. **Agent 1 (The Logistical Parser):** Extracts the proposed attendee list, arrival times, dietary restrictions, and desired activities from the chaotic chat log.
3. **Agent 2 (The Financial Estimator):** Parses the group's stated budget from the chat and compares it against expected costs for the proposed activities.
4. **Agent 3 (The Conflict Resolution Supervisor):** The core intelligence of the app. It consumes the outputs of Agents 1 & 2 and queries the Pinecone Vector DB (RAG) to audit the plan. 
    * *Example Catch:* If Agent 1 schedules a campfire at 11 PM, but Agent 3's RAG query reveals a strict fire ban, Agent 3 flags the conflict and automatically regenerates three compliant alternatives (e.g., "Shift to indoor fireplace" or "Stargazing without fire").
5. **API Delivery:** The validated, conflict-free itinerary and budget breakdown are served via a serverless RESTful API to the frontend.

---

### The Tech Stack

* **Backend:** Python (FastAPI) / Node.js (Express)
* **AI Orchestration:** LangGraph (Python) or LangChain (Node) for cyclic multi-agent routing.
* **LLM:** OpenAI GPT-4o via REST API.
* **Vector Database (RAG):** Pinecone for low-latency semantic search of venue constraints.
* **Infrastructure:** Serverless deployment on AWS Lambda / API Gateway, managed via Git/GitHub Actions.
* **Frontend UI:** React for a clean, interactive user interface.

---

### Why This Architecture? (Notes for Reviewers)

* **Multi-Agent Supervision:** This project demonstrates how to build reliable, production-ready AI. By isolating the "planning" and "auditing" functions into distinct agents, the system drastically reduces LLM hallucinations.
* **Deterministic Guardrails via RAG:** The AI does not rely on its foundational training data for venue rules; it is strictly grounded in the user-uploaded documentation, ensuring high-fidelity compliance.
* **REST API Mastery:** The system is completely decoupled. The multi-agent backend operates as an independent REST API that can be consumed by any frontend or downstream CRM/automation tool. 

---

### Local Setup & Testing

1. Clone the repository and run `pip install -r requirements.txt`.
2. Add your OpenAI and Pinecone API keys to the `.env` file.
3. Run `python main.py` to initialize the backend API.
4. Run `npm run dev` to launch the UI.
5. Upload the sample `joshua_tree_chat_log.txt` and `campground_rules.pdf` provided in the `/tests` folder. Watch the Supervisor Agent catch the midnight campfire violation in real-time!

***

### 🌐 Live Demo

[Try the Multi-Agent Trip Concierge (Demo)](https://multi-agent-trip-organizer.vercel.app/)
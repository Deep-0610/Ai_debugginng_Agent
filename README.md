🚀 AI Debugging & Code Review Agent

Transforming raw code into resilient, high-performance software with automated AI insights.
Welcome to the Ai_debugginng_Agent repository! This project delivers an automated code review and debugging system that analyzes changes, identifies subtle bug patterns, highlights performance bottlenecks, and recommends context-aware patches before code reaches production.
✨ Key Capabilities
🤖 Automated Code Architecture Review: Analyzes commits and pull requests against modern coding standards, architectural best practices, and security guidelines.
🐞 Deep Error & Stack Trace Analysis: Parses complex stack traces, runtime exceptions, and log outputs to deliver clear root-cause explanations and actionable solutions.
⚡ Intelligent Patch Generation: Constructs clean, ready-to-merge refactoring proposals and bug fixes directly tailored to your existing implementation.
📦 Frictionless Containerized Environment: Fully equipped with a .devcontainer configuration, ensuring consistent execution and fast onboarding across developers and environments.
📂 Repository Overview



Plaintext
Ai_debugginng_Agent/
├── .devcontainer/        # Standardized containerized development workspace
├── ai-code-reviewer/     # Core logic, LLM prompt templates, and execution engines
└── README.md             # Repository documentation and setup guide


🛠️ Environment Prerequisites
To run and extend this agent locally, ensure you have the following installed:
Docker Desktop: Required to run isolated development containers.
VS Code: Recommended IDE, paired with the Dev Containers extension.
Runtime: Python 3.10+ or Node.js (depending on your preferred backend service setup).
API Credentials: An active API key for your chosen LLM engine (e.g., Google Gemini, OpenAI, or Anthropic).
⚡ Quick Start Guide
1. Clone the Repository



Bash
git clone https://github.com/Deep-0610/Ai_debugginng_Agent.git
cd Ai_debugginng_Agent


2. Launch in DevContainer (Recommended)
Open the repository folder inside Visual Studio Code.
Press Ctrl + Shift + P (or Cmd + Shift + P on macOS).
Search for and select: Dev Containers: Reopen in Container.
3. Environment Configuration
Create a .env file inside the root directory to securely pass your environment parameters:



Code snippet
# LLM Provider Credentials
AI_PROVIDER_API_KEY=your_actual_api_key_here
LLM_MODEL_NAME=gemini-2.5-flash

# Execution Settings
LOG_LEVEL=DEBUG
ENVIRONMENT=development


🏃 Running the Agent
Navigate into the core service module to execute local tests or run full directory analyses:



Bash
cd ai-code-reviewer

# Example: Run standard code review on target files
python main.py --target ./path/to/source_code --output report.json


🤝 Contributing
We welcome community feedback, pull requests, and feature requests!
Explore active open issues on the Issues board.
Fork the repository and create your feature branch:
Bash
git checkout -b feature/awesome-new-enhancement


Commit your updates and open a Pull Request against the main branch.
📜 License
Distributed under the MIT License. See LICENSE for more information.

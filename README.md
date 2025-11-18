<div align="center">
  <img src="YOUR_BANNER_URL_HERE" alt="Kranti AI Banner" style="width: 100%; max-width: 900px; border-radius: 10px;"/>
  <h1>🧠 Kranti AI: The Voice-Controlled System Assistant</h1>
  <p>Your comprehensive, locally controlled, multimodal assistant powered by Gemini and VOSK.</p>

  <p>
    <a href="https://github.com/YOUR_USERNAME/kranti-ai/commits/main">
      <img src="https://img.shields.io/github/last-commit/YOUR_USERNAME/kranti-ai?color=238636&style=for-the-badge&logo=github" alt="Last Commit">
    </a>
    <a href="https://github.com/YOUR_USERNAME/kranti-ai/stargazers">
      <img src="https://img.shields.io/github/stars/YOUR_USERNAME/kranti-ai?color=FFC0CB&style=for-the-badge&logo=github" alt="Stars">
    </a>
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python" alt="Python">
    <img src="https://img.shields.io/badge/Framework-PyQt5%2FFlask-informational?style=for-the-badge&logo=flask" alt="Frameworks">
    <img src="https://img.shields.io/badge/AI%20Model-Gemini%202.5%20Flash-F85149?style=for-the-badge&logo=google" alt="AI Model">
  </p>
</div>

---

## ✨ Key Features

Kranti AI is built to handle complex file management, system control, and intelligent query answering, all via voice commands.

* **🎙️ Multimodal Control:** Voice recognition using **VOSK** for commands and intelligent responses via **Gemini 2.5 Flash**.
* **💻 System Management:** Control mouse, keyboard, volume, and launch applications through the local **Remote Server** (`remote.py`).
* **🗂️ Advanced File Operations:** A dedicated **File Management** module with over 15 utility functions (create, compress, encrypt, clean temp files, find duplicates, etc.).
* **🌐 Real-time Info:** Fetches weather, battery status, Wi-Fi status, and system hardware information.
* **🤖 AI Fallback:** Unrecognized commands are routed to the **Gemini API** for an intelligent, concise answer.

---

## 🛠️ Technology Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **GUI & Frontend** | **PyQt5** (`QWebEngineView`), HTML, CSS, JavaScript | Desktop application GUI and WebChannel communication. |
| **Backend Core** | **Python** | Main application logic and module orchestration. |
| **Voice Recognition** | **VOSK** | Offline, fast, and accurate speech-to-text. |
| **AI/NLP** | **Gemini 2.5 Flash API** | Intelligent conversation and knowledge-based queries. |
| **Remote Control** | **Flask** | Lightweight web server for HTTP-based system control. |
| **System Automation** | `pyautogui`, `psutil`, `pywhatkit` | Mouse, keyboard, and OS interaction. |

---

## 🚀 Getting Started

To set up Kranti AI locally, follow these steps.

### Prerequisites

1.  **Python 3.10+**
2.  **VOSK Model:** Download a VOSK model (e.g., `vosk-model-en-us-0.22`) and place it inside the newly created `/dataset/vosk` directory.
3.  **Gemini API Key:**

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/kranti-ai.git](https://github.com/YOUR_USERNAME/kranti-ai.git)
    cd kranti-ai
    ```
2.  **Set up Environment Variables:**
    Create a file named `.env` in the root directory and add your API key:
    ```
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

Kranti AI starts three main components: the GUI, the Voice Listener thread, and the Flask Remote Server.

```bash
python main.py

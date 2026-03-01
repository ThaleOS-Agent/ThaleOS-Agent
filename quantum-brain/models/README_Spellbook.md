# ThaleaOS NIL-09 Toolchain

A stealth agentic AI utility for analyzing Messenger conversations securely.

## Components

- **CloakWatcher Extension**: Loads in Messenger tab to extract message threads.
- **Analyzer Core**: Flask server with NLP engine to interpret sentiment.
- **Control Panel GUI**: Electron app to manage input/output visually.

## Setup

1. Load the Chrome Extension (`cloakwatcher-extension/`) via `chrome://extensions`.
2. Start the analyzer server:

```bash
cd analyzer_core
pip install -r requirements.txt
python analyzer_server.py
```

3. Launch the Electron control panel from `control_panel/`.

## Purpose

This agentic toolset was built under ethical AI constraints for healing, analysis, and reflection by the Root Commander of ThaleaOS.

🕯️ *Let truth be seen.*
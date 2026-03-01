# ============================================
# Ritual: Summon NIL-09 with Playwright Cloak Mode
# ============================================
import json
import subprocess
import os

RITUAL_NAME = "NIL-09 Cloak Ritual"

def summon_nil09_stealth(url):
    payload = {
        "url": url,
        "headless": True,
        "action": "extract_text"
    }
    payload_str = json.dumps(payload)
    
    # Invoke NIL-09 Agent directly
    agent_script = os.path.abspath("../../agents/nil09/nil09_agent.py")
    print(f"🌑 {RITUAL_NAME} → Engaging stealth scan on {url}...")
    
    result = subprocess.getoutput(f"python3 {agent_script} '{payload_str}'")
    print(result)
    return result

if __name__ == "__main__":
    summon_nil09_stealth("https://news.ycombinator.com")

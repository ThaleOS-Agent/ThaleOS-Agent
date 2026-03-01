# ============================================
# Spell Engine – Cloak Spell
# ============================================
import json, subprocess, os

INCANTATIONS = os.path.join(os.path.dirname(__file__), "../incantations.json")

def cast(spell_name):
    with open(INCANTATIONS) as f:
        spells = json.load(f)

    if spell_name not in spells:
        return f"❌ Spell '{spell_name}' not found."

    spell = spells[spell_name]
    agent = spell["agent"]
    payload = json.dumps(spell["payload"])

    print(f"🔮 Casting spell '{spell_name}' → Invoking {agent}")
    result = subprocess.getoutput(f"python3 ../core/orchestrator.py {agent} '{payload}'")
    return result

if __name__ == "__main__":
    print(cast("cloak_revenant"))

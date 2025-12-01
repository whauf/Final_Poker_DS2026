import re

def parse_simple_input(text: str):
    """
    Universal parser for simple poker input.

    Examples it accepts:
    - 'As Kd'
    - 'As Kd middle'
    - 'As Kd | Ts 9s 2d'
    - 'As Kd | Ts 9s 2d Jh | 3 players'
    - 'I have As Kd on Ts 9s 2d vs 3 players'
    """

    t = text.strip().lower()

    # -----------------------------------------
    # 1. Extract all playing cards (As, Td, 9c)
    # -----------------------------------------
    cards = re.findall(r"[akqjt2-9][shdc]", t)
    cards = [c.upper() for c in cards]

    hero = cards[:2]
    board = cards[2:]

    # -----------------------------------------
    # 2. Extract number of players (optional)
    # -----------------------------------------
    players = 1
    m = re.search(r"(\d+)\s*players?", t)
    if m:
        players = int(m.group(1))
    else:
        # Also detect short formats like: "/ 3"
        m2 = re.search(r"/\s*(\d+)", t)
        if m2:
            players = int(m2.group(1))

    # -----------------------------------------
    # 3. Detect preflop position
    # -----------------------------------------
    position = "middle"
    positions = ["early", "middle", "late", "button", "cutoff", "utg", "hijack"]
    for p in positions:
        if p in t:
            position = p
            break

    # -----------------------------------------
    # 4. Determine the street by board card count
    # -----------------------------------------
    if len(board) == 0:
        street = "preflop"
    elif len(board) == 3:
        street = "flop"
    elif len(board) == 4:
        street = "turn"
    elif len(board) == 5:
        street = "river"
    else:
        street = "unknown"

    return {
        "street": street,
        "hero_cards": hero,
        "board": board,
        "position": position,
        "opponents": players
    }
import re

def parse_facing_bets(text: str) -> dict:
    """
    Parse phrases like:
    - 'UTG raises to 3bb'
    - 'CO 3bet to 12bb'
    - 'BTN opens 2.5x'
    """

    if not text or not text.strip():
        return {"action": None, "aggressor": None, "size": None}

    text = text.lower().strip()

    # Detect position
    positions = ["utg","hj","lj","mp","co","btn","sb","bb"]
    aggressor = None
    for pos in positions:
        if text.startswith(pos):
            aggressor = pos.upper()
            break

    # Detect raise size
    # Allow "10", "10bb", "10x", "10.5"
    size_match = re.search(r"(\d+(\.\d+)?)\s*(bb|x)?", text)
    size = float(size_match.group(1)) if size_match else None

    # Classify action type
    if "3bet" in text or "3-bet" in text:
        action = "raise"  # Convert 3bet to raise
    elif "raises" in text or "raise" in text:
        action = "raise"
    elif "bets" in text or "bet" in text:
        action = "raise"  # Convert preflop bet to raise (no betting preflop in NLHE)
    elif "open" in text:
        action = "raise"  # Convert open to raise
    else:
        action = None  # Return None instead of "unknown" for no action

    return {
        "action": action,
        "aggressor": aggressor,
        "size": size
    }

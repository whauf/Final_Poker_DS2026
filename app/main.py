# app/main.py

from typing import Optional

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse

from .models import AdvisorRequest, PreflopState, StreetState
from .decision import decide_preflop, decide_postflop, parse_villain_action
from .sim import equity_vs_random_opponents
from .azure_blob import download_text_if_exists
from .utils import parse_facing_bets   # <-- RESTORED

import json
import os
import eval7



app = FastAPI(
    title="Poker Advisor",
    version="5.0",
    description="Multi-street Poker Advisor with eval7-safe parsing",
)


# ----------------------------------------------------
# HELPERS (server-side parsing)
# ----------------------------------------------------
VALID_RANKS = set("23456789TJQKA")
VALID_SUITS = set("cdhs")


def normalize_card(card: str) -> str:
    """
    Normalize a single card like 'as' / 'AS' / 'Ah' / 'AD' → 'As', 'Ah', etc.
    """
    card = card.strip()
    if len(card) < 2:
        raise ValueError(f"Card '{card}' too short")

    rank = card[0].upper()
    suit = card[1].lower()

    if rank not in VALID_RANKS:
        raise ValueError(f"Invalid rank in card '{card}'")
    if suit not in VALID_SUITS:
        raise ValueError(f"Invalid suit in card '{card}' (must be one of c,d,h,s)")

    return rank + suit


def parse_two_card_hand(hand_str: str) -> list[str]:
    """
    Parse something like:
      'As Kd'
      'as kd'
      'ASKD'
      'as kd xx' (takes first two)
    into ['As','Kd'].
    """
    text = hand_str.replace(",", " ").strip()
    parts = text.split()

    if len(parts) == 1 and len(parts[0]) == 4:
        # "ASKd" style: first two chars, last two chars
        cards_raw = [parts[0][:2], parts[0][2:]]
    elif len(parts) >= 2:
        cards_raw = [parts[0], parts[1]]
    else:
        raise HTTPException(400, "Could not parse hand. Example: As Kd")

    try:
        return [normalize_card(c) for c in cards_raw]
    except ValueError as e:
        raise HTTPException(400, f"Invalid hero hand: {e}") from e


def parse_board(board_str: str, min_cards: int = 3, max_cards: int = 5) -> list[str]:
    """
    Parse a board string like 'Ah Ad Ac', 'Ah Ad Ac 2c', 'Ah Ad Ac 2c 9h' into normalized cards.
    """
    text = (board_str or "").replace(",", " ").strip()
    if not text:
        raise HTTPException(400, "Board cards are required for postflop advice.")

    raw_tokens = text.split()
    try:
        cards = [normalize_card(t) for t in raw_tokens]
    except ValueError as e:
        raise HTTPException(400, f"Invalid board cards: {e}") from e

    if not (min_cards <= len(cards) <= max_cards):
        raise HTTPException(
            400,
            f"Board must contain between {min_cards} and {max_cards} cards; got {len(cards)}.",
        )

    return cards


# ----------------------------------------------------
# HEALTH CHECK
# ----------------------------------------------------
@app.get("/health")
def health():
    return {"ok": True}


# ----------------------------------------------------
# INDEX (HTML UI)
# ----------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def index():
    file_path = os.path.join(
        os.path.dirname(__file__),
        "templates",
        "index.html",
    )
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        return HTMLResponse(
            f"<h1>index.html not found</h1><p>{str(e)}</p>",
            status_code=500,
        )


# ----------------------------------------------------
# PREFLOP — used by HTML UI
# ----------------------------------------------------
@app.post("/simple-advise")
def simple_advise(
    hand: str = Form(...),
    stack: Optional[str] = Form(None),
    position: Optional[str] = Form(None),
    players: Optional[str] = Form(None),
    facing_bets: Optional[str] = Form(None),
):
    # Defaults for empty fields
    try:
        stack_val = int(stack) if stack not in ("", None) else 100
    except Exception:
        stack_val = 100

    try:
        players_val = int(players) if players not in ("", None) else 6
    except Exception:
        players_val = 6

    position_val = position or "middle"
    facing_bets_val = parse_facing_bets(facing_bets or "")


    # Hero cards
    hero_cards = parse_two_card_hand(hand)

    pst = PreflopState(
        hero_cards=hero_cards,
        position=position_val,
        facing_bets=facing_bets_val
    ) 



    result = decide_preflop(pst)

    result["hero_cards"] = hero_cards
    result["stack_bb"] = stack_val

    result["players"] = players_val
    return result


# ----------------------------------------------------
# POSTFLOP (FLOP / TURN / RIVER) — used by HTML UI
# ----------------------------------------------------
# ----------------------------------------------------
# STREET ADVISOR (Flop / Turn / River)
# ----------------------------------------------------
@app.post("/street-advise")
async def street_advise(request: Request):
    form = await request.form()
    print("RAW FORM:", dict(form))

    raw_hero = (form.get("hero_cards") or "").strip()
    raw_board = (form.get("board") or "").strip()
    raw_action = (form.get("action") or "").strip()
    opponents_raw = form.get("opponents") or "1"

    hero_parts = [normalize_card(t) for t in raw_hero.split()]
    board_parts = [normalize_card(t) for t in raw_board.split()]

    opponents = int(opponents_raw)

    # Postflop action parser
    from .decision import parse_villain_action
    facing_action = parse_villain_action(raw_action)

    print("DEBUG FACING:", facing_action)


    sst = StreetState(
        hero_cards=hero_parts,
        board=board_parts,
        street=("flop" if len(board_parts) == 3 else "turn" if len(board_parts) == 4 else "river"),
        pot=float(form.get("pot") or 0),
        opponents=opponents,
        facing_action=facing_action,
        position=form.get("position") or None
)


    return decide_postflop(sst)



# ----------------------------------------------------
# PROGRAMMATIC JSON ADVISOR (for API / scripts)
# ----------------------------------------------------
@app.post("/advisor")
def advisor(req: AdvisorRequest):
    board = req.board or []
    n = len(board)

    if n == 0:
        pst = PreflopState(
            hero_cards=req.hero_cards,
            position=req.position or "middle",
        )
        return decide_preflop(pst)

    elif n in (3, 4, 5):
        sst = StreetState(
            hero_cards=req.hero_cards,
            board=req.board,
            opponents=req.opponents,
        )
        return decide_postflop(sst)

    else:
        raise HTTPException(400, "Board must contain 0, 3, 4, or 5 cards.")


# ----------------------------------------------------
# SUPPORT ENDPOINTS
# ----------------------------------------------------
@app.post("/preflop")
def preflop_json(req: PreflopState):
    return decide_preflop(req)


@app.post("/street")
def street_json(req: StreetState):
    return decide_postflop(req)


@app.post("/equity")
def equity(req: StreetState):
    eqh, eqv, tie, dist = equity_vs_random_opponents(req.hero_cards, req.board)
    return {
        "hero_equity": eqh,
        "villain_equity": eqv,
        "tie": tie,
        "hand_distribution": dist,
    }


@app.get("/ranges")
def get_ranges():
    data = download_text_if_exists("data/ranges/preflop_live_fullring_100bb.json")
    if not data:
        return {"error": "Could not load ranges from Azure."}
    return json.loads(data)

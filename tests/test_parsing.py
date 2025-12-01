import pytest
from app.utils import parse_facing_bets

def test_parse_facing_bets_co_bets_10():
    # The feature requested: "CO bets 10"
    result = parse_facing_bets("CO bets 10")
    assert result["aggressor"] == "CO"
    assert result["action"] == "bet"
    assert result["size"] == 10.0

def test_parse_facing_bets_standard():
    # Existing functionality
    result = parse_facing_bets("UTG raises to 3bb")
    assert result["aggressor"] == "UTG"
    assert result["action"] == "raise"
    assert result["size"] == 3.0

def test_parse_facing_bets_variations():
    # "bets" vs "bet", no "bb"
    result = parse_facing_bets("BTN bets 2.5")
    assert result["aggressor"] == "BTN"
    assert result["action"] == "bet"
    assert result["size"] == 2.5

def test_parse_facing_bets_opens():
    result = parse_facing_bets("SB opens 3x")
    assert result["aggressor"] == "SB"
    assert result["action"] == "open"
    assert result["size"] == 3.0

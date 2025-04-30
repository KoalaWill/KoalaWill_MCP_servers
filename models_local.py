from PokerNow.models import GameState as BaseGameState, PlayerInfo as BasePlayerInfo

class PlayerInfo(BasePlayerInfo):
    def to_dict(self):
        return {
            "name": self.name,
            "stack": self.stack,
            "bet_value": self.bet_value,
            "cards": self.cards,
            "status": self.status.name if hasattr(self.status, "name") else str(self.status),
            "hand_message": self.hand_message
        }

class GameState(BaseGameState):
    def to_dict(self):
        return {
            "game_type": self.game_type,
            "pot_size": self.pot_size,
            "community_cards": self.community_cards,
            "players": [PlayerInfo(**vars(p)).to_dict() for p in self.players],
            "dealer_position": self.dealer_position,
            "current_player": self.current_player,
            "blinds": self.blinds,
            "winners": self.winners,
            "is_your_turn": self.is_your_turn
        }

from roulette import RouletteGame, RouletteHistory
import texts


class SpeedHaHistory(RouletteHistory):
    pass

# an smiler type of roulette game 
class SpeedHaGame(RouletteGame):
    texts_source = texts.SpeedHa
    name = texts_source.name
    history_object = SpeedHaHistory
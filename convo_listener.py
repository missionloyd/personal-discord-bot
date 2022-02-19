import random

def reply():
  QUOTES = [
    "If you had the strength, you could live. This is our contract. In return for my gift of power, you must grant one of my wishes. If you enter this contract, you will live as a human, but also as one completely different. Different rules, different time, a different life.... The power of the king will make you lonely indeed. If you are prepared for that, then...",
    "Win through, Lelouch. Ignore your past, and the consequences of your actions.",
    "False tears bring pain to those around you. A false smile brings pain to one self.",
    "No matter how great you make yourself sound, you're still just a naive boy who's all talk and who only dreams of victory in his head.",
    "Do you know why snow is white..? Because it forgot what colour it was.",
    "In this world, evil can arise from the best of intentions. And there is good which can come from evil intentions.",
    "A remaining piece of hope, a faint sign of wishes will be born from despairs.",
    "*after a giant pizza is thrown into the air**Gasp* 'Pizza!'",
    "Death may be my only freedom.",
    "Within the endless flow of time, I am alone.",
    "In their heart, everyone has faith that their victory exists. However, in the face of time and destiny, the act of faith is fruitless and fleeting at best.",
    "There are times in life when you have to distance yourself from those you love, because you love them.",
  ]

  return "\n:green_circle: " + random.choice(QUOTES) + " :green_circle: \n"


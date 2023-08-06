"""Tests the core module"""

from botboy import BotBoy

bot = BotBoy('Adder', lambda x, y: x + y)

def test_display_information():
  global bot
  bot.display_information()

def test_execute():
  global bot
  bot.execute(1, 2)
  bot.set_processing()
  bot.execute(3, 4)
  bot.set_processing()
  bot.execute(5, 6)
  bot.set_on_file()
  bot.execute(7, 8)

if __name__ == '__main__':
  test_display_information()
  test_execute()

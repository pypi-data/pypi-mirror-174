# BotBoy
Multithreading &amp; processing worker that executes functions and prints the
result

## Installation
`pip install botboy`

## Usage
### Create a new BotBoy object with a pre-defined function object and a name

`from botboy import BotBoy`

`bot = BotBoy('Adder', lambda x, y: x + y)`

### Display the information

`bot.display_information()`

> Adder

> <function <lambda> at 0x10e6e8040>

### Execute function object on separate thread

`bot.execute(1, 2)`

> Adder is executing task: <function <lambda> at 0x10e6e8040>

> Retrieved result from Adder: 3
### Execute function object on separate process

`bot.set_processing() # Can be turned back to thread by running same method`

`bot.execute(3, 4)`

> Adder is executing task: <function <lambda> at 0x10e6e8040>

> Retrieved result from Adder: 7

## Test

Runs the tests on the core module

`make test`

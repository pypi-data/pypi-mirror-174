"""Multithreading & processing worker that executes functions and prints the result"""
__version__ = '1'

import threading
import multiprocessing

class BotBoy:
  def __init__(self, name, task):
    self.name = name
    self.task = task
    self.result = None
    self.processing = False

  def get_name(self):
    """Displays assigned name"""
    print(self.name)

  def get_task(self):
    """Displays current tasks"""
    print(self.task)

  def bot_task(self, *args):
    """Adds logging to the task"""
    print(f'{self.name} is executing task: {self.task}')

    self.result = self.task(*args)

    print(f'Retrieved result from {self.name}: {self.result}')

  def run_task_on_thread(self, *args):
    """Executes the task on a separate thread"""
    thread = threading.Thread(target=self.bot_task, name=self.name, args=args)
    thread.run()

  def run_task_on_process(self, *args):
    """Executes the task on a separate process"""
    process = multiprocessing.Process(target=self.bot_task, name=self.name, args=args)
    process.run()

  def display_information(self):
    """Displays the bot's name and task"""
    self.get_name()
    self.get_task()

  def set_processing(self):
    """Changes from threading to processing"""
    if self.processing: self.processing = False
    else: self.processing = True

  def execute(self, *args):
    """Runs the assigned task"""
    if not self.processing: self.run_task_on_thread(*args)
    else: self.run_task_on_process(*args)

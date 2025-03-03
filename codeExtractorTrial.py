from guesslang import Guess

guess = Guess()
code = """
def hello():
print("Hello, world!")
if True:
print("This is a test")
"""
print("Detected Language:", guess.language_name(code))

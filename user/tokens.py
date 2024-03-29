import random
import string
import time


class Tokens:

    def __init__(self):
        self.t = ""

    def generate_token(self):
        token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(30))
        return token

    def get_token_creation_time(self):
        now = time.strftime('%Y-%m-%d %H-%M-%S')
        return now

    def get_token(self):
        return self.generate_token()

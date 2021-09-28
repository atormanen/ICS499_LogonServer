from global_logger import logger, VERBOSE

#Signin will handle the mechanics of signing a user in
import random
import string
import time

class Tokens:

    log_function_name = lambda x: logger.debug(f"func {inspect.stack()[1][3]}")

    def __init__(self):
        self.t = ""

    def generateToken(self):
        self.log_function_name()
        token = ''.join(random.SystemRandom().choice(string.ascii_uppercase +\
                        string.digits) for _ in range(30))
        return token

    def getTokenCreationTime(self):
        self.log_function_name()
        now = time.strftime('%Y-%m-%d %H-%M-%S')
        return now

    def getToken(self):
        self.log_function_name()
        return self.generateToken()

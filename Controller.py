from Listener import Listener
from multiprocessing import Process

class Controller:
    #listener = ''

    def __init__(self):
        self.listener = Listener()
        listener.listen()
        #createListener()

    def createListener():
        process = Process(target=listener.listen, args=(listener,))
        process.start()
        process.join()

def main():
    print('inside main')




if __name__ == '__main__':
    main()

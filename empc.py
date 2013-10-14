import webbrowser
from time import sleep
from empc import server


if __name__ == "__main__":
    host = 'localhost'
    port = 9932
    webbrowser.open("http://{0}:{1}".format(host, port))
    server.start(host, port)

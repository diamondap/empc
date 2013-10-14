import webbrowser
from time import sleep
from empc import server


if __name__ == "__main__":
    host = 'localhost'
    port = 9932
    url = "http://{0}:{1}".format(host, port)
    #webbrowser.open(url)
    server.start(host, port)

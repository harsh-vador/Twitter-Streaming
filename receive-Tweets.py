
import tweepy
from tweepy.auth import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json

consumer_key    = 'w3c71qVzZGNgW9dCXT0NbHHDt'
consumer_secret = '8XVonbrgPMvvsHJpFHlrzswGTIhmqiE7TOuW6vRW5F2ovfvgNN'
access_token    = '1299605150152105984-hslchIR50LQFbysEtUJqqXFTDiXQ6J'
access_secret   = '1299605150152105984-hslchIR50LQFbysEtUJqqXFTDiXQ6J'

class TweetsListener(StreamListener):

    def __init__(self, csocket):
        self.client_socket = csocket
    def on_data(self, data):
        try:
            message = json.loads( data )
            print( message['text'].encode('utf-8') )
            self.client_socket.send( message['text'].encode('utf-8') )
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def if_error(self, status):
        print(status)
        return True


def send_tweets(c_socket):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream.filter(track=['football'])



if __name__ == "__main__":
    new_skt = socket.socket()
    host = "127.0.0.1"
    port = 5555
    new_skt.bind((host, port))

    print("Now listening on port: %s" % str(port))

    new_skt.listen(5)
    c, addr = new_skt.accept()

    print("Received request from: " + str(addr))
    
    send_tweets(c)

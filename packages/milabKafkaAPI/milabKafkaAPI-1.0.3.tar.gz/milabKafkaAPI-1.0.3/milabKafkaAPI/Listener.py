from API import KafkaAPI
from butter.mas.api import HttpClient

"""
Listening and reacting to messages in the kafka server example.

General instructions:
Step 1: create a callback function to be called upon by the kafka listener, that acts on the message received.
Step 2: activate a listener on a specific kafka topic in the server, pointing to the callback function from step 1,
        using KafkaAPI.Subscribe(topic, duration, offset, callback_function).
"""

# The callback function
def MoveRobot(res):
    butterHttpClient = HttpClient('192.168.56.223')
    if res["distance"] <= 5:
        butterHttpClient.playAnimation('KipFollowtoUser')
        print(butterHttpClient.getAvailableAnimations())
    else:
        butterHttpClient.playAnimation('KipReturntoUser')

if __name__ == '__main__':
    KafkaAPI.Subscribe('gazer', -1, 'latest', MoveRobot)
    # duration set to -1 to run in an infinite loop
    # offset set to 'latest' to start listening from current time, and not from server boot (using 'earliest')

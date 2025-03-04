from concurrent_modular_agent import MessageClient


def test_send_receive():
    sender = MessageClient("agent", "sender")
    receiver = MessageClient("agent", "receiver")
    sender.send("receiver", "Hello")
    assert receiver.receive() == "Hello"
    

def test_receive_timeout():
    receiver = MessageClient("agent", "receiver")
    assert receiver.receive(timeout=0) == None
"""
Consumer script that listens to a Kafka topic and processes incoming messages.

Example usage:

    $ python consumer.py
"""

from subscriber_server import CentralServer

def main():
    """
    Main entry point of the consumer script.

    Initializes a CentralServer instance with the specified bootstrap servers, group ID, and topic,
    and starts listening for incoming messages.
    """
    bootstrap_servers = "192.168.20.190:9092"
    group_id = "kafka-python-consumer"
    topic = "test"
    central_server = CentralServer(bootstrap_servers, group_id, topic)
    central_server.listen()

if __name__ == "__main__":
    main()
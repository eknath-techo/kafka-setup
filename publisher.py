"""
Producer

This script acts as a producer that captures and processes images and sends them to a Kafka topic.
"""

from publisher_server import EdgeDevice

def main():
    """
    Main function to initiate the producer.

    This function creates an instance of EdgeDevice, which captures and 
    processes images, and sends them to a Kafka topic.
    """
    bootstrap_servers = "192.168.20.190:9092"           #"""str: The bootstrap server IP address for Kafka"""
    topic = "img"                                      #"""str: The Kafka topic to publish images to"""
    edge_device = EdgeDevice(bootstrap_servers, topic)#"""EdgeDevice: An instance of EdgeDevice that captures and processes images"""
    edge_device.capture_and_process()                  #"""Captures and processes images, and sends them to the Kafka topic"""

if __name__ == "__main__":
    """
    Entry point of the script.

    Example:
    ```
    python producer.py
    ```
    This will start the producer, which will capture and process images, and send them to the Kafka topic.
    """
    main()
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
    bootstrap_servers = "192.168.20.190:9092"          
    topic = "images"                                     
    camera_id = 0
    edge_device = EdgeDevice(bootstrap_servers, topic, camera_id=camera_id)
    edge_device.capture_and_process()               

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
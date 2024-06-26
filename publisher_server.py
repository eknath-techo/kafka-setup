""" 
EdgeDevice module
This module provides a class EdgeDevice that captures images 
from a camera, processes them, and sends them to a Kafka server.
"""

import pickle
import datetime
import cv2
from confluent_kafka import Producer

class EdgeDevice():
    """ 
    EdgeDevice class

    This class represents an edge device that captures images from a camera, processes them, and sends them to a Kafka server.

    Args :
    bootstrap_servers (str): The bootstrap servers for the Kafka cluster.
    topic (str): The topic to produce messages to.

    Attributes:
    producer (Producer): The Kafka producer instance.
    topic (str): The topic to produce messages to.
    cap (VideoCapture): The OpenCV video capture instance.
    """
    def __init__(self, bootstrap_servers, topic):
        """
        Initialize the EdgeDevice instance.

        Args:
        bootstrap_servers (str): The bootstrap servers for the Kafka cluster.
        topic (str): The topic to produce messages to.
        """
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})
        self.topic = topic
        self.cap = cv2.VideoCapture(0)

    def acked(self, err, msg):
        """
        Callback function for message delivery.

        Args:
        err (Error): The error object if the message delivery failed.
        msg (Message): The message object.
        """
        if err is not None:
            print(f"Failed to deliver message: {str(msg)}: {str(err)}" )
        else:
            print(f"Message produced to: {msg.topic()} {[ msg.partition()]}")

    def capture_and_process(self):
        """
        Capture images from the camera, process them, and send them to the Kafka server.

        This method captures images from the camera, adds a timestamp to each frame, and sends them to the Kafka server.
        """
        while True:
            ret, frame = self.cap.read()
            if ret:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                cv2.putText(frame, current_time, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
                self.send_to_server(frame)
                cv2.imshow('Edge Device', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print("Failed to capture frame")
        self.cap.release()
        cv2.destroyAllWindows()

    def send_to_server(self, frame):
        """
        Send the processed frame to the Kafka server.

        Args :
            frame (numpy.ndarray): The processed frame.

        Example :
            >>> edge_device = EdgeDevice("localhost:9092", "my_topic")
            >>> frame = cv2.imread("image.jpg")
            >>> edge_device.send_to_server(frame)
        """
        data = pickle.dumps(frame)
        print("Frame send to kafka server")
        self.producer.produce(self.topic, key='camera_frame', value=data, callback=self.acked)
        self.producer.flush()
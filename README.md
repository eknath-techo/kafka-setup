# Kafka-Setup
This project demonstrates how to use Apache Kafka to stream video frames from an edge device to a central server. The edge device captures images from a camera, processes them, and sends them to a Kafka server. The central server consumes these video frames, processes them using the Google Cloud Vision API, and displays the annotated frames.
## Prerequisite
- Knowledge
  - Node.JS Intermediate level
  - Experience with designing distributed systems
- Tools
  - Python: [Download Python](https://www.python.org/downloads/)
  - Docker: [Download Docker](https://www.docker.com)
  - VsCode: [Download VSCode](https://code.visualstudio.com)

## Steps
1. Start Zookeper Container and expose PORT `2181`.
```bash
docker run -p 2181:2181 zookeeper
```
2. Start Kafka Container, expose PORT `9092` and setup ENV variables. Replace <PRIVATE_IP> with your private IP address:
```bash
docker run -p 9092:9092 \
-e KAFKA_ZOOKEEPER_CONNECT=<PRIVATE_IP>:2181 \
-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://<PRIVATE_IP>:9092 \
-e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
confluentinc/cp-kafka
```
3. Clone the Project Repository
```bash
git clone https://github.com/eknath-techo/kafka-setup.git
cd kafka-setup
```

4. Install Python Dependencies
```bash 
pip install -r requirements.txt
```

5. Configure the Edge Device
- Edit the publisher.py script to set the correct Kafka bootstrap server address and topic:

```bash
# In publisher.py
bootstrap_servers = "192.168.20.86:9092"
topic = "img"
```

6. Run the Edge Device Script
```bash
python publisher.py
```

7. Configure the Subscriber Server
- Edit the subscriber.py script to set the correct Kafka bootstrap server address, group ID, and topic:
```bash
# In subscriber.py
bootstrap_servers = "192.168.20.86:9092"
group_id = "kafka-python-consumer"
topic = "img"


8.Run the Central Server Script
- Start the central server script to listen for incoming messages from the Kafka topic and process the frames:
```bash
python subscriber.py
```

## File Descriptions
- <b>publisher_server.py</b>: Contains the EdgeDevice class that captures images from the camera, processes them, and sends them to the Kafka server.
- <b>publisher.py</b>: Script to start the edge device, capture and process images, and send them to the Kafka topic.
- <b>subscriber_server.py</b>: Contains the CentralServer class that consumes video frames from the Kafka topic, processes them, and displays the annotated frames.
- <b>subscriber.py</b>: Script to start the central server, listen for incoming messages, and process the frames.
## Notes
1. Ensure your camera is connected and accessible by OpenCV.
2. Replace <PRIVATE_IP> with your actual private IP address.
3. The default Kafka topic is set to "img". You can change this in the publisher.py and subscriber.py scripts.
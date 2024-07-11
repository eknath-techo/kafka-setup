# run this script on your local machine and replace the "REMOTE_IP" with remote_server IP
import cv2
import requests
import numpy as np

url = "http://REMOTE_IP:5000/video_feed"

while True:
    img_resp = requests.get(url, stream=True)
    if img_resp.status_code == 200:
        byte_stream = b''
        for chunk in img_resp.iter_content(chunk_size=1024):
            byte_stream += chunk
            a = byte_stream.find(b'\xff\xd8')
            b = byte_stream.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = byte_stream[a:b+2]
                byte_stream = byte_stream[b+2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                cv2.imshow('Remote Camera', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    else:
        print("Unable to connect to the stream.")
        break

cv2.destroyAllWindows()
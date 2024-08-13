import zmq
import cv2
import json
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

def subscriber(topic):
    context = zmq.Context()
    subscriber_socket = context.socket(zmq.SUB)
    subscriber_socket.connect("tcp://localhost:7000")

    subscriber_socket.setsockopt_string(zmq.SUBSCRIBE, topic)

    print('Subscriber Started')
    while True:
        # receiving detection data
        topic_received, detection_results_serialized = subscriber_socket.recv_multipart()
        
        # Deserialize the detection results using JSON
        detection_results = json.loads(detection_results_serialized.decode())

        # Access detection results
        bboxes = detection_results['bboxes']
        classes = detection_results['classes']
        scores = detection_results['scores']
        area = detection_results['area']
        center_coords = detection_results['center_coords']

        # Deserialize image frame
        image_frame = np.array(detection_results['image'], dtype=np.uint8)


        print(f'''bboxes : {bboxes} 
                classes : {classes}
                scores : {scores}
                area : {area},
                center_coords : {center_coords},
                
                ''')

        print(f'Subscriber receiving frames for the topic {topic_received.decode()}')
        
        # Display the received image
        cv2.imshow(topic_received.decode(), image_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    subscriber_socket.close()

if __name__ == "__main__":
    topic = os.getenv('USE_CASE')
    subscriber(topic)

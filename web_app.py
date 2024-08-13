import tkinter as tk
import zmq
from PIL import Image
from PIL import ImageTk
import io
import json

class FruitPickingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fruit Picking")
        
        # Set up ZeroMQ
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:7000")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "image")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "data")
        
        # UI Elements
        self.create_ui_elements()
        
    def create_ui_elements(self):
        # Frame display
        self.frame_label = tk.Label(self.root)
        self.frame_label.grid(row=0, column=0, rowspan=6, sticky="nsew")
        
        # Right side text display
        self.data_text = tk.Text(self.root, width=40, height=20)
        self.data_text.grid(row=0, column=2, sticky="nsew")
        
        # Configure grid weights to control resizing behavior
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=7)  # 70% width
        self.root.grid_columnconfigure(1, weight=3)  # 30% width
        
        # Start listening to ZeroMQ
        self.root.after(100, self.update_data)
        
    def update_data(self):
        try:
            topic, message = self.socket.recv_multipart()
            topic = topic.decode('utf-8')
            
            if topic == "image":
                # Convert frame bytes to an image and then to a PhotoImage for tkinter
                frame_image = Image.open(io.BytesIO(message))
                frame_photo = ImageTk.PhotoImage(frame_image)
                self.frame_label.config(image=frame_photo)
                self.frame_label.image = frame_photo  # Keep a reference to prevent garbage collection
            
            elif topic == "data":
                data = message.decode('utf-8')
                data = json.loads(data)
                #Widgets
                self.data_text.delete(1.0, tk.END)
                #BENCHMARK
                self.data_text.insert(tk.END, f"Benchmark:\n FPS: {str(int(data['fps']))} || CPU: {str(data['cpu'])} || RAM: {str(data['ram'])} \n\n")
                
                #DETECTIONS
                self.data_text.insert(tk.END, "Detections:\n")
                for i in range(len(data['detections']['bboxes'])):
                    fruit = ['apple', 'unknown'][data['detections']['ids'][i]]
                    condition = ['unripe', 'ripe'][data['detections']['conditions'][i]]
                    size = ['small', 'medium', 'large'][data['detections']['sizes'][i]]
                    self.data_text.insert(tk.END, f"{fruit}, {condition}, {size}\n")
                
                #CONTROL ACTIONS
                self.data_text.insert(tk.END, "\nControl Actions:\n")
                for i in range(len(data['actions']['directionX'])):
                    harvest = ['ignore', 'pick'][data['actions']['pick'][i]]
                    if harvest == 'ignore':
                        self.data_text.insert(tk.END, f"{harvest}\n")
                    else:
                        Hmov = data['actions']['directionX'][i] + str(data['detections']['center'][i][0] - 0.5)[:8]
                        Vmov = data['actions']['directionY'][i] + str(data['detections']['center'][i][1] - 0.5)[:8]
                        self.data_text.insert(tk.END, f"{harvest}:{Hmov}:{Vmov}\n")
                      
        except zmq.Again:
            pass
            
        self.root.after(100, self.update_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = FruitPickingApp(root)
    root.mainloop()

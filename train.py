from ultralytics import YOLO
import os

# Optional: Start TensorBoard manually in another terminal if needed
# os.system("tensorboard --logdir=runs/train --port=6006 &")

# Set environment variable to reduce CUDA fragmentation
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# Load the lightest model (YOLOv8n)
model = YOLO('yolov8x.pt')  # or 'yolov8s.pt' for more accuracy

# Start training
model.train(
    data='YOLOv8_dataset/data.yaml',  # path to your dataset YAML
    epochs=50,
    imgsz=416,              # smaller image size to reduce memory load
    batch=2,                # small batch size to fit into GPU memory
    name='idd_yolov8_model',
    workers=1,              # fewer workers, less RAM pressure
    device=0,               # use CUDA device 0
    amp=True,               # use Automatic Mixed Precision
    project='runs/train',
    exist_ok=True,
    verbose=True
)


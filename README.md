# Apple Analyzer using Publisher-Subscriber Architecture with ZMQ

This project implements an Apple Analyzer that performs fruit detection, classification, and size segmentation using a publisher-subscriber architecture facilitated by ZeroMQ (ZMQ). The project is designed to process images of apples, categorizing them as ripe, unripe, or rotten, and sorting them into different size categories.

## Project Overview

The Apple Analyzer is built to serve multiple key purposes:
- **Fruit Detection:** Identify apples within images.
- **Fruit Classification:** Categorize apples as ripe, unripe, or rotten.
- **Fruit Size Segmentation:** Sort apples into Large, Medium, or Small sizes.

### Architecture
The project follows a publisher-subscriber architecture:
- **Publisher:** This component captures or receives apple images and publishes the data to a ZeroMQ socket.
- **Subscriber:** This component subscribes to the data from the publisher, processes the images to detect, classify, and segment the apples, and outputs the results.

### Key Features
- **Real-Time Processing:** The system is designed to work in real-time, providing instant feedback on apple quality.
- **Scalability:** The publisher-subscriber model allows for easy scaling, with multiple subscribers processing data from a single publisher.
- **Modularity:** Each component (detection, classification, segmentation) is modular, allowing for easy updates and improvements.

# Result

https://github.com/user-attachments/assets/85e93112-a644-469a-952d-3ebdf879523f



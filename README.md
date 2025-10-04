# Callus Inc. - AI ML Server Engineer Competency Assessment

## 🕺 Project: Cloud-based Dance Movement Analysis Server

This project is a cloud-deployed AI service that analyzes short dance videos to identify key dance poses. It's built with Python, MediaPipe, and Flask, containerized with Docker, and deployed on AWS EC2.

---

### 🤔 Thought Process & Design Choices

* **Core Technology**: I chose **MediaPipe** for its high-performance, pre-trained pose detection models, which are lightweight enough for a simple server. It provides 33 keypoints, offering sufficient detail for pose analysis.
* **Pose Definition**: Instead of relying on raw coordinates, poses are defined by the **angles between body landmarks**. This makes detection robust against variations in the dancer's position, scale, and video resolution. The logic is encapsulated in `poses.py` for clarity.
* **API Framework**: **Flask** was selected for its simplicity and lightweight nature, making it ideal for a single-endpoint microservice. For a more complex application, I might have chosen FastAPI for its automatic data validation and API documentation features.
* **Containerization**: **Docker** was the obvious choice for packaging. It ensures that the application runs identically on my local machine and in the cloud, resolving any dependency conflicts and simplifying the deployment process. The `opencv-python-headless` package was used to minimize the image size.
* **Cloud Platform**: I chose **AWS EC2** due to its reliability, scalability, and the generous free tier, making it perfect for a proof-of-concept deployment. The entire deployment process is scripted and straightforward.

---

### 🌐 How This Project Fits Callus's Vision

*(This is your space to be creative. For example: "This project serves as a foundational microservice for Callus's vision of creating interactive fitness and dance applications. By accurately analyzing user movements in real-time, we can provide feedback, track progress, or even create gamified experiences. This server is designed to be a scalable, low-latency component in a larger ecosystem of wellness technology...")*

---

### 🚀 API Usage

The server exposes one endpoint: `/analyze`.

**Endpoint**: `POST http://<your-ec2-public-ip>/analyze`

**Request**: `multipart/form-data` with a single field:
* `key`: `video`
* `value`: The video file (`.mp4`, `.mov`, etc.)

**Example (`curl`)**
```bash
curl -X POST -F "video=@/path/to/your/dance.mp4" http://<your-ec2-public-ip>/analyze

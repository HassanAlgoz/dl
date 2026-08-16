# Computer Vision

> [_Computer vision_](https://en.wikipedia.org/wiki/Computer_vision) is an interdisciplinary field that deals with how computers can be made to gain high-level understanding from digital images or videos. From the perspective of engineering, it seeks to automate tasks that the human visual system can do.

## Applications of CV

![Real World Computer Vision Applications](../assets/cv_applications.png)

    
- **Facial Recognition:** This technology powers the Face ID on your smartphone, tagging friends in social media photos, and security screening at airports.
    
- **Medical Imaging:** Algorithms analyze X-rays, MRIs, and CT scans to help doctors detect anomalies like tumors or fractures earlier and with higher accuracy.
    
- **Retail and Manufacturing:** Used for automated products inspection for defects on assembly lines.
    
- **Autonomous Vehicles:** Self-driving cars use computer vision to process feeds from multiple cameras in real-time to detect lanes, read traffic signs, and avoid pedestrians and other vehicles.

## CV Tasks at HuggingFace

HuggingFace classifies Computer Vision into 19 [Tasks](https://huggingface.co/tasks) we mention a few here

![](../assets/hf_cv_tasks.png)

### 1. [Depth Estimation](https://huggingface.co/tasks/depth-estimation)

Depth estimation is the task of predicting the distance of objects in a scene from the camera's viewpoint. It converts a 2D image into a representation where each pixel corresponds to a depth value, which is crucial for robotics, 3D reconstruction, and autonomous driving.

### 2. [Image Classification](https://huggingface.co/tasks/image-classification)

Image classification involves assigning a single label or category to an entire input image from a predefined set of classes (e.g., labeling an image as a "cat", "dog", or "car").

### 3. [Image Feature Extraction](https://huggingface.co/tasks/image-feature-extraction)

This task involves passing an image through a pre-trained model to extract low-dimensional, dense vector embeddings that represent its visual content. These embeddings can then be used for downstream tasks like image retrieval, similarity search, or clustering.

### 4. [Image Segmentation](https://huggingface.co/tasks/image-segmentation)

Image segmentation divides an image into multiple segments or pixel-level groups to locate objects and boundaries. It includes semantic segmentation (classifying every pixel), instance segmentation (separating individual objects of the same class), and panoptic segmentation (combining both).

### 5. [Keypoint Detection](https://huggingface.co/tasks/keypoint-detection)

Keypoint detection involves identifying and locating specific, important points of interest within an image, such as facial landmarks (eyes, nose, mouth) or human skeletal joints for pose estimation.

### 6. [Mask Generation](https://huggingface.co/tasks/mask-generation)

Popularized by models like SAM (Segment Anything), mask generation allows users to isolate objects within an image by producing precise binary masks based on prompt inputs like bounding boxes, points, or text descriptions.

### 7. [Object Detection](https://huggingface.co/tasks/object-detection)

Object detection identifies the presence of objects within an image, classifies them, and locates them by drawing bounding boxes around each detected object.

### 8. Image-to-text (OCR)

**OCR** models convert the text present in an image, e.g. a scanned document, to text.

![](../assets/vlm_ocr.png)

#### Example Vision-language Model

[`NAMAA-Space/Qari-OCR-0.4.0-VL-4B-Instruct`](https://huggingface.co/NAMAA-Space/Qari-OCR-0.4.0-VL-4B-Instruct) is a **vision-language model (VLM)** fine-tuned for OCR on Islamic books and Arabic manuscripts. Based on [Qwen/Qwen3-VL-4B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct), trained on 45,000 image-text pairs from the [seemorg/books-ocr](https://huggingface.co/datasets/seemorg/books-ocr) dataset.


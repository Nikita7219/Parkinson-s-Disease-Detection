# **🧠** Parkinson's Disease Detection Using CNN

## **📌 Introduction**

Parkinson's disease (PD) is a progressive neurodegenerative disorder affecting movement control, highlighting the importance of timely detection and intervention to improve patient quality of life. However, accurate diagnosis remains challenging due to its similarity with other neurological conditions, leading to a 25% rate of inaccurate manual diagnoses. Convolutional Neural Networks (CNNs) offer a promising solution for medical image classification and analysis, capable of learning complex patterns in images. In this study, we introduce an innovative automated diagnostic model using CNN that provides an appropriate output indicating whether a person is diagnosed with PD or not.

## **🎥 Demo**

Check out the working demo on **YouTube**:  
📺 [Watch the Demo](https://youtu.be/pP9AxfuGayM)


## **📥 Download Trained Model**  

To use the pre-trained model, download the `.h5` and `.keras` files from the link below:  

📂 **[Download Model Files](https://drive.google.com/drive/folders/16E8SJtag6H4gpxvjVn5FQsWT00-ZhpWa?usp=sharing)**  

After downloading, place the files inside the `models` directory in the project.


## **📂 Dataset Details**

In the proposed system, the dataset is gathered from the **Parkinson’s Progression Markers Initiative (PPMI)**. We specifically use a dataset containing **31,436 MRI scans** in the **DICOM format**.

* **18,690 MRI scans** related to Parkinson's Disease  
* **12,746 MRI scans** representing Healthy Controls  
* **Data Split:**  
  * Training: **80%**  
  * Validation: **10%**  
  * Testing: **10%**  
* **Dataset Size:** **7.13 GB**

## **🎯 Objectives**

✔ Develop an automated diagnostic model using CNNs to accurately diagnose PD.  
✔ Utilize the **Parkinson Progression Markers Initiative (PPMI)** dataset, which provides     benchmarked MRI images of PD and healthy controls.  
✔ Differentiate between PD and non-PD cases with high accuracy.

## **⚙ Methods**

A **Convolutional Neural Network (CNN)** is a deep learning algorithm suitable for medical image classification and analysis as it can learn complex patterns in images and identify hidden trends in data.  
We have used:

* **VGG16** and **ResNet50** pretrained CNN models to achieve high accuracy and prediction.  
* Various algorithms and activation functions such as **EfficientNetB0**, **EfficientNetB1**, and **Softmax**, **Sigmoid**, and **ReLU** to validate performance.

## **📊 Results**

✔ Achieved an **outstanding accuracy rate of 97%**.  
✔ Tested and validated the model using multiple approaches.

## **🔍 Conclusion**

This research introduces an innovative framework for the **early detection of Parkinson’s disease using convolutional neural networks**. Our system demonstrates remarkable capability in identifying subtle patterns indicative of PD in its early stages.

## **🛠 Tools and Technologies Used**

🔹 **Integrated Development Environment (IDE):** Visual Studio Code  
🔹 **Programming Languages:** Python, CSS, HTML, JavaScript  
🔹 **Database:** phpMyAdmin (MySQL)  
🔹 **Libraries:** Keras, NumPy, OpenCV (CV2), scikit-learn (sklearn), Matplotlib, SciPy,   TensorFlow, Flask  
🔹 **Web Framework:** Flask  
🔹 **Machine Learning Models:** VGG16, ResNet50, EfficientNetB0, EfficientNetB1  
🔹 **Data Format:** DICOM (Digital Imaging and Communications in Medicine)

## **🚀 Installation Guide**

Follow these steps to set up and run the project on your local system:

1️⃣ **Clone the repository**:
  ```bash
  git clone https://github.com/your-username/Parkinson-s-Disease-Detection.git
  ```

2️⃣ **Navigate to the project directory**:
  ```bash
  cd Parkinson-s-Disease-Detection
  ```


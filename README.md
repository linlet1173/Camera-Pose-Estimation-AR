## Camera Pose Estimation and AR

This is a camera pose estimation and AR project using openCV python. This project implements an AR system using camera pose estimation. It overlays 3D letters "L", "I", and "N" onto a chessboard using OpenCV. The AR objects are rendered in 3D and respond accurately to the camera's position and orientation in space.



### Objective

- Estimate the camera pose using calibration data.
- Visualize a custom AR object (3D letters) onto a real-world scene (chessboard pattern).



## Result

### Original chessboard image
<img width="468" alt="cv04 chessboard" src="https://github.com/user-attachments/assets/e612b676-74a5-4b3e-bfa0-ff03a4f12dfc" />


### Camera Calibration image
<img width="544" alt="cv03 detection_image" src="https://github.com/user-attachments/assets/76762940-067f-469c-ae51-f6e4028f56eb" />


### AR visualization image
<img width="468" alt="cv04 ARobject" src="https://github.com/user-attachments/assets/d9b866d8-f4fa-4628-95e3-01274e22998f" />




### How It Works

1. **Camera Calibration**  
   Used pre-calibrated intrinsic parameters and distortion coefficients from camera calibration assignment.

2. **Pose Estimation**  
   - Detected chessboard corners in each frame.
   - Used `cv.solvePnP()` to compute rotation and translation vectors.

3. **AR Object Rendering**  
   - Defined 3D coordinates of letters "L", "I", "N".
   - Projected 3D points to 2D using `cv.projectPoints()`.
   - Rendered 3D lines in red to form each letter.



### Dependencies

    OpenCV
    NumPy



###  How to Run

### 1. Install Dependencies
    pip install opencv-python numpy

### 2. Run the Script
    python cv04.CPE&AR.py
* Make sure the video file (chessboard.avi) is in the correct path.
* Output video will be saved as ar_object.avi.



### File Structure

    ├── cv04.CPE&AR.py              # Main Python script
    ├── chessboard.avi         # Input video
    ├── ar_object.avi      # Output with AR overlay
    ├── images/
    │   ├── chessboard.png
        ├── detection_image.png
    │   └── ar_object.png
    └── README.md



### License

This project is licensed under the [MIT License].

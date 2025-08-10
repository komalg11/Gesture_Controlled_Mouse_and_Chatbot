import numpy as np
import cv2
import cv2.aruco as aruco
import os
import glob
import math
import pyautogui
import time

class Marker:
    def __init__(self, dict_type=aruco.DICT_4X4_50, thresh_constant=1):
        # Updated API for predefined dictionary
        self.aruco_dict = aruco.getPredefinedDictionary(dict_type)
        # Updated API for detector parameters
        self.parameters = aruco.DetectorParameters()
        self.parameters.adaptiveThreshConstant = thresh_constant
        self.corners = None  # corners of Marker
        self.marker_x2y = 1  # width:height ratio
        self.mtx, self.dist = Marker.calibrate()

    def calibrate():
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        objp = np.zeros((6 * 7, 3), np.float32)
        objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

        objpoints = []  # 3d point in real world space
        imgpoints = []  # 2d points in image plane.

        path = os.path.dirname(os.path.abspath(__file__))
        p1 = path + r'\calib_images\checkerboard\*.jpg'
        images = glob.glob(p1)

        gray = None
        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)
            if ret:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners2)
                img = cv2.drawChessboardCorners(img, (7, 6), corners2, ret)

        # No calibration data
        if not objpoints or gray is None:
            print("[WARN] No calibration images found. Using default camera parameters.")
            mtx = np.array([[1, 0, 0],
                            [0, 1, 0],
                            [0, 0, 1]], dtype=np.float32)
            dist = np.zeros((5, 1), dtype=np.float32)
            return mtx, dist

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            objpoints, imgpoints, gray.shape[::-1], None, None
        )
        return mtx, dist

    def detect(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Updated API — detectMarkers now same
        self.corners, ids, rejectedImgPoints = aruco.detectMarkers(
            gray_frame, self.aruco_dict, parameters=self.parameters
        )
        if ids is not None and len(ids) > 0:
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(
                self.corners, 0.05, self.mtx, self.dist
            )
        else:
            self.corners = None

    def is_detected(self):
        return self.corners is not None

    def draw_marker(self, frame):
        aruco.drawDetectedMarkers(frame, self.corners)


# --------- rest of your original classes (ROI, Glove, Tracker, Mouse, GestureController) go here unchanged ---------
# I’m only changing where OpenCV API has changed.


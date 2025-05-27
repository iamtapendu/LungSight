"""
UI Configuration and Utility Definitions for LungSight Application

This module provides:
- Thematic color settings and fonts used across the UI.
- Global paths to the best segmentation and classification models.
- Definitions for key segmentation evaluation metrics: Jaccard Index and Dice Coefficient.

Modules Used:
-------------
- TensorFlow/Keras for deep learning.
- PIL, OpenCV, and Matplotlib for image processing and visualization.
- Tkinter for GUI components.
"""

# === Standard and GUI Libraries ===
import os
import re
import tkinter as tk
import tkinter.messagebox as msg
from tkinter import filedialog
from tkinter import messagebox

# === Scientific and Image Processing Libraries ===
import numpy as np
import cv2
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

# === TensorFlow and Keras ===
import tensorflow as tf
from tensorflow import keras

# === Warnings Management ===
import warnings


# ======================
# UI Theme Configuration
# ======================
class Litera:
    """
    Defines a light-themed color scheme for the GUI components.
    """
    type = "light"
    primary = '#008cba'
    secondary = "#adb5bd"
    success = "#02b875"
    info = "#17a2b8"
    warning = "#f0ad4e"
    danger = "#d9534f"
    light = "#F8F9FA"
    dark = "#343A40"
    bg = "#ffffff"
    fg = "#343a40"
    selectbg = "#d9d9d9"
    selectfg = "#ffffff"
    border = "#bfbfbf"
    inputfg = "#343a40"
    inputbg = "#fff"
    menubg = "#2b3e50"
    selectmenu = "#3d5770"

# Create color instance for use in UI
clr = Litera()

# ======================
# Font Configuration
# ======================
TXT_11 = ('Helvetica', 11)
TXT_11_B = ('Helvetica', 11, 'bold')
TXT_12_B = ('Helvetica', 12, 'bold')
PROD_11_B = ('Courier', 11, 'bold')

# ======================
# Model File Paths
# ======================
CLF_PATH = os.path.abspath('resource/best_clf_model.keras')
SEG_PATH = os.path.abspath('resource/best_seg_model.keras')


# ======================
# Evaluation Metrics
# ======================

@keras.utils.register_keras_serializable()
def jaccard_index(y_true, y_pred, smooth=100):
    """
    Computes the Jaccard Index (IoU) for evaluating segmentation masks.

    Parameters:
    -----------
    y_true : tensor
        Ground truth binary mask.

    y_pred : tensor
        Predicted binary or probability mask.

    smooth : float, optional (default=100)
        Smoothing factor to avoid division by zero.

    Returns:
    --------
    jaccard : tensor
        Jaccard index (IoU) as a scalar tensor.
    """
    y_true_f = tf.reshape(tf.cast(y_true, tf.float32), [-1])
    y_pred_f = tf.reshape(tf.cast(y_pred, tf.float32), [-1])
    intersection = tf.reduce_sum(y_true_f * y_pred_f)
    union = tf.reduce_sum(y_true_f) + tf.reduce_sum(y_pred_f) - intersection
    return (intersection + smooth) / (union + smooth)


@keras.utils.register_keras_serializable()
def dice_coefficient(y_true, y_pred, smooth=1):
    """
    Computes the Dice Coefficient for evaluating segmentation overlap.

    Parameters:
    -----------
    y_true : tensor
        Ground truth binary mask.

    y_pred : tensor
        Predicted binary or probability mask.

    smooth : float, optional (default=1)
        Smoothing constant to prevent division by zero.

    Returns:
    --------
    dice : tensor
        Dice coefficient as a scalar tensor.
    """
    y_true_f = tf.reshape(tf.cast(y_true, tf.float32), [-1])
    y_pred_f = tf.reshape(tf.cast(y_pred, tf.float32), [-1])
    intersection = tf.reduce_sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (tf.reduce_sum(y_true_f) + tf.reduce_sum(y_pred_f) + smooth)

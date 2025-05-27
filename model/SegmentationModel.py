from common_libs import np, cv2, keras
from common_libs import dice_coefficient, jaccard_index

class SegmentationModel:
    """
    Handles loading and applying a pre-trained Keras model to perform
    lung segmentation on chest X-ray images.

    Attributes:
    -----------
    path : str
        Path to the Keras model file (.keras or .h5).

    customObj : dict
        Custom metrics dictionary required for loading the model.

    model : keras.Model
        Loaded Keras model ready for segmentation prediction.
    """

    def __init__(self, path):
        """
        Loads the segmentation model from the specified path using custom metrics.

        Parameters:
        -----------
        path : str
            File path to the trained Keras segmentation model.
        """
        self.path: str = path
        """str: Path to the saved Keras model file."""

        self.customObj: dict = {
            'dice_coefficient': dice_coefficient,
            'jaccard_index': jaccard_index
        }
        """dict: Custom evaluation metrics used during model training."""

        self.model: keras.Model = keras.models.load_model(self.path, custom_objects=self.customObj)
        """keras.Model: The trained segmentation model loaded from disk."""

    def predict(self, img):
        """
        Predicts a lung segmentation mask for the given chest X-ray image.

        Preprocessing:
        - Resize to 512x512.
        - Convert to grayscale.
        - Normalize pixel values to [0, 1].
        - Add batch dimension.

        Postprocessing:
        - Squeeze out batch/channel dims.
        - Scale values to [0, 255].
        - Convert to RGB for visualization.

        Parameters:
        -----------
        img : np.ndarray
            Input BGR image (OpenCV format).

        Returns:
        --------
        pred_mask : np.ndarray
            Predicted segmentation mask as an RGB image with uint8 values.
        """
        # Resize and normalize input
        img = cv2.resize(img, (512, 512))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img / 255.0
        img = np.expand_dims(img, axis=0)

        # Predict the mask
        pred_mask = self.model.predict(img, verbose=0)

        # Postprocess the prediction
        pred_mask = (np.squeeze(pred_mask) * 255).astype(np.uint8)
        pred_mask = cv2.cvtColor(pred_mask, cv2.COLOR_GRAY2RGB)

        return pred_mask

    @staticmethod
    def getColoredMask(image, mask_image, color=(255, 20, 255)):
        """
        Overlays a transparent colored segmentation mask on the input image
        to visualize segmented regions.

        Workflow:
        - Convert mask to grayscale to create binary mask.
        - Apply binary mask to extract relevant regions.
        - Paint masked regions with a specified color.
        - Blend the overlay with the original image.

        Parameters:
        -----------
        image : np.ndarray
            Original image in BGR format.

        mask_image : np.ndarray
            Segmentation mask image in RGB format (binary/grayscale-like).

        color : tuple, optional
            BGR color for mask overlay. Default is magenta (255, 20, 255).

        Returns:
        --------
        np.ndarray
            BGR image with the colored mask overlaid.
        """
        # Convert mask to grayscale for binary masking
        mask_image_gray = cv2.cvtColor(mask_image, cv2.COLOR_BGR2GRAY)

        # Extract mask region using the grayscale mask
        mask = cv2.bitwise_and(mask_image, mask_image, mask=mask_image_gray)

        # Identify non-black pixels (mask region)
        mask_coord = np.where(mask != [0, 0, 0])

        # Paint those pixels with overlay color
        mask[mask_coord[0], mask_coord[1], :] = color

        # Blend original and colored mask
        blended = cv2.addWeighted(image, 0.6, mask, 0.4, 0)

        return blended

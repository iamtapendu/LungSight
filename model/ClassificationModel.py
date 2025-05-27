from common_libs import np, cv2, keras
from common_libs import dice_coefficient, jaccard_index

class ClassificationModel:
    """
    Handles loading and using a pre-trained Keras classification model
    to predict the presence of lung disease (e.g., tuberculosis) from chest X-ray images.

    Attributes:
    -----------
    path : str
        File path to the saved Keras classification model.

    customObj : dict
        Dictionary containing any custom metrics used in the model.

    model : keras.Model
        Loaded Keras model ready for inference.
    """

    def __init__(self, path):
        """
        Initializes the ClassificationModel by loading the model with custom metrics.

        Parameters:
        -----------
        path : str
            File path to the trained Keras classification model (.keras or .h5).
        """
        self.path: str = path
        """str: Path to the trained classification model."""

        self.customObj: dict = {
            'dice_coefficient': dice_coefficient,
            'jaccard_index': jaccard_index
        }
        """dict: Custom metrics dictionary used during model training."""

        self.model: keras.Model = keras.models.load_model(self.path, custom_objects=self.customObj)
        """keras.Model: The classification model loaded from the provided path."""

    def predict(self, img):
        """
        Predicts disease presence probability or class from a chest X-ray image.

        Preprocessing:
        - Resize image to 512x512 pixels.
        - Convert to grayscale.
        - Normalize pixel values to [0, 1].
        - Add batch dimension.

        Postprocessing:
        - Squeeze output to return a scalar or 1D array.

        Parameters:
        -----------
        img : np.ndarray
            Input image in BGR format (as read using OpenCV).

        Returns:
        --------
        float or np.ndarray
            Predicted class probability or logits, depending on model architecture.
        """
        # Resize to input shape expected by model
        img = cv2.resize(img, (512, 512))

        # Convert BGR to grayscale
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Normalize to [0, 1]
        img = img / 255.0

        # Expand dimensions to match model input (1, 512, 512)
        img = np.expand_dims(img, axis=0)

        # Run prediction
        pred = self.model.predict(img, verbose=0)

        # Remove batch or extra dimensions if present
        pred = np.squeeze(pred)

        return pred

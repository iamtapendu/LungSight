import view.MainView as mv
import view.HomeView as hv
import model.SegmentationModel as sm
import model.ClassificationModel as cm
from common_libs import filedialog, messagebox, ImageTk, Image, cv2
from common_libs import SEG_PATH, CLF_PATH

class MainController:
    """
    Main controller that coordinates between the view and model layers.
    It manages user input (file upload), model predictions (segmentation & classification),
    and updating the UI accordingly.
    """

    def __init__(self):
        """
        Initializes the application components: main view, segmentation model,
        classification model, and home view.
        """
        # Instantiate the main GUI window.
        self.mainView: mv.MainView = mv.MainView()
        """MainView: The primary window of the application managing the root layout."""

        # Placeholder to store the uploaded image as a NumPy array.
        self.img: any = None
        """np.ndarray: Image loaded from the user's file input."""

        # Load the trained lung segmentation model.
        self.segModel: sm.SegmentationModel = sm.SegmentationModel(SEG_PATH)
        """SegmentationModel: Deep learning model for segmenting lung regions from the X-ray."""

        # Load the trained tuberculosis classification model.
        self.clfModel: cm.ClassificationModel = cm.ClassificationModel(CLF_PATH)
        """ClassificationModel: Deep learning model to classify presence of tuberculosis."""

        # Create the HomeView interface and bind the upload button to a callback.
        self.homeView: hv.HomeView = hv.HomeView(self.mainView, self.browseFile)
        """HomeView: Interface layer presenting the home screen layout and binding file upload event."""

        # Update the main layout before rendering.
        self.mainView.update_idletasks()

    def start(self):
        """
        Launches the application's main loop.
        This keeps the window open and responsive to user actions.
        """
        self.mainView.mainloop()

    def browseFile(self):
        """
        Handles the file selection dialog, triggers predictions,
        and updates the view with results.

        This method is triggered by the file upload button and facilitates:
        - Selecting an image file.
        - Displaying a loading animation.
        - Performing image segmentation and classification.
        - Displaying the processed results.
        """
        try:
            # Open a file dialog for image selection
            img_file = filedialog.askopenfilename(
                initialdir='',
                title='Select a file',
                filetypes=(('All Files', '*.*'),
                           ('PNG', '*.png'),
                           ('JPG', '*.jp*'),
                           ('BMP', '*.bmp'),
                           ('TIFF', '*.tif*'))
            )

            # Check if a valid file was selected
            if len(img_file) > 3:
                filename = img_file.split('/')[-1]

                # Trim long filenames for display
                if len(filename) > 20:
                    filename = filename[:10] + '...'

                # Update label and show loading indicator
                self.homeView.browseLbl.config(text='Uploaded File : ' + filename)
                self.homeView.showLoading()
                self.homeView.update_idletasks()

                # Run prediction pipeline
                self.loadInsight(img_file)

                # Hide loading indicator
                self.homeView.stopLoading()

        except Exception as e:
            # Show error dialog on failure
            messagebox.showerror('Error', f'Please check your file type...\n{e}')

    def loadInsight(self, img_file):
        """
        Loads and preprocesses the uploaded image, performs lung segmentation
        and tuberculosis classification, and updates the view with the results.

        Parameters:
        -----------
        img_file : str
            Path to the uploaded image file.

        Workflow:
        ---------
        - Read and resize the image to 512x512 pixels.
        - Generate the segmentation mask using the segmentation model.
        - Predict TB probability using the classification model.
        - Convert images to Tkinter-compatible formats.
        - Display the original image, segmentation mask, and overlay.
        - Show TB prediction result and confidence.
        """
        # Read and resize the image
        self.img = cv2.resize(cv2.imread(img_file, 1), (512, 512))

        # Predict segmentation mask
        pred_mask = self.segModel.predict(self.img)

        # Predict tuberculosis status
        tb = self.clfModel.predict(self.img)

        # Generate mask overlay
        colored_mask = self.segModel.getColoredMask(self.img, pred_mask)

        # Convert OpenCV images to Tkinter-compatible format
        pil_img = ImageTk.PhotoImage(Image.fromarray(self.img))
        pil_mask = ImageTk.PhotoImage(Image.fromarray(pred_mask))
        pil_colored_mask = ImageTk.PhotoImage(Image.fromarray(colored_mask))

        # Display original image, mask, and colored overlay
        self.homeView.addImage(pil_img, 0, 0)
        self.homeView.addImage(pil_mask, 0, 1)
        self.homeView.addImage(pil_colored_mask, 0, 2)

        # Display prediction label and confidence
        self.homeView.addLabel(f'Tuberculosis: {"Positive" if tb > 0.5 else "Negative"}', 1, 0)
        confidence = tb * 100 if tb > 0.5 else (1 - tb) * 100
        self.homeView.addLabel(f'Confidence: {confidence:.2f}%', 1, 1)

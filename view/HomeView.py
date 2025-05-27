from common_libs import tk, TXT_12_B

class HomeView(tk.Frame):
    """
    HomeView represents the main content view in the application window.

    This view includes:
    - A top menu bar with an upload label, button, and loading indicator.
    - A content area to display uploaded images and prediction labels.

    Attributes:
    -----------
    parent : tk.Tk or tk.Frame
        The parent container where this frame is placed.

    callback : function
        The function to be called when the 'Upload' button is clicked.

    menuFrm : tk.Frame
        Frame that contains the upload label, button, and loading text.

    browseLbl : tk.Label
        Label prompting the user to upload an X-ray image.

    browseBtn : tk.Button
        Button to trigger the upload action.

    loading : tk.Label
        Label used to show the current status ("Loading..." or "Finished").

    contentFrm : tk.Frame
        Frame where the output images and labels are dynamically displayed.
    """

    def __init__(self, parent, callback):
        """
        Initializes the HomeView frame, sets up layout and interface elements.

        Parameters:
        -----------
        parent : tk.Tk or tk.Frame
            The parent container.

        callback : function
            The function triggered when the upload button is clicked.
        """
        super().__init__(parent)
        self.parent = parent
        """tk.Tk or tk.Frame: The parent container where this frame is placed."""

        self.callback = callback
        """function: The function to be called when the 'Upload' button is clicked."""

        # Layout configuration
        self.grid(row=0, column=0, sticky=tk.NSEW)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=49)
        self.columnconfigure(0, weight=1)

        # Top menu for upload actions
        self.menuFrm = tk.Frame(self, name='menu')
        """tk.Frame: Frame that contains the upload label, button, and loading text."""

        self.menuFrm.grid(row=0, column=0, sticky=tk.NSEW)
        self.menuFrm.rowconfigure(0, weight=1)

        self.browseLbl = tk.Label(self.menuFrm, text="Upload a Lungs X-Ray Image: ")
        """tk.Label: Label prompting the user to upload an X-ray image."""

        self.browseLbl.grid(row=0, column=0, sticky=tk.NSEW)

        self.browseBtn = tk.Button(
            self.menuFrm,
            text='Upload',
            command=self.callback,
            font=TXT_12_B,
            anchor=tk.CENTER
        )
        """tk.Button: Button to trigger the upload action."""

        self.browseBtn.grid(row=0, column=1, sticky=tk.NSEW)

        self.loading = tk.Label(self.menuFrm, text='', font=TXT_12_B)
        """tk.Label: Label used to show the current status ("Loading..." or "Finished")."""

        self.loading.grid(row=0, column=2, sticky=tk.NSEW)

        # Content display area
        self.contentFrm = tk.Frame(self)
        """tk.Frame: Frame where the output images and labels are dynamically displayed."""
        self.contentFrm.grid(row=1, column=0, sticky=tk.NSEW)
        self.contentFrm.rowconfigure(0, weight=1)
        self.contentFrm.rowconfigure(1, weight=1)
        self.contentFrm.columnconfigure(0, weight=1)
        self.contentFrm.columnconfigure(1, weight=1)
        self.contentFrm.columnconfigure(2, weight=1)

    def addImage(self, img, row, column):
        """
        Displays an image in the content frame at the specified position.

        Parameters:
        -----------
        img : PhotoImage
            The image to be displayed (Tkinter-compatible).

        row : int
            Row index in the grid layout.

        column : int
            Column index in the grid layout.
        """
        img_container = tk.Label(self.contentFrm, image=img, bd=0)
        img_container.image = img  # Keep a reference to avoid garbage collection
        img_container.grid(row=row, column=column, sticky=tk.NSEW)

    def addLabel(self, text, row, column):
        """
        Adds a label with specified text to the content frame.

        Parameters:
        -----------
        text : str
            Text content of the label.

        row : int
            Row index in the grid layout.

        column : int
            Column index in the grid layout.
        """
        lbl = tk.Label(self.contentFrm, text=text, font=TXT_12_B)
        lbl.grid(row=row, column=column, sticky=tk.NSEW)

    def showLoading(self):
        """
        Displays a 'Loading...' status in the menu frame.
        """
        self.loading.config(text='Loading...')

    def stopLoading(self):
        """
        Updates the loading label to indicate completion ('Finished').
        """
        self.loading.config(text='Finished')

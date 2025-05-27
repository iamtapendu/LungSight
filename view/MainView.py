from common_libs import tk, clr, TXT_11_B, TXT_11


class MainView(tk.Tk):
    """
    MainView represents the root window of the LungSight application.

    This class sets up the initial configuration of the application window,
    including theming, fonts, widget styling, and responsive layout settings.

    Inherits:
    ---------
    tk.Tk : The main window class in Tkinter.
    """

    def __init__(self):
        """
        Initializes the main window with custom styling and responsive layout.
        """
        super().__init__()

        # ===== Window Properties =====
        self.title('LungSight')  # Window title
        self.geometry('1280x720')  # Default window size
        self.minsize(width=1067, height=600)  # Minimum size allowed

        # ===== General Styling =====
        self.config(bg=clr.bg)  # Background color
        self.option_add('*font', TXT_11)  # Default font
        self.option_add('*background', clr.bg)  # Default background
        self.option_add('*foreground', clr.fg)  # Default foreground

        # ===== Button Styling =====
        self.option_add('*Button.background', clr.primary)
        self.option_add('*Button.foreground', clr.light)
        self.option_add('*Button.activeBackground', clr.light)
        self.option_add('*Button.activeForeground', clr.primary)
        self.option_add('*Button.highlightBackground', clr.primary)
        self.option_add('*Button.highlightColor', clr.bg)

        # ===== Menu Button Styling =====
        self.option_add('*menu.Button.highlightThickness', 0)
        self.option_add('*menu.Button.background', clr.menubg)
        self.option_add('*menu.Button.foreground', clr.light)
        self.option_add('*menu.Button.activeBackground', clr.selectmenu)
        self.option_add('*menu.Button.activeForeground', clr.light)

        # ===== Entry (Input Fields) Styling =====
        self.option_add('*Entry.highlightColor', clr.fg)
        self.option_add('*Entry.highlightBackground', clr.secondary)

        # ===== General Widget Defaults =====
        self.option_add('*borderWidth', 0)
        self.option_add('*relief', tk.FLAT)

        # ===== Canvas Styling =====
        self.option_add('*Canvas.background', clr.bg)
        self.option_add('*Canvas.highlightThickness', 0)
        self.option_add('*Canvas.height', 600)

        # ===== Toolbar Buttons Styling (Classifier Section) =====
        self.option_add('*toolbar_c.Button.background', clr.success)
        self.option_add('*toolbar_c.Button.foreground', clr.light)
        self.option_add('*toolbar_c.Button.activeBackground', clr.light)
        self.option_add('*toolbar_c.Button.activeForeground', clr.success)
        self.option_add('*toolbar_c.Button.highlightBackground', clr.success)
        self.option_add('*toolbar_c.Button.highlightColor', clr.light)
        self.option_add('*toolbar_c.Button.font', TXT_11_B)

        # ===== Toolbar Buttons Styling (Segmenter Section) =====
        self.option_add('*toolbar_s.Button.background', clr.danger)
        self.option_add('*toolbar_s.Button.foreground', clr.light)
        self.option_add('*toolbar_s.Button.activeBackground', clr.light)
        self.option_add('*toolbar_s.Button.activeForeground', clr.danger)
        self.option_add('*toolbar_s.Button.highlightBackground', clr.danger)
        self.option_add('*toolbar_s.Button.highlightColor', clr.light)
        self.option_add('*toolbar_s.Button.font', TXT_11_B)

        # ===== Window Grid Layout Configuration =====
        self.rowconfigure(0, weight=1)  # Make row 0 stretchable
        self.columnconfigure(0, weight=1)  # Make column 0 stretchable

"""
Entry point for the application.

This script initializes and starts the main controller of the application,
which is responsible for coordinating the execution of the entire project pipeline.

Modules Used:
-------------
- controller.MainController: Contains the core logic and methods to run the application.
- common_libs.os: Used for setting environment variables.
- common_libs.warnings: Used to suppress warning messages during runtime.
"""

# Import the main controller from the controller module
import controller.MainController as mc

# Import necessary standard libraries
from common_libs import os, warnings

# Suppress all warnings
warnings.filterwarnings('ignore')

# Suppress TensorFlow debug logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if __name__ == '__main__':
    # Instantiate the main controller
    app = mc.MainController()
    """controller.MainController: Contains the core logic and methods to run the application."""

    # Start the application workflow
    app.start()

import sys
import time
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSlider,
    QLCDNumber,
    QHBoxLayout,
    QWidget,
    QLabel
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EcoRev") #sets the Windows Title of the app

        layout = QHBoxLayout() #makes the layout of the app to be horizontal

        self.displayer = QLCDNumber() #creates the LCD widget
        layout.addWidget(self.displayer) #adds LCD to the layout

        slider = QSlider() #creates the slider widget
        slider.setMinimum(0) #sets values to the slider
        slider.setMaximum(25)
        slider.setSingleStep(1)

        self.slider_timer = None  # Initialize the timer
        self.start_time = None  # Initialize the start time

        slider.valueChanged.connect(self.value_changed) #to display the speed on the LCD screen
        slider.sliderPressed.connect(self.slider_pressed_event) #to start the timer for the acceleration
        slider.sliderReleased.connect(self.slider_released_event) #to stop the timer for the acceleration

        layout.addWidget(slider) #adds slider to layout

        self.warning_label = QLabel() #creates a label widget
        layout.addWidget(self.warning_label) #adds widget to layout

        widget = QWidget() #all items under the class  
        widget.setLayout(layout) #applies the layout
        self.setCentralWidget(widget) #centers all the widgets

    def value_changed(self, i):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time #gets the time for
            product = i * elapsed_time #finds speed by mutiplying throttle percentage and time
            self.displayer.display(product)
            if i > 6: #warns the users if they are accelerating too fast (5 seconds to accelerate your vehicle up to 20 kilometres per hour from a stop)
                self.warning_label.setText("You are going too fast")
            else:
                self.warning_label.clear()           

    def slider_pressed_event(self):
        print("Slider pressed")
        self.start_time = time.time()
        self.slider_timer = QTimer()  # Create a QTimer for handling the time
        self.slider_timer.timeout.connect(self.print_elapsed_time)
        self.slider_timer.start(1000)  # Start the timer when the slider is pressed

    def slider_released_event(self):
        print("Slider released")
        if self.slider_timer is not None:
            self.slider_timer.stop()  # Stop the timer when the slider is released

    def print_elapsed_time(self): #Displays elasped time in the terminal
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            print(f"Elapsed Time: {elapsed_time:.2f} seconds")

app = QApplication(sys.argv) #creates the app
window = MainWindow() #creates the window of the app
window.show() #displays the app
app.exec() #start the event loop

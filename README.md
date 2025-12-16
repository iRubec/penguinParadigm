# penguinParadigm
 Gamified paradigm implemented in Python to study decision making under uncertain and volatile environments.

## Example of the paradigm
The paradigm has two different conditions:

**Reward condition**
https://github.com/user-attachments/assets/aa992158-853d-4e62-9ef3-3f94687203b9

**Punishment condition**
https://github.com/user-attachments/assets/b8128335-d4b2-4330-8446-d439319b5759



##  How to use it
To run the experiment, simply open a terminal in the desired condition and run the *main.py* script. The terminal will ask you to enter the name of the file to save the decisions of the participant: just enter the name and press *Enter*. Then, you will need to enter the contingency setting: A or B. Just enter the letter (in capital letter) and press *Enter* to select it. The game will then start.

##  What you will need...
This paradigm is designed to be used together with [BrainVision](https://brainvision.com/) EEG measure system. Therefore, you will need to have the [Cedrus c-pod](https://cedrus.com/support/c-pod/) marker sender connected to the computer in order to send the events that occur during the experiment to the [USB 2 Adapter](https://brainvision.com/product/usb-2-adapter-bua/), to be recorded togehter with the EEG signals by the [BrainVision Recorder](https://brainvision.com/product/recorder/). If it is not connected the paradigm will not work.

You will also need to have installed the following Puthon modules:
- [sys](https://docs.python.org/3/library/sys.html)
- [os](https://docs.python.org/3/library/os.html)
- [random ](https://docs.python.org/3/library/random.html)
- [pygame](https://www.pygame.org/news)
- [pandas](https://pandas.pydata.org/)
- [pyxid2](https://github.com/cedrus-opensource/pyxid)
- [pathlib](https://docs.python.org/3/library/pathlib.html)

## Contact
For any inquiry, please contact with [ruben.eguinoa@unavarra.es](mailto:ruben.eguinoa@unavarra.es)

# penguinParadigm
 Gamified paradigm implemented in Python to study decision making under uncertain and volatile environments.

## Example of the paradigm
The paradigm has two different conditions, separated in two folders:

| **Reward condition** | **Punishment condition** |
|----------------------|--------------------------|
| ![Reward](https://github.com/user-attachments/assets/f2933a7f-8d63-40cb-b546-880491626ab2) | ![Punishment](https://github.com/user-attachments/assets/5b1e74fe-d55a-4f4e-ba21-b1ebfbb8034f) |

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

## Acknowledgments
This research is supported by the Basque Government through the BERC 2022-2025 program and Funded by the Spanish State Research Agency through BCBL Severo Ochoa excellence accreditation CEX2020-001010/AEI/10.13039/501100011033 and through project PID2020-118829RB-I00 funded by the Spanish Ministry of Research and Innovation.

## Contact
For any inquiry, please contact with [ruben.eguinoa@unavarra.es](mailto:ruben.eguinoa@unavarra.es)

## Further information and Citation

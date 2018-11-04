# WIT-AI-Speech-to-Code

The overall idea is to record audio and save as a .wav file, then parse this audio file, and make requests to Wit.ai for each phrase to determine the code to write. Currently, acutally writing code is accomplished by keyboard commands from pynput.keyboard. For example, to save a completed written file:

            keyboard.press(Key.ctrl)
            keyboard.press('s')
            keyboard.release(Key.ctrl)
            keyboard.release('s')
            keyboard.type(name)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            
So, for demos and testing speech-to-code functionality, your cursor should be selected in any open text editor that you'd like to use. The application will directly insert text into whatever file you have open, and will save it according to verbal save commands.
            
Currently, speech_file.py iterates through several pre-recorded .wav files, provided in this repo, and writes text for each. Simply running speech_file.py with a text editor open should function for a demo. The file names in speech_file.py can be changed to test any .wav files. Additional audio files can be recorded by running test_file.py and following the prompt upon execution. text_file.py runs a demo using only a text file meant to simulate oral speech, initially intended for scenarios (such as noisy hackathons) where presentation with audio can be challenging.

To view the context-learning and phrase structure, or to try training on the model, the Wit.ai app is available here:
wit.ai/scglenn/MyFirstApp

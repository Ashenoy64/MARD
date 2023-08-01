Sure, here's an improved version of the README with more detailed information on getting started and the correct location for creating and instantiating custom plugins:

# MARD - Multi-Functional AI Robot with Raspberry Pi 5 and OpenAI

MARD (Multi-Functional AI Robot with Raspberry Pi 5 and OpenAI) is an exciting hardware project developed by Monish, Avanish, Ramesh, and Druva. This project utilizes a Raspberry Pi 5, an L298 motor driver, and the power of OpenAI to create an intelligent robot that can interact with users through speech, movement, and remote control. With the ability to process voice commands and provide responses, MARD offers an engaging and interactive experience.

## Features

- Speech Recognition: MARD is equipped with speech recognition capabilities. It can understand and respond to voice commands, making interactions more natural.

- Motor Control: The integration of the L298 motor driver allows MARD to move around freely, making it a fully mobile AI robot. Users can command it to go forward, backward, turn, and more.

- Web-Based Remote Control: MARD comes with a web-based remote control interface accessible through a webpage. Users can conveniently control the robot's movements remotely.

- Extensibility: The project is designed with extensibility in mind. Users can add custom plugins to enhance the bot's functionality further. Custom plugins can be easily created and integrated, expanding MARD's capabilities beyond its core features.

## Getting Started

To get started with MARD, follow these steps:

1. **Clone or Download**: You can either clone the MARD repository using Git or download the zip file from [https://github.com/Ashenoy64/MARD.git](https://github.com/Ashenoy64/MARD.git).

   ```bash
   # Clone the repository
   git clone https://github.com/Ashenoy64/MARD.git
   ```

   If you choose to download the zip file, extract it to your desired location.

2. **Install Dependencies**: Navigate to the project directory and install the required dependencies using `pip`.

   ```bash
   cd MARD
   pip install -r requirements.txt
   ```

   Make sure you have Python and `pip` installed on your system.

3. **Display Setup**: Set up the display for the bot by following the documentation provided at [https://learn.adafruit.com/monochrome-oled-breakouts/python-setup](https://learn.adafruit.com/monochrome-oled-breakouts/python-setup).

4. **Speech Model**: Obtain the speech model needed for speech recognition from [https://alphacephei.com/vosk/install](https://alphacephei.com/vosk/install).

5. **Run the Application**: Launch the application by running the following command:

   ```bash
   flask --app main.py run
   ```

## Custom Plugins

To create a custom plugin for MARD, you need to define your plugin class in the `AI.py` file. Below is the template for creating a custom plugin:

```python
class CustomPluginTemplate:
    def __init__(self):

        # When the user uses words similar to commandName, AI will call the function process
        self.commandName = ''

        # AI will gather data from the prompt given and pass it in this format
        self.inputFormat = ''

    def process(self, obj):
        # Perform your operation here
        pass
```

Once you have defined your custom plugin, you can instantiate it in the `AI.py` file and add it to the `pluginArray` of the `AI` class. Make sure to place the instantiation of the custom plugins above the `AIOBJ` object at the end of the `AI.py` file.

```python
# Instantiate your custom plugins here
customPlugin1 = CustomPluginTemplate()
customPlugin2 = CustomPluginTemplate()

# Add your custom plugins to the pluginArray
AIOBJ = AI(api_key_1="", api_key_2='', pluginArray=[Timer(), Task(), customPlugin1, customPlugin2])
```

By creating custom plugins and integrating them into MARD, you can extend the capabilities of the bot and customize its behavior according to your requirements.

MARD is an incredible showcase of how hardware and AI can merge to create an interactive and versatile robot. Feel free to explore the project, add your own custom plugins, and unleash the potential of this multi-functional AI robot!



## License

The MARD project is open-source and licensed under the [MIT License](LICENSE).

## Thank You for Exploring MARD!

We want to extend our sincere gratitude for checking out the MARD project. We hope you find it exciting and inspiring. If you have any feedback or suggestions, feel free to share them with us.

Happy coding and have a fantastic day!

---

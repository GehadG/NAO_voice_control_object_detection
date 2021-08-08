
# NAO_voice_control_object_detection
project for Robocup module at TU Berlin to control NAO robot using voice commands

![nao (1)](https://user-images.githubusercontent.com/13661852/128642713-66be2ab0-26ca-439c-9d5d-c92f82fec55e.png)
# Click on the image below to watch the demo video
[![Watch the video](https://img.youtube.com/vi/hWowrjhZa9M/maxresdefault.jpg)](https://youtu.be/hWowrjhZa9M)
## Problems faced :
Unfortunately webots doesn't support listening to voice commands
Therefore i had to use PyAudio

## Under the hood
#### Hotwords detection and voice commands
I used picovoice library for hotword detection and voice commands
they offer a portal to train ML models for these purposes
Unfortunately the Hotword detection free version is limited to 30 days
However they offer opensource pretrained hotwords that are unlimted.
Currently, the project support the following hotwords: Hey, neo ( limited to 30 days ) , Jarvis ( unlimted )

#### Commands format
Start by saying the Hotword ( currently configured to Hey, neo)
followed by that say any of the following sentences
the [] indicates that any of these words will be matched
the () indicates that this word is optional
the variable $color can be any of RED , BLUE , GREEN
the variable $direction can be FORWARD, BACKWARD, LEFT, RIGHT
```
[find, scan, look, search, detect, locate] (for) (a) (an) (the) $color:col (object)
[go, navigate] (to) (a) (an) (the) $color:col (object)
move $direction:dir
turn $direction:dir
```
For example :

1.Hey neo, go to the blue object

2.Hey neo , move forward

3.Hey neo , turn left

## How to run
1. open nao_voice_control.wbt in Webots
2. Install Requirements
```
pip install -r requirements.txt
```
3. add the required environment variables for webot to run : (see here: https://cyberbotics.com/doc/guide/using-your-ide)
4. install pyAudio ( see how to here :https://pythonprogramming.altervista.org/how-to-install-pyaudio/?doing_wp_cron=1628445951.2597301006317138671875 )
5. run the main python script
```
python main.py
```


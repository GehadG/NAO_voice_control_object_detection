
# NAO_voice_control_object_detection
project for Robocup module at TU Berlin to control NAO robot using voice commands

![nao (1)](https://user-images.githubusercontent.com/13661852/128642713-66be2ab0-26ca-439c-9d5d-c92f82fec55e.png)
# Click on the image below to watch the demo video
[![Watch the video](https://img.youtube.com/vi/hWowrjhZa9M/maxresdefault.jpg)](https://youtu.be/hWowrjhZa9M)

# Description:
Project scope was for the NAO robot to be able to interpret voice commands and act accordingly
Combined with object detection based on color, where the voice controlled NAO can perform the following tasks:
1. Scan the room for an object with a certain color
2. Locate and Move to an object
3. Basic mobility voice commands such as moving and turning to any direction.

## Plan
### Voice Detection
The plan was to make the NAO bot behave in a similar manner to Artificial assistants such as Alexa in terms of voice commands recognition.
Where the bot will continously process input audio from the microphone and use word spotting ( Hot words ) to trigger a command event.
My initial thought was to use the ALSpeechRecognition module with word spotting, however after a bit further investigation
i found that Webots doesn't support ALSpeechRecognition.

Given the need that the project would have to run on a simulated environment, i started looking into using the python speechrecognition library
However, it looked like it will also pose some limitiations, in terms of API limits. 
Which will not be optimal for word spotting, as we will have to always be listening and using the API to transcribe.

Which brought me to the final idea of training a ML model for hotwords detection
Before diving into training a model myself i had a look at some current services that handles the process.
The following 2 were investigated:
1. Snowboy
2. Picovice

Snowboy looked like a very promising solution that trains models for word spotting ( which will work 100% offline )
Unfortunately they were having troubles with their portal at the time of the project

To train the model with snowboy i had to upload a certain number of audio files containing the hotword.
I initially thought that i can use Google's Text to speech to generate the hotword in 300 different accents and pronounciation and use them to train the model.

However after further investigation, i found that Picovoice fully handles the training without the need to upload audio files.
Picovoice also offered a secondary service to handle commands recognition, so that was 2 birds with one stone.

### Object Recognition
Since i decided to use webots as a simulator
And one of the functionalities is Object detection, i utilized the camera recognition offered for the NAO simulator.

However since the commands that needed to be implemented includes moving towards the object when recognized,
I had to find a way to use the coordinates of the object in the camera to navigate the bot towards it.

```python
    def getObjectDetails(self, objectToParse):
        x = objectToParse.get_position()[0]
        y = objectToParse.get_position()[1]
        currentAngle = math.atan2(x, y)
        distance = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
        return x, y, distance, currentAngle
```

I defined the above function to give me 2 important parameters, which are the distance of the center of the object form the center of the camera
as well as the current angle the object is placed from the center of the camera.

The use of distance was pretty clear, once the distance is converging near 0 that means that the center of the object converging towards the center of the camera
Thus meaning that the bot should stop moving forward.

However using the angle provided from the camera was a bit tricky. however i utilized it in the following manner:
Key points to know , if the angle value is negative then the object is on the left of the bot
otherwise if positive, then the object was on the right of the bot.

The following flow was defined to detect the object and make it in the center of the camera :
1. Spin around the room until an object with color X is in the camera frame.
2. If the object is to the right ( angle is +ve ) spin to the right with very small angles till the angle of the object is (-ve) , and vice versa
3. The switch of angle from (+ve to -ve) or from (-ve to +ve) indicates that this object is now relatively in the center of the camera( it isn't 100% centered still, but that's good enough indicator)

Now we have the object relatively in the center, the following flow is defined to move towards the object:
1. Know the initial angle ( if positive or negative, i.e. if object is slightly on the left or slighly on the right)
2. Move forward
3. Check if angle of deviation from the object increased
4. If yes, then recenter the object
5. If no, repeat from step 2
6. If distance is converging to 0 , stop moving since the bot reached the object


## Problems faced :

Initially i experimented with Simspark and Choreograph to provide a simulated environment, however they aren't that well documented and then decided to use Webots.
Using Webots came with it's own disadvantages, such as not being able to use ALSpeechrecognition.

When intially planning to use python speechrecognition library, it posed an extra overhead of always having the bot connected to the internet for API usage, that's why i refrained from using it and started looking into the ML models approach.

How to utilize the coordinates of the object in the camera to transform them to be used in a 3D environment.

Webots demos had certain motions for movement, however the angles for turning for example wasn't really small, and i needed smaller angles for turning to tune in the object in the center of the camera


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

# How to run
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


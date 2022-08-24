update installed first
    apt-get update -y

installing pyttsx3, ubuntu 18.04

    - install espeak first
     sudo apt-get install espeak
     sudo apt-get install espeak -y

    - now install pyttsx3
     pip install pyttsx3
      more - https://pypi.org/project/pyttsx3/

install pyaudio
    pip install pyaudio

installing vosk
      python3 -m pip install https://github.com/alphacep/vosk-api/releases/download/0.3.21/vosk-0.3.21-py3-none-linux_aarch64.whl


mount dir to the container
    docker/run.sh  -v '/home/makini/jetson-voice/pipeline3.6:/jetson-voice/pipeline3.6'


errors :
    overflow on stt

sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
pip install pyaudio --user


#uninstall and install portaudioWhat you need to do:

Uninstall python-pyaudio with sudo apt-get purge --remove python-pyaudio if you have it (This is version 0.2.8)
Download the latest version (19) of PortAudio.
Untar and install PortAudio
./configure
make
make install
Get the dependencies for pyaudio
portaudio19-dev #sudo apt-get install portaudio19-dev
python-all-dev (python3-all-dev for Python 3) #sudo apt-get install python-all-dev
sudo pip install pyaudio

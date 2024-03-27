# How to run

This application is a mock code for Avatar AI using Python. The demo can be viewed on YouTube below.

https://youtu.be/peaXa7jJX4Q

## 1. Install and run VOICEBOX

https://voicevox.hiroshiba.jp/

## 2. Get ChatGPT API Key and set into environment variable

```commandline
export OPENAI_API_KEY=XXXXXXXXXXXXX
```

## 3. Set any video file

Please download `Nene.mp4` and `Rin.mp4` below and place them in your local folder.
https://drive.google.com/drive/folders/1ZMgW_9IsD_AHIlBWX6CNj8fHvbX_VAk1?usp=sharing

Configured the following.
Video is the location of the video file, name is the avatar's name, and speaker is the character's voice parameter. Speaker can be changed to other numbers.

```python
AVATAR_INFO = [
    {
        "video": "./Nene.mp4",
        "name": "ねね",
        "speaker": 60,
    },
    {
        "video": "./Rin.mp4",
        "name": "りん",
        "speaker": 10,
    }
]
```

## 4 Install lib on Mac 

```commandline
brew install portaudio
brew install espeak-ng
```

## 5. Install python packages

```commandline
pip3 install -r requirements.txt
```

## 6. Run

```commandline
python3 main.py
```
"""
Voice Module for dost.This module contains all the functions related to voice recognition and text to speech.

Examples:
    >>> import voice3
    >>> voice3.text_to_speech("Hello World")
    >>> voice3.speech_to_text()
    "Hello World"
    >>> voice3.text_to_speech_offline("Hello World")
    

This module contains the following functions:
        
- `text_to_speech(text)`: Converts text to speech.
- `speech_to_text()`: Converts speech to text.
- `text_to_speech_offline(text)`: Converts text to speech offline.

"""


from pathlib import WindowsPath
from dost.helpers import dostify
from dost.helpers import _is_speaker_available
is_speaker_connected = _is_speaker_available()


@dostify(errors=[(Exception, "Could not find PyAudio or no Microphone input device found. It may be being used by another application.")])
def _canonicalizePath(path: WindowsPath) -> WindowsPath:
    """Converts to absolute path and removes trailing slash
    Args:
        path (WindowsPath): Path to be canonicalized
    Returns:
        WindowsPath: Canonicalized path
    Examples:
        >>> _canonicalizePath(WindowsPath('C:\\Users\\'))
    """

    return str(path)


@dostify(errors=[(Exception, "Could not find PyAudio or no Microphone input device found. It may be being used by another application.")])
def playsound(sound, block: bool = True) -> None:
    """Plays the specified sound
    Args:
        sound (WindowsPath): Path to the sound
        block (bool): Whether to block the thread or not
    Examples:
        >>> playsound(WindowsPath('C:\\Users\\user\\Desktop\\sound.mp3'))
    """
    # Code Section
    sound = '"' + _canonicalizePath(sound) + '"'

    from ctypes import create_unicode_buffer, windll, wintypes
    from time import sleep
    windll.winmm.mciSendStringW.argtypes = [
        wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.UINT, wintypes.HANDLE]
    windll.winmm.mciGetErrorStringW.argtypes = [
        wintypes.DWORD, wintypes.LPWSTR, wintypes.UINT]

    def winCommand(*command):
        bufLen = 600
        buf = create_unicode_buffer(bufLen)
        command = ' '.join(command)
        # use widestring version of the function
        errorCode = int(windll.winmm.mciSendStringW(
            command, buf, bufLen - 1, 0))
        if errorCode:
            errorBuffer = create_unicode_buffer(bufLen)
            # use widestring version of the function
            windll.winmm.mciGetErrorStringW(errorCode, errorBuffer, bufLen - 1)
            exceptionMessage = ('\n    Error ' + str(errorCode) + ' for command:'
                                '\n        ' + command +
                                '\n    ' + errorBuffer.value)
            text_to_speech(exceptionMessage)
        return buf.value

    try:
        winCommand(u'open {}'.format(sound))
        winCommand(u'play {}{}'.format(sound, ' wait' if block else ''))
    finally:
        try:
            winCommand(u'close {}'.format(sound))
        except Exception:
            pass


@dostify(errors=[(Exception, "Could not find PyAudio or no Microphone input device found. It may be being used by another application.")])
def speech_to_text() -> str:
    """ 
    Converts speech to text
    Returns:
        string: Text from the speech
    Examples:
        >>> speech_to_text()
        "Hello World"
    """
    # Import Section
    import pyaudio
    import speech_recognition as sr
    import sys

    """
    Speech to Text using Google's Generic API
    """
    # Code Section
    recognizer = sr.Recognizer()
    energy_threshold = [3000]

    unknown = False
    data = None

    while True:
        with sr.Microphone() as source:
            recognizer.dynamic_energy_threshold = True
            if recognizer.energy_threshold in energy_threshold or recognizer.energy_threshold <= \
                    sorted(energy_threshold)[-1]:
                recognizer.energy_threshold = sorted(
                    energy_threshold)[-1]
            else:
                energy_threshold.append(
                    recognizer.energy_threshold)

            recognizer.pause_threshold = 0.8

            recognizer.adjust_for_ambient_noise(source)

            try:
                if not unknown:
                    text_to_speech("Speak now")
                audio = recognizer.listen(source)
                data = recognizer.recognize_google(audio)
            except AttributeError:
                text_to_speech(
                    "Could not find PyAudio or no Microphone input device found. It may be being used by "
                    "another "
                    "application.")
            except sr.UnknownValueError:
                unknown = True
            except sr.RequestError as e:
                print("Try Again")
    return data


@dostify(errors=[(Exception, "Could not find PyAudio or no Microphone input device found. It may be being used by another application.")])
def text_to_speech(audio, show: bool = True) -> None:
    """
    Converts text to speech
    Args:
        audio (string): Text to be converted to speech
        show (bool): Whether to print the text or not
    Examples:
        >>> text_to_speech("Hello World")
    """
    # Import Section
    import random
    import os

    # Code Section
    text_to_speech_offline(audio, show)


@dostify(errors=[(Exception, "Could not find PyAudio or no Microphone input device found. It may be being used by another application.")])
def text_to_speech_offline(audio, show: bool = True, rate: int = 170) -> None:
    """
    Converts text to speech offline
    Args:
        audio (string): Text to be converted to speech
        show (bool): Whether to print the text or not
        rate (int): Rate of speech. Default is 170
    Examples:
        >>> text_to_speech_offline("Hello World")
    """
    # Import Section
    import random
    import pyttsx3
    import sys

    # Code Section
    if is_speaker_connected:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        voice = random.choice(voices)  # Randomly decide male/female voice
        engine.setProperty('voice', voice.id)

        engine.setProperty('rate', rate)
        engine.say(audio)
        engine.runAndWait()

    if type(audio) is list:
        if show:
            print(' '.join(audio))
    else:
        if show:
            print(str(audio))

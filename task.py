import pygame
import time
import argparse
import random
import sounddevice as sd
import soundfile as sf
import numpy as np
from datetime import datetime


pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Vocab Learning task")
font = pygame.font.SysFont(None, 60)

kor_to_eng = {'One(il)': "one", "Two(i)": "two", "Three(sam)": "three", 'Four(sa)': "four", "Five(o)": "five"}

# render fixation cross
def show_fixation(first=False, color=(255, 255, 255)):
    cross = font.render('+', True, color)
    cross_rect = cross.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.fill((0, 0, 0))
    screen.blit(cross, cross_rect)
    pygame.display.flip()
    
    if first:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return
                
def record_audio(samplerate=44100, channels=1):
    audio_data = []
    # Callback function to capture audio data
    def callback(indata, frames, time, status):
        audio_data.extend(indata.copy())
    # Open the audio input stream, keep open until closed
    stream = sd.InputStream(samplerate=samplerate, channels=channels, callback=callback)
    return stream, audio_data

def run_task():
    running = True
    data = []
    # TODO: change to be < 5min per block
    num_trials = 5
    for i in range(num_trials):
        show_fixation(first=True)
        show_fixation(False, (0, 255, 0))

        # choose one of the stimuli randomly and play it
        stim = random.choice(["One(il)", "Two(i)", "Three(sam)", 'Four(sa)', "Five(o)"])
        pygame.mixer.init()
        pygame.mixer.music.load(f"stimuli/{stim}.wav")
        pygame.mixer.music.play()

        # start recording
        # stream, audio_data = record_audio()
        # stream.start()

        trial_active = True
        spaces = 0
        while trial_active:
            for event in pygame.event.get():
                # stop recording if they've pressed any of the keys (will count that as an incorrect response)
                # stream.stop()
                # stream.close()
                # audio_array = np.array(audio_data)
                # dt = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                # sf.write(f'{dt}.wav', audio_array, samplerate=44100)

                if event.type == pygame.KEYDOWN:
                    # SPACE if the subject needs to hear the answer
                    # NOTE: can do a version where the subject can play the answer as many times as they want
                    if event.key == pygame.K_SPACE:
                        spaces += 1
                        ans = kor_to_eng[stim]
                        pygame.mixer.music.load(f"stimuli/{ans}.wav")
                        pygame.mixer.music.play()
                    # ENTER if the subject thinks they know the answer
                    # NOTE: option to have them say the answer or not
                    elif event.key == pygame.K_RETURN:
                        trial_active = False
                elif event.type == pygame.QUIT:
                    trial_active = False
                    running = False

        pygame.display.flip()

        if not running:
            break

    pygame.quit()


def main():
    # parser = argparse.ArgumentParser(description='Run different versions of a script with a flag')
    # args = parser.parse_args()

    run_task()

if __name__ == "__main__":
    main()
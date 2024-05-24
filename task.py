import pygame
import time
import argparse
import random
import sounddevice as sd
import soundfile as sf
import numpy as np
from datetime import datetime
from pynput.keyboard import Listener


pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Vocab Learning task")
font = pygame.font.SysFont(None, 60)

kor_to_eng = {'One(il)': "one", "Two(i)": "two", "Three(sam)": "three", 'Four(sa)': "four", "Five(o)": "five"}

# render fixation cross
def show_fixation(duration, color):
    cross = font.render('+', True, color)
    cross_rect = cross.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.fill((0, 0, 0))
    screen.blit(cross, cross_rect)
    pygame.display.flip()
    time.sleep(duration)
                
def record_audio(samplerate=44100, channels=1):
    audio_data = []
    # Callback function to capture audio data
    def callback(indata, frames, time, status):
        audio_data.extend(indata.copy())
    # Open the audio input stream, keep open until closed
    stream = sd.InputStream(samplerate=samplerate, channels=channels, callback=callback)
    return stream, audio_data

def run_task():
    screen.fill((0, 0, 0))

    # press any key to start
    def on_press(key):
        # print(f'{key} pressed')
        return False  # stop listener

    with Listener(on_press=on_press) as listener:
        listener.join()

    running = True
    data = []
    num_trials = 5

    for i in range(num_trials):
        # show white fixation cross
        show_fixation(duration=1, color=(255, 255, 255))

        # choose one of the stimuli randomly and play it
        stim = random.choice(["One(il)", "Two(i)", "Three(sam)", 'Four(sa)', "Five(o)"])
        pygame.mixer.init()
        pygame.mixer.music.load(f"stimuli/{stim}.wav")
        pygame.mixer.music.play()
        show_fixation(duration=3, color=(255, 0, 0))

        # start recording
        # stream, audio_data = record_audio()
        # stream.start()

        trial_active = True
        # stim_repeats = 0
        # ans_plays = 0
        while trial_active:
            # prompt subject to answer
            show_fixation(duration=5, color=(0, 255, 0))
            trial_active = False
            for event in pygame.event.get():
            #     # stop recording if they've pressed any of the keys (will count that as an incorrect response)
            #     # stream.stop()
            #     # stream.close()
            #     # audio_array = np.array(audio_data)
            #     # dt = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            #     # sf.write(f'{dt}.wav', audio_array, samplerate=44100)

            #     if event.type == pygame.KEYDOWN:
            #         # SPACE if the subject needs to hear the answer
            #         # NOTE: can do a version where the subject can play the answer as many times as they want
            #         if event.unicode == 'r':
            #             stim_repeats += 1
            #             pygame.mixer.music.load(f"stimuli/{stim}.wav")
            #             pygame.mixer.music.play()
            #         elif event.key == pygame.K_SPACE:
            #             ans_plays += 1
            #             ans = kor_to_eng[stim]
            #             pygame.mixer.music.load(f"stimuli/{ans}.wav")
            #             pygame.mixer.music.play()
            #         # ENTER if the subject thinks they know the answer
            #         # NOTE: option to have them say the answer or not
            #         elif event.key == pygame.K_RETURN:
            #             trial_active = False
                if event.type == pygame.QUIT:
                    trial_active = False
                    running = False

        pygame.display.flip()

        # play correct answer
        ans = kor_to_eng[stim]
        pygame.mixer.music.load(f"stimuli/{ans}.wav")
        pygame.mixer.music.play()
        show_fixation(duration=3, color=(255, 0, 0))

        if not running:
            break

    pygame.quit()


def main():
    # parser = argparse.ArgumentParser(description='Run different versions of a script with a flag')
    # args = parser.parse_args()

    run_task()

if __name__ == "__main__":
    main()
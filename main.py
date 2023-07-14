import pygame
from pygame import mixer
from mutagen.mp3 import MP3
import os
import time

pygame.init()
mixer.init()

pygame.display.set_caption("Music Player")

WINDOW_WIDTH, WINDOW_HEIGHT = 500, 300
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
PRIMARY_COLOR = (244, 81, 30)
SECONDARY_COLOR = (0, 170, 255)

FONT_SMALL = pygame.font.SysFont("Arial", 16)
FONT_MEDIUM = pygame.font.SysFont("Arial", 20, bold=True)

# Directory containing the music files
CURRENT_DIRECTORY = os.getcwd()

# Specify the music directory path
MUSIC_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "music")

# load and play a music file
def play_music(file_path):
    mixer.music.load(file_path)
    mixer.music.play()

# pause
def pause_music():
    mixer.music.pause()

# resume
def resume_music():
    mixer.music.unpause()

# stop
def stop_music():
    mixer.music.stop()

def get_music_duration(file_path):
    audio = MP3(file_path)
    return audio.info.length

def format_duration(duration):
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    return f"{minutes:02d}:{seconds:02d}"

def display_song_info(file_path):
    song_name = os.path.basename(file_path)
    duration = get_music_duration(file_path)
    duration_str = format_duration(duration)

    song_label = FONT_MEDIUM.render(song_name, True, BLACK)
    duration_label = FONT_SMALL.render(duration_str, True, GRAY)

    window.fill(WHITE)
    window.blit(song_label, (20, 20))
    window.blit(duration_label, (20, 60))
    pygame.display.update()

def handle_button_click(button_rect, file_path):
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        if file_path:
            display_song_info(file_path)
            play_music(file_path)
        else:
            stop_music()

def main():
    music_files = os.listdir(MUSIC_DIRECTORY)
    music_files = [file for file in music_files if file.endswith(".mp3")]

    buttons = []
    button_y = 100
    button_width = 150
    button_height = 40
    button_margin = 20

    for music_file in music_files:
        button_x = (WINDOW_WIDTH - button_width) // 2
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        button = {
            "rect": button_rect,
            "file_path": os.path.join(MUSIC_DIRECTORY, music_file)
        }
        buttons.append(button)
        button_y += button_height + button_margin

    clock = pygame.time.Clock()
    running = True

    # Create buttons
    stop_button_rect = pygame.Rect(350, 250, 100, 30)
    play_button_rect = pygame.Rect(350, 200, 100, 30)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    handle_button_click(button["rect"], button["file_path"])
                handle_button_click(stop_button_rect, None)
                handle_button_click(play_button_rect, buttons[0]["file_path"])  # Play the first song by default

        window.fill(WHITE)

        # Draw buttons
        for button in buttons:
            pygame.draw.rect(window, PRIMARY_COLOR, button["rect"])
            button_name = os.path.basename(button["file_path"])
            button_label = FONT_SMALL.render(button_name, True, BLACK)
            button_label_pos = button["rect"].center
            button_label_pos = (button_label_pos[0] - button_label.get_width() // 2, button_label_pos[1] - button_label.get_height() // 2)
            window.blit(button_label, button_label_pos)

        pygame.draw.rect(window, PRIMARY_COLOR, stop_button_rect)
        stop_label = FONT_SMALL.render("Stop", True, BLACK)
        stop_label_pos = stop_button_rect.center
        stop_label_pos = (stop_label_pos[0] - stop_label.get_width() // 2, stop_label_pos[1] - stop_label.get_height() // 2)
        window.blit(stop_label, stop_label_pos)

        pygame.draw.rect(window, PRIMARY_COLOR, play_button_rect)
        play_label = FONT_SMALL.render("Play", True, BLACK)
        play_label_pos = play_button_rect.center
        play_label_pos = (play_label_pos[0] - play_label.get_width() // 2, play_label_pos[1] - play_label.get_height() // 2)
        window.blit(play_label, play_label_pos)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

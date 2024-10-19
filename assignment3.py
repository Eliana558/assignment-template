import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine, Square
import random
import pygame

# Define C major, E major, G major, and A major scales
C_MAJOR_SCALE = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]  # C4, D4, E4, F4, G4, A4, B4
E_MAJOR_SCALE = [329.63, 392.00, 440.00, 493.88, 554.37, 587.33, 659.25]  # E4, F#4, G#4, A4, B4, C#5, D#5
G_MAJOR_SCALE = [392.00, 440.00, 493.88, 523.25, 587.33, 659.25, 698.46]  # G4, A4, B4, C5, D5, E5, F#5
A_MAJOR_SCALE = [440.00, 493.88, 554.37, 587.33, 659.25, 698.46, 783.99]  # A4, B4, C#5, D5, E5, F#5, G#5

# Map each MBTI type to a specific scale
mbti_to_scale = {
    'INTJ': C_MAJOR_SCALE,
    'INTP': C_MAJOR_SCALE,
    'ENTJ': G_MAJOR_SCALE,
    'ENTP': G_MAJOR_SCALE,
    'INFJ': E_MAJOR_SCALE,
    'INFP': E_MAJOR_SCALE,
    'ENFJ': A_MAJOR_SCALE,
    'ENFP': A_MAJOR_SCALE,
    'ISTJ': C_MAJOR_SCALE,
    'ISFJ': C_MAJOR_SCALE,
    'ESTJ': G_MAJOR_SCALE,
    'ESFJ': G_MAJOR_SCALE,
    'ISTP': E_MAJOR_SCALE,
    'ISFP': E_MAJOR_SCALE,
    'ESTP': A_MAJOR_SCALE,
    'ESFP': A_MAJOR_SCALE,
}

# Function to generate music based on MBTI type and age
def generate_music(mbti, age):
    scale = mbti_to_scale.get(mbti.upper(), C_MAJOR_SCALE)  # Default to C major if MBTI is unknown

    # Adjust the tempo (speed) based on age
    if age < 20:
        tempo = 220  # Faster tempo
    elif 20 <= age < 40:
        tempo = 180  # Moderate-fast tempo
    else:
        tempo = 140  # Slower tempo

    duration = 600  # Duration of each note in milliseconds
    segment = Sine(random.choice(scale)).to_audio_segment(duration=duration)  # Start with a random note

    # Generate random chords and add them to the music segment
    num_chords = random.randint(3, 5)  # Randomly generate between 3 to 5 chords
    for _ in range(num_chords):
        chord_notes = [random.choice(scale) for _ in range(3)]  # Randomly choose 3 notes from the scale
        chord = sum(Sine(note).to_audio_segment(duration=duration) for note in chord_notes)  # Create a chord
        segment += chord

    # Generate additional random notes to make the music more varied
    num_notes = random.randint(15, 25)  # Generate a random number of additional notes
    for _ in range(num_notes):
        random_pitch = random.choice(scale)  # Randomly choose a pitch from the selected scale
        wave_type = random.choice([Sine, Square])  # Randomly choose a wave type (sine or square)
        note = wave_type(random_pitch).to_audio_segment(duration=duration)  # Generate the note
        
        # Add a small random variation in volume
        volume_change = random.uniform(-1, 1)
        note = note + volume_change
        
        segment += note

    # Adjust the playback speed to match the selected tempo
    segment = segment.speedup(playback_speed=tempo / 100.0)

    return segment

# Function to add an echo effect to the audio
def add_echo(audio_segment, delay=100, decay=0.3):
    echo = audio_segment + AudioSegment.silent(duration=delay)  # Create initial delay
    for _ in range(2):  # Overlay the echo 2 times
        echo = echo.overlay(audio_segment - (5 * decay), position=delay)  # Reduce volume for each echo
        delay += int(delay * decay)  # Increase the delay for each successive echo

    return echo

# Function to play the generated music using pygame
def play_music(filename):
    pygame.mixer.init()  # Initialize the mixer module in pygame
    pygame.mixer.music.load(filename)  # Load the audio file
    pygame.mixer.music.play()  # Play the loaded audio file
    while pygame.mixer.music.get_busy():  # Keep the program running while music is playing
        pygame.time.Clock().tick(10)

# Function to save the generated music to a file
def save_music(mbti, age, filename="generated_music.wav"):
    music = generate_music(mbti, age)  # Generate the music segment
    music_with_echo = add_echo(music)  # Add echo effect to the music
    music_with_echo.export(filename, format="wav")  # Export the music to a wav file
    print(f"Music generated and saved as {filename}")
    play_music(filename)  # Play the saved music file

# Main execution block to prompt user for MBTI type and age, then generate music
if __name__ == "__main__":
    mbti = input("Enter MBTI type (e.g., INTJ, ENFP): ").strip()  # Get MBTI type from user
    age = int(input("Enter age: ").strip())  # Get age from user

    save_music(mbti, age)  # Generate and save the music based on user input

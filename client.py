# Importing the necessary libraries
import socket, pygame, os, time, ftplib, ntpath
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pygame import mixer
from playsound import playsound
from ftplib import FTP
from pathlib import Path

# Declaring the global variables
IP_ADDRESS = '127.0.0.1'
PORT = 8000
BUFFER_SIZE = 4096
SERVER = None

# Creating more global variables
songs_listbox = None
info_label = None
song_counter = 0
song_selected = None
filePathLabel = None

# Function to browse files
def browseFiles():
    global songs_listbox
    global song_counter
    global filePathLabel

    try:
        # Creating the file dialog object for browsing the MP3, WAV, OGG files
        filename = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")])

        # FTP Credentials to connect to the FTP Server
        HOSTNAME = "127.0.0.1"
        USERNAME = "lftpd"
        PASSWORD = "lftpd"

        # Connecting to the FTP Server and uploading the song file(s)
        ftp_server = FTP(HOSTNAME, USERNAME, PASSWORD)
        ftp_server.encoding = 'utf-8'
        fname = ntpath.basename(filename)
        with open(filename, 'rb') as file:
            ftp_server.storbinary(f'STOR {fname}', file)
        ftp_server.dir()
        ftp_server.quit()

        # Inserting the songs into the listbox
        songs_listbox.insert(song_counter, fname)
        song_counter += 1
    except FileNotFoundError:
        print("File Dialog has been closed without selecting any file")

# Function to download the songs
def download():
    # Getting the selected song from the listbox to download
    song_to_download = songs_listbox.get(ANCHOR)
    info_label.config(text=f"Downloading {song_to_download}")

    # FTP Credentials to connect to the FTP Server
    HOSTNAME = "127.0.0.1"
    USERNAME = "lftpd"
    PASSWORD = "lftpd"

    # Navigating to the Downloads directory of the user and downloading the song file(s) from the FTP Server
    home = str(Path.home())
    download_path = f"{home}/Downloads"
    ftp_server = FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp_server.encoding = 'utf-8'
    local_filename = os.path.join(download_path, song_to_download)
    file = open(local_filename, 'wb')
    ftp_server.retrbinary(f'RETR {song_to_download}', file.write)
    ftp_server.dir()
    file.close()
    ftp_server.quit()

    # Displaying the information in the info label
    info_label.config(text=f"Downloaded {song_to_download} to {download_path}")
    
    # Changing the information in the info label after 5 seconds
    time.sleep(5)
    if(song_selected != None):
        info_label.config(text=f"Playing {song_selected}")
    else:
        info_label.config(text="Please select a song to play")

# Function to play the songs
def play():
    # Declaring the required global variables
    global song_selected
    global songs_listbox

    # Getting the selected song from the listbox
    song_selected = songs_listbox.get(ANCHOR)

    # Playing the selected song
    pygame
    mixer.init()

    # FTP Credentials to connect to the FTP Server
    HOSTNAME = "127.0.0.1"
    USERNAME = "lftpd"
    PASSWORD = "lftpd"
    
    # Navigating to the shared_files directory of the user and playing the song file(s)
    ftp_server = FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp_server.encoding = 'utf-8'
    if not os.path.exists("shared_files_temp"):
        os.makedirs("shared_files_temp")
    local_filename = os.path.join("shared_files_temp", song_selected)
    file = open(local_filename, 'wb')
    ftp_server.retrbinary(f'RETR {song_selected}', file.write)
    ftp_server.dir()
    file.close()
    ftp_server.quit()

    # Playing the song
    mixer.music.load(local_filename)
    mixer.music.play()

    if(song_selected != None):
        info_label.config(text=f"Playing {song_selected}")
    else:
        info_label.config(text="Please select a song to play")

# Function to stop the songs
def stop():
    # Declaring the required global variables
    global song_selected
    
    # Stopping the selected song
    pygame
    mixer.init()
    mixer.music.stop()
    mixer.music.unload()
    info_label.config(text=f"Stopped {song_selected}")

    # Deleting the temporary directory along with the song file
    if os.path.exists("shared_files_temp"):
        os.remove(f"shared_files_temp/{song_selected}")
        os.rmdir("shared_files_temp")

# Function to pause the songs
def pause():
    # Declaring the required global variables
    global song_selected
    
    # Pausing the selected song
    pygame
    mixer.init()
    mixer.music.pause()
    info_label.config(text=f"Paused {song_selected}")

# Function to resume the songs
def resume():
    # Declaring the required global variables
    global song_selected
    
    # Resuming the selected song
    pygame
    mixer.init()
    mixer.music.unpause()
    info_label.config(text=f"Resumed {song_selected}")

# Creating the GUI for the music window
def musicWindow():
    # Declaring the global variables
    global song_counter
    global songs_listbox
    global info_label

    # Creating a new window
    music_window = Tk()

    # Setting the title of the window
    music_window.title("Music Player")

    # Setting the geometry of the window
    music_window.geometry('300x350')
    
    # Setting the background of the window
    music_window.configure(bg='LightSkyBlue')

    # Creating a label for the select song option
    select_song_label = Label(music_window, text="Select Song", bg='LightSkyBlue', font=('Calibri', 8))
    select_song_label.place(x=2, y=1)

    # Creating a listbox widget to display the songs
    songs_listbox = Listbox(music_window, width=39, height=10, activestyle='dotbox', bg='LightSkyBlue', borderwidth=2, font=('Calibri', 10))
    songs_listbox.place(x=10, y=18)

    # Getting music files from the system
    #for file in os.listdir('shared_files'):
    #    filename = os.fsdecode(file)
    #    songs_listbox.insert(song_counter, filename)
    #    song_counter += 1

    # Getting music files from the FTP Server
    HOSTNAME = "127.0.0.1"
    USERNAME = "lftpd"
    PASSWORD = "lftpd"
    ftp_server = FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp_server.encoding = 'utf-8'
    ftp_server.dir()
    files = ftp_server.nlst()
    for file in files:
        songs_listbox.insert(song_counter, file)
        song_counter += 1
    ftp_server.quit()

    # Creating a scrollbar for the listbox
    scrollbar = Scrollbar(songs_listbox)
    scrollbar.place(relheight=1, relx=1)
    scrollbar.config(command=songs_listbox.yview)

    # Creating a button to play the selected song
    play_button = Button(music_window, text="Play", width=10, bd=1, bg='SkyBlue', font=('Calibri', 10), command=play)
    play_button.place(x=30, y=200)

    # Creating a button to stop the selected song
    stop_button = Button(music_window, text="Stop", width=10, bg='SkyBlue', font=('Calibri', 10), command=stop)
    stop_button.place(x=200, y=200)

    # Creating a button to resume the selected song
    resume_button = Button(music_window, text="Resume", width=10, bd=1, bg='SkyBlue', font=('Calibri', 10), command=resume)
    resume_button.place(x=30, y=300)

    # Creating a button to pause the selected song
    pause_button = Button(music_window, text="Pause", width=10, bd=1, bg='SkyBlue', font=('Calibri', 10), command=pause)
    pause_button.place(x=200, y=300)

    # Creating a button to upload the song
    upload_button = Button(music_window, text="Upload", width=10, bd=1, bg='SkyBlue', font=('Calibri', 10), command=browseFiles)
    upload_button.place(x=30, y=250)

    # Creating a button to download the song
    download_button = Button(music_window, text="Download", width=10, bd=1, bg='SkyBlue', font=('Calibri', 10), command=download)
    download_button.place(x=200, y=250)

    # Creating an info label
    info_label = Label(music_window, text="", fg='Blue', font=('Calibri', 8))
    info_label.place(x=4, y=330)

    # Running the main loop
    music_window.mainloop()

# Setup function to initialize the client
def setup():
    # Getting the global variables along with its values
    global SERVER
    global IP_ADDRESS
    global PORT

    # Creating a socket for the client
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connecting the client to the server
    SERVER.connect((IP_ADDRESS, PORT))

    # Calling the music window function
    musicWindow()

# Running the setup function
setup()
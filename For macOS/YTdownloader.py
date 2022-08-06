import tkinter, time, threading, os, urllib, socket
from tkinter import filedialog
from pytube import YouTube, exceptions
import Utilities # My Utilities file


root = tkinter.Tk()
root.title("YouTube Downloader")
root.resizable(False, False)


# Define methods:
def ThreadDownload(link):
    try:
        video = YouTube(link)
    except exceptions.RegexMatchError:
        LinkEntry.EnableClearInsertDisable("Please enter a valid YouTube link.")
        Utilities.UnGrid([ButtonDownload, ButtonFolder, ChooseType])
        time.sleep(10)
        LinkEntry.EnableClear()
        ChooseType.grid(row=2, column=1)
        ButtonFolder.grid(row=2, column=0)
        return
    global FolderLocation
    def ShowDownload():
        LinkEntry.EnableClearInsertDisable("downloading...")
        Utilities.UnGrid([ButtonDownload, ButtonFolder, ChooseType])
        ButtonQuit.config(text="Stop & Exit")
    try:
        if chosen.get() == typeOptions[0]:
            ShowDownload()
            video.streams.get_highest_resolution().download(FolderLocation)
            # extension = '.mp4'
        elif chosen.get() == typeOptions[1]:
            ShowDownload()
            des = video.streams.get_audio_only().download(FolderLocation)
            os.rename(des, des[:len(des) - 3] + "mp3")
            # extension = '.mp3'
        else: return # when no type was chosen
    except urllib.error.URLError or socket.gaierror: # Changed
        LinkEntry.EnableClearInsertDisable("No internet connection!")
        Utilities.UnGrid([ButtonDownload, ButtonFolder, ChooseType])
        ButtonQuit.config(text="Exit")
        time.sleep(15)
        ChooseType.grid(row=2, column=1)
        ButtonFolder.grid(row=2, column=0)
        LinkEntry.EnableClear()
        return
    LinkEntry.EnableClear()
    ButtonFolder.grid(row=2, column=0)
    ChooseType.grid(row=2, column=1)
    FinishedLabel.config(text="Finished downloading\n\"{}\"\nas {}".format(video.title, chosen.get().lower()[:5]))
    FinishedLabel.grid(row=5, columnspan=2)
    ButtonQuit.config(text="Exit")
    ButtonQuit.grid(row= 4,columnspan=2)
    # print("Size - " + str(os.path.getsize(FolderLocation + '/' + video.title + extension)) + " bytes")
    time.sleep(15)
    Utilities.UnGrid([FinishedLabel])

def MainDownload():
    thread = threading.Thread(target=lambda:ThreadDownload(LinkEntry.get()), daemon=True)
    thread.start()

def ChooseFolder():
    global FolderLocation
    root.filename = filedialog.askdirectory(initialdir="/Users/omri/Downloads")
    FolderLocation = root.filename
    if FolderLocation != '':
        for i in range(len(FolderLocation)):
            if FolderLocation[i] == '/':
                index = i
        ButtonDownload.config(text="Download file in \"{}\"".format(FolderLocation[index + 1:]))
        Utilities.UnGrid([ButtonQuit])
        #ButtonQuit.grid_forget()
        ButtonDownload.grid(row=3, columnspan=2, pady=5)
        ButtonQuit.grid(row= 4,columnspan=2)

# Define & create widgets:
EnterLinkLabel = tkinter.Label(root ,text="Enter link:", fg="red", font=("", 15))
LinkEntry = Utilities.Entry(root, width=25)

chosen = tkinter.StringVar()
chosen.set("Choose type")
typeOptions = ["Video (mp4)", "Audio (mp3)"]
ChooseType = tkinter.OptionMenu(root, chosen, *typeOptions)

ButtonDownload = tkinter.Button(root, fg="#FF0000", command=MainDownload)
FinishedLabel = tkinter.Label(root)
ButtonQuit = tkinter.Button(root, text="Exit", command=root.quit)
ButtonFolder = tkinter.Button(root, text="Choose folder", command=ChooseFolder)

# Add widgets:
EnterLinkLabel.grid(row= 0,columnspan=2)
LinkEntry.grid(row= 1,columnspan=2)
ChooseType.grid(row=2, column=1)
ButtonFolder.grid(row=2, column=0)
ButtonQuit.grid(row= 4,columnspan=2)


root.eval("tk::PlaceWindow . center")
root.mainloop()
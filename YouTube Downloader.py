import tkinter, time, threading, os, urllib, socket, pathlib, sys
from tkinter import filedialog, ttk
from pytube import YouTube, exceptions
import Utilities


root = tkinter.Tk()
root.title("YouTube Downloader")
root.iconbitmap(sys.argv[0])
root.resizable(False, False)


# Define methods:
def ThreadDownload(link):
    global FolderLocation
    try:
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
        def ShowDownload():
            LinkEntry.EnableClearInsertDisable("downloading...")
            Utilities.UnGrid([ButtonDownload, ButtonFolder, ChooseType])
            ButtonQuit.config(text="Stop & Exit")
        try:
            if chosen.get() == typeOptions[0]:
                ShowDownload()
                video.streams.get_highest_resolution().download(FolderLocation)
            elif chosen.get() == typeOptions[1]:
                ShowDownload()
                des = video.streams.get_audio_only().download(FolderLocation)
                os.rename(des, des[:len(des) - 3] + "mp3")
            else: return # when no type was chosen 
        except urllib.error.URLError or socket.gaierror:
            LinkEntry.EnableClearInsertDisable("Internet disconnected!")
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
        FinishedLabel.config(text=f"Finished downloading\n\"{video.title}\"\nas {chosen.get().lower()[:5]}")
        FinishedLabel.grid(row=5, columnspan=2)
        ButtonQuit.config(text="Exit")
        ButtonQuit.grid(row= 4,columnspan=2)
        time.sleep(15)
        Utilities.UnGrid([FinishedLabel])
    except Exception:
        Utilities.UnGrid([ButtonDownload, ButtonFolder, ChooseType])
        LinkEntry.EnableClearInsertDisable("Something went wrong!")

def MainDownload():
    thread = threading.Thread(target=lambda:ThreadDownload(LinkEntry.get()), daemon=True)
    thread.start()

def ChooseFolder():
    global FolderLocation
    root.filename = filedialog.askdirectory(initialdir=f"{pathlib.Path.home()}\\Downloads")
    FolderLocation = root.filename
    if FolderLocation != '':
        for i in range(len(FolderLocation)):
            if FolderLocation[i] == '/':
                index = i
        ButtonDownload.config(text=f"Download file in\n{FolderLocation[index + 1:]}")
        Utilities.UnGrid([ButtonQuit])
        ButtonDownload.grid(row=3, columnspan=2, pady=6)
        ButtonQuit.grid(row= 4,columnspan=2)

# Define & create widgets:
EnterLinkLabel = tkinter.Label(root ,text="Enter link:", fg="red", font=("Aharoni", 18), width=20)
LinkEntry = Utilities.Entry(root, width=37, fg="crimson", bg="White", font="Gisha 10")

chosen = tkinter.StringVar()
chosen.set("Choose type")
typeOptions = ["Video (mp4)", "Audio (mp3)"]
#ChooseType = tkinter.OptionMenu(root, chosen, *typeOptions)
ChooseType = ttk.Combobox(root, textvariable=chosen, values=typeOptions, state="readonly", width=15)


ButtonDownload = tkinter.Button(root, fg="#cf352e", bg="White", font="Aharoni 10", command=MainDownload)
FinishedLabel = tkinter.Label(root)
ButtonQuit = tkinter.Button(root, text="Exit", command=root.quit, pady=1, font="Aharoni 12")
ButtonFolder = tkinter.Button(root, text="Choose folder", command=ChooseFolder, font="Aharoni 10", width=14)

# Add widgets:
EnterLinkLabel.grid(row= 0,columnspan=2)
LinkEntry.grid(row= 1,columnspan=2)
ChooseType.grid(row=2, column=1, pady=5)
ButtonFolder.grid(row=2, column=0, pady=5)
ButtonQuit.grid(row= 4,columnspan=2, pady=2)


root.eval("tk::PlaceWindow . center")
root.mainloop()

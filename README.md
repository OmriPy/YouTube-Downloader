## NOTE
Unfortunately the app doesn't work due to the fact that the `pytube` module isn't supported anymore.

# YouTube-Downloader

## Preparation
In order for the code to work properly, open Command Prompt (for Windows) or Terminal (macOS) and type this line:
```
pip3 install pytube
```
This command simply downloads the Pytube module.
## Note for Windows users:
On line 9:
```py
root.iconbitmap(sys.argv[0])
```
I put:
```py
sys.argv[0]
```
Becuase I wanted to make the code an executable file (an app) so I will have it in my Taskbar. When I built the app using Command Prompt I gave cmd the path to the icon I wanted the app to have.

So if you don't want an icon you can remove that line or if you want an icon type:
```py
root.iconbitmap()
```
And put the full path to the icon inside the parentheses.

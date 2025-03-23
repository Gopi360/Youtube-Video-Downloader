import yt_dlp
link = input("Enter a yt link: ")
yt_dlp.YoutubeDL({'format':'best','outtmpl': '%(title)s.%(ext)s'}).download([link])
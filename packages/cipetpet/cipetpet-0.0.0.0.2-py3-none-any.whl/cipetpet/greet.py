
def SayHello():
    import vlc
    import pafy
    
    url = "https://www.youtube.com/watch?v=WpKiG413FXk&ab_channel=GoldPunch"
    
    video = pafy.new(url)
    best = video.getbest()
    media = vlc.MediaPlayer(best.url)
    media.play()
    return
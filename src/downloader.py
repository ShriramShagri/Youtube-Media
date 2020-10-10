import pafy

class Manager:
    def __init__(self, url):
        self.video = pafy.new(url)
        self.url = url
    
    def getDetails(self):
        return self.video
    
    def getAudioStream(self):
        return self.video.audiostreams
    
    def getVideoStream(self):
        return self.video.videostreams
    
    def getAllStream(self):
        return self.video.streams
    
    def downloadAudio(self, stream):
        stream.download()
    
    def downloadVideo(self, stream):
        stream.download()
    
    def downloadAll(self, stream):
        stream.download()
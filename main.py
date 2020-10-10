import src

url = ''

m = src.Manager(url)

print(m.getAudioStream()[-1])
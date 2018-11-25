import sounddevice as sd
sd.default.samplerate = 8000
sd.default.device = 14,3
print(sd.default.device)
print("*recording")
myrecording = sd.rec(int(5*8000), 8000, 1, blocking=True)
print("*end")
print("*playing")
sd.play(myrecording, 8000, blocking=True)
sd.stop()
print("*end")
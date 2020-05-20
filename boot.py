from threading import Thread
from queue import Queue  # Python 3 import
import Filter
import speech_recognition as sr
import ThreadMain
import Plugins


#PL = Utils.PluginLoader()

r = sr.Recognizer()
audio_queue = Queue()

# start a new thread to recognize audio, while this thread focuses on listening
recognize_thread = Thread(target=ThreadMain.recognize_worker, args=(audio_queue, sr, r, Filter))
recognize_thread.daemon = True
recognize_thread.start()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    try:
        while True:  # repeatedly listen for phrases and put the resulting audio on the audio processing job queue
            audio_queue.put(r.listen(source))
            print("put audio on queue")
    except KeyboardInterrupt:  # allow Ctrl + C to shut down the program
        pass

audio_queue.join()  # block until all current audio processing jobs are done
audio_queue.put(None)  # tell the recognize_thread to stop
recognize_thread.join()  # wait for the recognize_thread to actually stop
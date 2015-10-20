#!/usr/bin/python3

import threading
import time

import gi
from gi.repository import GObject, Gst

default_song = '01.Uptown Funk.mp3'
error_song = 'Error music.mp3'
song_5678 = '5678.mp3'

class MusicPlayer():
    def __init__(self):
        GObject.threads_init()
        Gst.init(None)
        self.pipeline = None
        self._create_pipeline(default_song)
        loop = GObject.MainLoop()
        threading.Thread(target=loop.run, daemon=True).start()

    def _create_pipeline(self, filename):
        if self.pipeline is not None:
            self.pause_music()
            self.pipeline = None

        pipeline = Gst.Pipeline('pipeline')
        source = Gst.ElementFactory.make('filesrc', 'audio_source')
        decode = Gst.ElementFactory.make('mad', 'decode')
        sink = Gst.ElementFactory.make('alsasink', 'audio_sink')

        if not all([pipeline, source, decode, sink]):
            print('Failed creating pipeline elements')
            return

        source.set_property('location', filename)
        pipeline.add(source)
        pipeline.add(decode)
        pipeline.add(sink)

        source.link(decode)
        decode.link(sink)

        self.pipeline = pipeline
    
    def change_music(self, filename):
        self._create_pipeline(filename)
    
    def default_music(self):
        self.change_music(default_song)
        self.play_music()
        
    def error_music(self):
        self.change_music(error_song)
        self.play_music()

    def play_5678_music(self):
        self.change_music(song_5678)
        self.play_music()

    def play_music(self):
        self.pipeline.set_state(Gst.State.PLAYING)
    
    def pause_music(self):
        self.pipeline.set_state(Gst.State.PAUSED)

#music = MusicPlayer()
#music.play_music()
#time.sleep(2)
#music.pause_music()
#time.sleep(2)
#music.error_music()
#music.play_music()
#time.sleep(3)
#music.pause_music()

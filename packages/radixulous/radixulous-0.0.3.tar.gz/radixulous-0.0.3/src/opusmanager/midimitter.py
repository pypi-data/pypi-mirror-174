'''Play a .mid through a connected midi device'''
import sys
import time
import threading
from apres import MIDI, SetTempo, NoteOff, NoteOn, AllNotesOff


class PassiveController(object):
    def __init__(self, ticks, initial_ppqn):
        self.initial_ppqn = initial_ppqn
        self.ticks = ticks
        self.fake_pipe = []
        self.playing = False
        self._active_notes = {}

    def start(self):
        self.playing = True
        thread = threading.Thread(target=self.__play)
        thread.daemon = True
        thread.start()

    def read(self):
        while not self.fake_pipe:
            pass
        return self.fake_pipe.pop(0)

    def close(self):
        self.fake_pipe = []
        self.playing = False

    def __play(self):
        ptick = 0
        time.sleep(.4)
        start = time.time()
        seconds_per_tick = 60 / (self.initial_ppqn * 120)
        delay_accum = 0

        grouped_events = []
        last_tick = None
        for tick, event in self.ticks:
            if last_tick != tick:
                grouped_events.append((tick, []))
            grouped_events[-1][1].append(event)
            tick = last_tick

        self._active_notes = {}
        for tick, eventlist in grouped_events:
            delay = (tick - ptick) * seconds_per_tick # ideal delay
            drift = delay_accum - (time.time() - start) # how much the timing has drifted
            delay_accum += delay

            time.sleep(max(0, delay + drift))
            ptick = tick


            for event in eventlist:
                if isinstance(event, SetTempo):
                    bpm = event.get_bpm()
                    seconds_per_tick =  60 / (self.initial_ppqn * bpm)
                elif isinstance(event,NoteOn):
                    if event.velocity > 0:
                        self._active_notes[(event.note, event.channel)] = True
                    else:
                        self._active_notes[(event.note, event.channel)] = False
                elif isinstance(event,NoteOff):
                    self._active_notes[(event.note, event.channel)] = False

                self.fake_pipe.append(bytes(event))

        self.playing = False

class MidEmitter(object):
    def __init__(self, pinout=None):

        self.high_threshold = 81 # The note at which multiple fdds are required to be able to hear it
        self.playing = False


    def play(self, controller, instrument_count=128):
        controller.start()
        self.playing = True
        instrument_count = 1
        while controller.playing:
            chunk = controller.read()
            with open("/dev/midi1", 'wb') as pipe:
                pipe.write(chunk)

    def passive_play(self, midilike):
        ticks = []
        eventlist = midilike.get_all_events()

        passive_controller = PassiveController(eventlist, midilike.ppqn)
        try:
            self.play(passive_controller, 4)
        except KeyboardInterrupt:
            for i in range(16):
                with open("/dev/midi1", "wb") as pipe:
                    pipe.write(bytes(AllNotesOff(channel=i)))


if __name__ == "__main__":
    fddc = MidEmitter()
    if len(sys.argv) > 1:
        midi = MIDI.load(sys.argv[1])
        fddc.passive_play(midi)


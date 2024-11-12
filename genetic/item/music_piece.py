import numpy as np
import mido
from mido import MidiFile, MidiTrack, Message
import json

class MusicPiece:
    def __init__(self, length: int, pace: float, base_pitch: int =60):
        self.length = length
        self.pace = pace
        self.base_pitch = base_pitch
        self.notes = np.zeros((length, 2), dtype=int) # 2 columns: pitch and duration
    
    def get_length(self):
        return self.length
    
    def get_pace(self):
        return self.pace
    
    def get_base_pitch(self):
        return self.base_pitch
    
    def get_notes(self):
        return self.notes

    # append another music piece to the end of the current music piece
    def append(self, music_piece: 'MusicPiece'):
        self.notes = np.append(self.notes, music_piece.get_notes(), axis=0)
        self.length += music_piece.length

    # add a note to the music piece
    def add_note(self, pitch: int, duration: int = 1):
        self.notes = np.append(self.notes, [[pitch, duration]], axis=0)
        self.length += 1

    #change average to base_pitch
    def normalize(self):
        tmp = int(np.mean(self.notes[:, 0]))
        self.notes[:, 0] -= tmp

    # retrograde the music piece(playing the music piece in reverse order)
    def retrograde(self)-> 'MusicPiece':
        music_piece = MusicPiece(self.length, self.pace, self.base_pitch)
        music_piece.notes = np.flip(self.notes, axis=0)
        return music_piece

    # invert the music piece(playing the music piece upside down, i.e., the pitch of the notes are mirrored around the base pitch)
    def invert(self)-> 'MusicPiece':
        music_piece = MusicPiece(self.length, self.pace, self.base_pitch)
        music_piece.notes = self.notes.copy()
        music_piece.notes[:, 0] = music_piece.notes[:, 0]
        return music_piece

    # transpose the music piece by a given interval, i.e., shift the pitch of the notes by the given interval
    def transpose(self, interval: int)-> 'MusicPiece':
        music_piece = MusicPiece(self.length, self.pace, self.base_pitch)
        music_piece.notes = self.notes.copy()
        music_piece.notes[:, 0] += interval
        return music_piece

    #retrograde and invert the music piece at the same time
    def retrograde_invert(self)-> 'MusicPiece':
        music_piece = MusicPiece(self.length, self.pace, self.base_pitch)
        music_piece.notes = np.flip(self.notes, axis=0)
        music_piece.notes[:, 0] = - music_piece.notes[:, 0]
        return music_piece

    # get a part of the music piece, starting from the start-th note and ending at the end-th note
    def get_part(self, start: int, end: int)-> 'MusicPiece':
        music_piece = MusicPiece(end - start, self.pace, self.base_pitch)
        music_piece.notes = self.notes[start:end]
        return music_piece

    def __str__(self):
        ret = ""
        for pitch, duration in self.notes:
            ret += f"({pitch}, {duration}) "
        return ret
    # output the music piece to a MIDI file with the given filename and instrument
    def output_midi(self, filename: str, instrument: str, instrument_json_path: str):
        mid = mido.MidiFile()
        track = mido.MidiTrack()
        mid.tracks.append(track)

        with open(instrument_json_path, 'r') as f:
            instrument_mapping = json.load(f)
            instrument_number = instrument_mapping.get(instrument.lower(), 0)

        track.append(mido.Message('program_change', program=instrument_number))

        time = 0
        for pitch, duration in self.notes:
            note_use = np.clip(pitch + self.base_pitch, 0, 127) 
            track.append(mido.Message('note_on', note = note_use, velocity=64, time=1))
            track.append(mido.Message('note_off', note = note_use, velocity=64, time=int(duration * self.pace * 480)))  # 480 ticks per beat

        mid.save(filename)
        


    
        
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psychtoolbox as ptb
from psychopy import locale_setup
from psychopy import prefs

import os
import sys
import time

flagUseSound = True;
flagUsePTBSound = False;

useReloadSystem = False;

if flagUsePTBSound:
    prefs.hardware['audioLib'] = 'ptb'
    useReloadSystem = False;
    pass;
else:
    flagSounddevice = False;
    
    if flagSounddevice:
        prefs.hardware['audioLib'] = 'sounddevice'
        useReloadSystem = True;
    else:
        prefs.hardware['audioLib'] = 'pyo'
        useReloadSystem = False;
    pass;



prefs.hardware['audioDriver'] = 'Primary Sound' # ['Primary Sound', 'ASIO', 'Audigy'])

if flagUsePTBSound:
    #prefs.hardware['audioLatencyMode'] = '4'
    #prefs.hardware['audioLatencyMode'] = '3'  # soundblaster BAD
    #prefs.hardware['audioLatencyMode'] = '2'
    #prefs.hardware['audioLatencyMode'] = '1'
    #prefs.hardware['audioLatencyMode'] = '0'
    prefs.hardware['audioLatencyMode'] = '4'
else:
    prefs.hardware['audioLatencyMode'] = '0'
    
from psychopy import sound

#hardsnddelay = 0.140; #asus60 inner sound
#hardsnddelay = 0.100; #asus60 HDMI out
#hardsnddelay = 0.250; # soundblaster and audioLatencyMode is 0
#hardsnddelay = 0.250; # soundblasterXG6 and audioLatencyMode is 0
hardsnddelay = 0.230; # soundblasterXG6 and audioLatencyMode is 0
hardsnddelay = 0.300; # soundblasterXG6 and audioLatencyMode is 0
hardsnddelay = 0.400; # soundblasterXG6 and audioLatencyMode is 0
hardsnddelay = 0.100; # soundblasterXG6 and audioLatencyMode is 4
hardsnddelay = 0.400; # soundblasterXG6 and audioLatencyMode is 0
hardsnddelay = 0.100; # soundblasterXG6 and audioLatencyMode is 4
hardsnddelay = 0.200; # soundblasterXG6 and audioLatencyMode is 4
hardsnddelay = 0.250; # soundblasterXG6 and audioLatencyMode is 4
hardsnddelay = 0.400; # soundblasterXG6 and audioLatencyMode is 4
hardsnddelay = 0.250; # soundblasterXG6 and audioLatencyMode is 4
hardsnddelay = 0.100; # soundblasterXG6 and audioLatencyMode is 4
hardsnddelay = 0.300; # soundblasterXG6 and audioLatencyMode is 4
hardsnddelay = 0.200; # soundblasterXG6 and audioLatencyMode is 4

if flagUsePTBSound:
    sound_pre_sampleRate=44100
    sound_sampleRate=44100
else:  
    sound_pre_sampleRate=48000
    sound_sampleRate=48000

if flagUseSound:
    if flagUsePTBSound:
        #sb_init = sound.backend_ptb.SoundPTB(sampleRate=sound_pre_sampleRate,preBuffer=128,stereo=True);
        #sb_init2 = sound.backend_ptb.SoundPTB(sampleRate=sound_sampleRate,preBuffer=128,stereo=True);
        #sb_init = sound.backend_ptb.SoundPTB(sampleRate=sound_pre_sampleRate,stereo=True);
        sb_init = sound.backend_ptb.SoundPTB(sampleRate=sound_pre_sampleRate,preBuffer=32, stereo=True);
        #sb_init2 = sound.backend_ptb.SoundPTB(sampleRate=sound_sampleRate,stereo=True);
        pass;
    pass;
else:
    pass;

class BTTsSoundInfo:
    def __init__(self):
        global hardsnddelay;
        global sound_sampleRate;
        self.hardsnddelay = hardsnddelay;
        self.sound_sampleRate = sound_sampleRate;
        self.useReload = useReloadSystem;
        pass;

print('Using %s (with %s) for sounds' % (sound.audioLib, sound.audioDriver))

def testSound1():
    print("testSound1");
    sound_init_file = 'A'
    sound_init_lenth_sec = 0.2

    sound_init = sound.Sound(sound_init_file,secs=sound_init_lenth_sec, sampleRate=sound_sampleRate, stereo=True, hamming=False,name='sound_init')
    sound_init.setSound(sound_init_file, secs=sound_init_lenth_sec,  hamming=False );
    sound_init.setVolume(1)

    #nextFlip = 0;
    #sound_init.play(when=(nextFlip+hardsnddelay));
    
    #mySound.play(when=now+0.5) 
    now = ptb.GetSecs()
    sound_init.setSound(sound_init_file, secs=sound_init_lenth_sec,  hamming=False );
    sound_init.play(when=now+0.3);
    time.sleep(3.0);
    now = ptb.GetSecs()
    sound_init.setSound(sound_init_file, secs=sound_init_lenth_sec,  hamming=False );
    sound_init.play(when=now+0.3);
    time.sleep(3.0);

    for n in range(10):
        print("count "+str(n));
        now = ptb.GetSecs()
        sound_init.setSound(sound_init_file, secs=sound_init_lenth_sec,  hamming=False );
        sound_init.play(when=now+0.3);
        time.sleep(1.0);

    time.sleep(3.0);


def testMain():
    testSound1();
    pass;

if __name__ == "__main__":
    testMain();



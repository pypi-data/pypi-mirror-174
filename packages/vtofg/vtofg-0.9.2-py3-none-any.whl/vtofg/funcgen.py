'''
###########################
VTOFG: Vibration Test Object Function Generator
###########################
vtofg.funcgen
Author: Zack Ravetz

This file contains VTOFG's main "FunctionGenerator" class. This defines the main
function generator window and tk.TK instance
'''

import numpy as np
import tkinter as tk
import pyaudio
import threading

if __name__!='__main__':
    from vtofg.plotter import Plotter
    from vtofg.waves import *
    from vtofg._tools import *

else:
    from plotter import Plotter
    from waves import *
    from _tools import *


class FunctionGenerator(tk.Tk):
    '''
    The class for the function generator

    Attributes
    ----------
    plot:bool
        Boolean wether the plotter is ran or not
    player: PyAudio
        The PyAudio object to play the signal
    stream: PyAudio stream
        The stream attached to player that the signal is written to
    playing: bool
        Keeps track of if the signal is playing
    vcmd_perc: function
        registration for the validator command for percentages
    vcmd_int: function
        registration for the validator command for integers
    vcmd_float: function
        registration for the validator command for floats
    vcmd_byte: function
        registration for the validator command for bytes
    amp_var: tkinter DoubleVar
        The tkinter variable containing the master amplitude
    gen_freq_var: tkinter IntVar
        The tkinter variable containing the generator frequency
    gen_res_var: tkinter IntVar
        The tkinter variable containing the byte resolution
    time_var: tkinter DoubleVar
        The tkinter variable containing the buffer time
    wave_frame: tkinter Frame
        The tkinter Frame that the WaveUIs are placed into
    w_count: int
        The number of waves
    waveUIs: list[WaveUI]
        A list of the WaveUI objects
    wave_nums: list[tkinter Label]
        A list of the wave number labels
    wave_butt: list[tkinter Button]
        A list of the delete buttons for the waves
    run_button: tkinter Button
        The button to run/stop the signal
    plotter: Plotter
        The spectrum plotter for this function generator
    waves: list[SweepWave]
        A list of SweepWave objects to calculate the signal from
    stream_thread: Thread
        Thread to play the signal

    Methods
    -------
    delete_wave(i)
        Deletes the i-th wave
    add_wave
        Adds a new wave
    play_stop
        Toggles between playing the signal and stopping it
    load_signal
        Calculates the next signal buffer and plays it
    close
        Collects all threads and closes the function generator
    '''
    def __init__(self, plot = True):
        '''
        constructs the FunctionGenerator

        Parameters
        ----------
        plot: bool
            Boolean wether to plot the output or not
        '''
        super().__init__()
        self.grid_columnconfigure(0, weight=1)

        self.title("Function Generator")
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.plot = plot

        self.player = pyaudio.PyAudio()
        self.stream = self.player.open(format=self.player.get_format_from_width(2),
                channels=1,
                rate=44100,
                output=True)
        self.stream.stop_stream()
        self.playing = False

        self.vcmd_perc = (self.register(check_perc))
        self.vcmd_int = (self.register(check_int))
        self.vcmd_float = (self.register(check_float))
        self.vcmd_byte = (self.register(check_byte))

        self.amp_var = tk.DoubleVar(self)
        self.amp_var.set(100)
        amp_lab = tk.Label(self, text="Master Amplitude (%):")
        amp_input = tk.Entry(self,
            textvariable=self.amp_var,
            validate='all',
            validatecommand=(self.vcmd_perc, '%P'))
        amp_lab.grid(column=0, row=0, sticky='nsew')
        amp_input.grid(column=1, row=0, sticky='nsew')

        self.gen_freq_var = tk.IntVar(self)
        self.gen_freq_var.set(44100)
        gen_freq_lab = tk.Label(self, text="Generator Frequency (Hz):")
        gen_freq_input = tk.Entry(self,
            textvariable=self.gen_freq_var,
            validate='all',
            validatecommand=(self.vcmd_int, '%P'))
        gen_freq_lab.grid(column=2, row=0, sticky='nsew')
        gen_freq_input.grid(column=3, row=0, sticky='nsew')

        self.gen_res_var = tk.IntVar(self)
        self.gen_res_var.set(2)
        gen_res_lab = tk.Label(self, text="Resolution (Bytes):")
        gen_res_input = tk.Entry(self,
            textvariable=self.gen_res_var,
            validate='all',
            validatecommand=(self.vcmd_byte, '%P'))
        gen_res_lab.grid(column=4, row=0, sticky='nsew')
        gen_res_input.grid(column=5, row=0, sticky='nsew')

        self.time_var = tk.DoubleVar(self)
        self.time_var.set(0.1)
        time_lab = tk.Label(self, text="Buffer Time (s):")
        time_input = tk.Entry(self,
            textvariable=self.time_var,
            validate='all',
            validatecommand=(self.vcmd_float, '%P'))
        time_lab.grid(column=6, row=0, sticky='nsew')
        time_input.grid(column=7, row=0, sticky='nsew')

        self.wave_frame = tk.Frame(self)
        self.wave_frame.columnconfigure(0, weight = 1)
        self.wave_frame.columnconfigure(1, weight = 1)
        self.wave_frame.columnconfigure(2, weight = 1)
        self.wave_frame.columnconfigure(3, weight = 1)
        self.wave_frame.columnconfigure(4, weight = 1)
        self.wave_frame.grid(column=0, row=1, columnspan=8, sticky='nsew')

        w_num = tk.Label(self.wave_frame, text="Wave")
        w_amp_lab=tk.Label(self.wave_frame, text="Amplitude (%)")
        w_start_lab=tk.Label(self.wave_frame, text="Start Frequency (Hz)")
        w_end_lab=tk.Label(self.wave_frame, text="End Frequency (Hz)")
        w_time_lab=tk.Label(self.wave_frame, text="Sweep Time (s)")
        w_num.grid(column=0, row=0, sticky='nsew')
        w_amp_lab.grid(column=1, row=0, sticky='nsew')
        w_start_lab.grid(column=2, row=0, sticky='nsew')
        w_end_lab.grid(column=3, row=0, sticky='nsew')
        w_time_lab.grid(column=4, row=0, sticky='nsew')

        self.w_count = 1
        self.waveUIs = [WaveUI(self, self.wave_frame, 1)]
        self.wave_nums = [tk.Label(self.wave_frame, text="1")]
        self.wave_butt = [tk.Button(self.wave_frame,
            text="Delete",
            command=lambda i=self.w_count-1: self.delete_wave(i))]
        self.wave_nums[0].grid(column=0, row=1, sticky='nsew')
        self.wave_butt[0].grid(column=5, row=1, sticky='nsew')

        self.run_button = tk.Button(self, text="Run", command=self.play_stop)
        self.run_button.grid(column=0, row=2, sticky='nsew')

        add_button = tk.Button(self, text="Add Wave", command=self.add_wave)
        add_button.grid(column=1, row=2, sticky='nsew')

        if self.plot:
            self.plotter = Plotter(self)
            self.plotter.grid(column=0, row=3, columnspan=8, sticky='nsew')

    def delete_wave(self, i):
        '''
        Deletes the i-th wave
        
        Parameters
        ----------
        i: int
            The number of the wave to delete
        '''
        #removes all wave related tkinter widgets
        for j in range(len(self.waveUIs)):
            self.wave_butt[j].grid_forget()
            self.wave_nums[j].grid_forget()
            self.waveUIs[j].remove_widgets()

        #deletes i-th wave
        self.waveUIs.pop(i)

        #generates new tkinter widgets/locations
        self.wave_nums = []
        self.wave_butt = []
        jmax = len(self.waveUIs)
        for j in range(jmax):
            self.waveUIs[j].update_index(j+1)
            self.wave_nums.append(tk.Label(self.wave_frame, text=str(j+1)))
            self.wave_butt.append(tk.Button(self.wave_frame,
                text="Delete",
                command=lambda i=j: self.delete_wave(i)))
            self.wave_nums[-1].grid(column=0, row=j+1, sticky='nsew')
            self.wave_butt[-1].grid(column=5, row=j+1, sticky='nsew')
        
        #updates number of waves
        self.w_count = jmax

    def add_wave(self):
        '''
        Adds a new wave
        '''
        #updates number of waves
        self.w_count+=1

        #creates new WaveUI and relevant tkinter widgets
        self.waveUIs.append(WaveUI(self, self.wave_frame, self.w_count))
        self.wave_nums.append(tk.Label(self.wave_frame, text=str(self.w_count)))
        self.wave_butt.append(tk.Button(self.wave_frame,
            text="Delete",
            command=lambda i=self.w_count-1: self.delete_wave(i)))
        self.wave_nums[-1].grid(column=0, row=self.w_count, sticky='nsew')
        self.wave_butt[-1].grid(column=5, row=self.w_count, sticky='nsew')

    def play_stop(self):
        '''
        Toggles between playing the signal and stopping it
        '''
        #gets values from user entries
        self.resolution = self.gen_res_var.get()
        self.fgen_freq = self.gen_freq_var.get()
        self.fgen_period = 1/self.fgen_freq

        #gets list of SweepWave objects from the WaveUI inputs
        self.waves = [self.waveUIs[i].get_wave() for i in range(len(self.waveUIs))]

        #starts/stops plotter
        if self.plot:
            self.plotter.toggle_pause(self.waves)

        #checks if signal is running
        if self.stream.is_stopped():
            if len(self.waveUIs)>0:
                self.run_button['text'] = "Stop"
                self.playing = True
                #starts playing signal
                self.stream_thread = threading.Thread(target = self.load_signal)
                self.stream_thread.start()

        elif self.stream.is_active():
            #stops playing signal
            self.playing = False
            self.stream_thread.join()
            self.run_button['text'] = "Run"


    def load_signal(self):
        '''
        Calculates the next signal buffer and plays it
        '''
        #gets values from user input and calculates first buffer signal
        self.buffer_time = self.time_var.get()
        self.master_amp = self.amp_var.get()/100

        times = np.arange(0, self.buffer_time, self.fgen_period)
        sigs = np.zeros(times.shape)
        amps = 0
        for wave in self.waves:
            sig, amp = wave.get_signal(times)
            sigs = sigs+sig
            amps = amps+amp
        if amps != 0:
            sigs = sigs/amps
        sigs = (2**(8*self.resolution-1)-1)*sigs*self.master_amp
        sigs = sigs.astype('i{}'.format(self.resolution))

        #creates PyAudio stream
        self.stream = self.player.open(format=self.player.get_format_from_width(self.resolution),
                channels=1,
                rate=self.fgen_freq,
                output=True)

        while self.playing:
            #plays buffer signal
            write_thread = threading.Thread(target = lambda sigs = sigs: self.stream.write(sigs, num_frames=sigs.shape[0]))
            write_thread.start()
            #calculates next buffer signal
            times = times+self.buffer_time
            sigs = np.zeros(times.shape)
            amps = 0
            for wave in self.waves:
                sig, amp = wave.get_signal(times)
                sigs = sigs+sig
                amps = amps+amp
            if amps != 0:
                sigs = sigs/amps
            sigs = (2**(8*self.resolution-1)-1)*sigs*self.master_amp
            sigs = sigs.astype('i{}'.format(self.resolution))
            #waits for previous signal to finish playing before starting next one
            write_thread.join()
        #stops stream
        self.stream.stop_stream()

    def close(self):
        '''
        Collects all threads and closes the function generator
        '''
        self.playing = False
        try:
            self.stream_thread.join()
        except AttributeError:
            pass
        if self.plot:
            try:
                self.plotter.next_thread.join()
            except AttributeError:
                pass
        self.stream.close()
        self.player.terminate()
        self.destroy()

if __name__ == "__main__":
    root = FunctionGenerator()
    root.mainloop()
'''
###########################
VTOFG: Vibration Test Object Function Generator
###########################
vtofg.plotter
Author: Zack Ravetz

This file contains VTOFG's "SweepWave" and "WaveUI classes. These are used for the creation
of wave in the signal for the function generator.
'''

import numpy as np
import tkinter as tk

class SweepWave:
    '''
    Backend for a wave swept linearly through frequencies

    Attributes
    ----------
    start_freq: int
        starting frequency for the swept wave, in Hz
    end_freq: int
        end frequency for the swept wave, in Hz
    amplitude: float
        relative amplitude of the swept wave, value<1
    sweep_period: float
        period of the swept wave, in seconds

    Methods
    -------
    get_signal(times_raw) -> (Any, float)
        returns signal for given times and amplitude
    '''
    def __init__(self,  start_freq: int, end_freq: int, amplitude: float, sweep_period: float) -> None:
        '''
        Constructs the swept wave

        Parameters
        ----------
        start_freq: int
            starting frequency for the swept wave, in Hz
        end_freq: int
            end frequency for the swept wave, in Hz
        amplitude: float
            relative amplitude of the swept wave, value<1
        sweep_period: float
            period of the swept wave, in seconds
        '''
        self.start_freq = start_freq
        self.end_freq = end_freq
        self.amplitude = amplitude
        self.sweep_period = sweep_period

    def get_signal(self, times_raw):
        '''
        Returns the signal at the times provides

        Parameters
        ----------
        times_raw: array like
            an array of times to calculate the signal for, times in seconds after start

        Returns
        -------
        sig: array like
            signal of wave at the given times, arbitrary units
        self.amplitude: float
            relative amplitude of the swept wave, value<1
        '''
        if self.sweep_period == 0: #ensures no divide by zero in calculating frequencies
            return np.zeros(times_raw.shape), 0

        else:
            times = (times_raw%self.sweep_period) #modular of given times for given period
            k_diff = self.start_freq - (self.start_freq-self.end_freq)*times/(2*self.sweep_period) #unitary frequencies for given times
            wave_func = 2*np.pi*k_diff*times #phases for given times
            wave = np.sin(wave_func) 
            sig = wave*self.amplitude

            return sig, self.amplitude

class WaveUI:
    '''
    The user interface for the swept waves

    Attributes
    -----------
    main: FunctionGenerator
        The FunctionGenerator object that this wave is attached to
    frame: tkinter Frame
        the tkinter frame object that the tkinter widgets for this wave are placed in
    index: int
        the unique index 
    amp_var: tkinter DoubleVar
        the tkinter variable attached to the amplitude input
    amp_input: tkinter Entry
        the tkinter entry box for the amplitude 
    start_var: tkinter IntVar
        the tkinter variable attached to the start frequency input
    start_input: tkinter Entry
        the tkinter entry box for the start frequency 
    end_var: tkinter IntVar
        the tkinter variable attached to the end frequency input
    end_input: tkinter Entry
        the tkinter entry box for the end frequency 
    time_var: tkinter DoubleVar
        the tkinter variable attached to the sweep period input
    time_input: tkinter Entry
        the tkinter entry box for the sweep period 
    
    Methods
    -------
    get_wave -> SweepWave
        Creates the backend SweepWave object for the values entered into the UI
    remove_widgets
        Function to remove the tkinter widgets from view, used when deleting a wave
    update_index
        Updates the index and shows the tkinter widgets at the new index after a wave has been deleted
    '''

    def __init__(self, main, frame:tk.Frame, index: int):
        '''
        Constructs the user interface

        Parameters
        -----------
        main: FunctionGenerator
            The FunctionGenerator object that this wave is attached to
        frame: tkinter Frame
            The tkinter frame object that the tkinter widgets for this wave are placed in
        index: int
            The unique index of this wave
        '''
        self.main = main
        self.frame = frame
        self.index = index

        #creating the tkinter variables and widgets for this wave
        self.amp_var = tk.DoubleVar()
        self.amp_var.set(100)
        self.amp_input = tk.Entry(self.frame,
            textvariable=self.amp_var,
            validate='all',
            validatecommand=(self.main.vcmd_perc, '%P'))
        self.amp_input.grid(column=1, row=index, sticky='nsew')

        self.start_var = tk.IntVar()
        self.start_var.set(2000)
        self.start_input = tk.Entry(self.frame,
            textvariable=self.start_var,
            validate='all',
            validatecommand=(self.main.vcmd_int, '%P'))
        self.start_input.grid(column=2, row=index, sticky='nsew')

        self.end_var = tk.IntVar()
        self.end_var.set(2000)
        self.end_input = tk.Entry(self.frame,
            textvariable=self.end_var,
            validate='all',
            validatecommand=(self.main.vcmd_int, '%P'))
        self.end_input.grid(column=3, row=index, sticky='nsew')

        self.time_var = tk.DoubleVar()
        self.time_var.set(10)
        self.time_input = tk.Entry(self.frame,
            textvariable=self.time_var,
            validate='all',
            validatecommand=(self.main.vcmd_float, '%P'))
        self.time_input.grid(column=4, row=index, sticky='nsew')

    def get_wave(self)->SweepWave:
        '''
        Creates the backend SweepWave object for the values entered into the UI

        Returns
        -------
        sweepwave: SweepWave
            the SweepWave object for the entries into this UI
        '''
        start_freq = self.start_var.get()
        end_freq = self.end_var.get()
        amplitude = self.amp_var.get()/100
        sweep_period = self.time_var.get()
        sweepwave = SweepWave(start_freq, end_freq, amplitude, sweep_period)
        return sweepwave

    def remove_widgets(self)->None:
        '''
        Function to remove the tkinter widgets from view, used when deleting a wave
        '''
        self.amp_input.grid_forget()
        self.start_input.grid_forget()
        self.end_input.grid_forget()
        self.time_input.grid_forget()

    def update_index(self, index)->None:
        '''
        Updates the index and shows the tkinter widgets at the new index after a wave has been deleted

        Parameters
        ----------
        index: int
            New index for the wave
        '''
        self.index = index

        self.amp_input.grid(column=1, row=index, sticky='nsew')
        self.start_input.grid(column=2, row=index, sticky='nsew')
        self.end_input.grid(column=3, row=index, sticky='nsew')
        self.time_input.grid(column=4, row=index, sticky='nsew')
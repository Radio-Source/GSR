#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Gnuradio Spectro Radiometer
# Author: Pierre Terrier - Original code Marcus Leech (CCERA)
# Copyright: GNU-GPL
# Description: A simple spectro radiometer for radiastronmy
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
import gsr_baseline_compensate as baseline_compensate  # embedded python block
import gsr_ezRAvectorlogger as ezRAvectorlogger  # embedded python block
import gsr_flipper as flipper  # embedded python block
import gsr_formatter as formatter  # embedded python block
import gsr_stripchart_0 as stripchart_0  # embedded python block
import gsr_vectorlogger as vectorlogger  # embedded python block
import math
import osmosdr
import time
import ra_funcs
import sip
import threading



class gsr(gr.top_block, Qt.QWidget):

    def __init__(self, dmult=100, freq=1420.4058e6, logtime=5.0, longitude=2.552186, rfgain=49, sinteg=60.0, srate=2.5e6, tinteg=60, utc=1, vf=1):
        gr.top_block.__init__(self, "Gnuradio Spectro Radiometer", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Gnuradio Spectro Radiometer")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "gsr")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Parameters
        ##################################################
        self.dmult = dmult
        self.freq = freq
        self.logtime = logtime
        self.longitude = longitude
        self.rfgain = rfgain
        self.sinteg = sinteg
        self.srate = srate
        self.tinteg = tinteg
        self.utc = utc
        self.vf = vf

        ##################################################
        # Variables
        ##################################################
        self.alt = alt = 30.00
        self.latitude = latitude = 44.695978
        self.altitude = altitude = alt
        self.pacer = pacer = 0.0
        self.decln = decln = altitude-latitude
        self.tiktok = tiktok = pacer*0.0
        self.samp_rate = samp_rate = srate
        self.ifreq = ifreq = freq
        self.gmt = gmt = time.gmtime()
        self.fftsize = fftsize = 2048
        self.declnstr = declnstr =  str("%3.2f" % decln) if (decln<0) else "+"+str("%3.2f" % (decln))
        self.Longitude = Longitude = longitude
        self.winpower = winpower = sum([x*x for x in window.blackman_harris(fftsize)])
        self.velocity = velocity = vf
        self.variable_qtgui_label_rf = variable_qtgui_label_rf = ""
        self.variable_qtgui_label_Location = variable_qtgui_label_Location = ""
        self.variable_qtgui_label_3 = variable_qtgui_label_3 = ""
        self.variable_qtgui_label_1 = variable_qtgui_label_1 = '180 ( meridian transit )'
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = ""
        self.today = today = "%04d-%02d-%02d" % (gmt.tm_year, gmt.tm_mon, gmt.tm_mday)
        self.split_ratio = split_ratio = 100
        self.seconds = seconds = 3600
        self.prefix = prefix =  "%3.2f" % (decln)
        self.ltp = ltp = time.gmtime(time.time())
        self.itinteg = itinteg = tinteg
        self.isinteg = isinteg = sinteg
        self.irfgain = irfgain = rfgain
        self.idecln = idecln = declnstr
        self.freqstep = freqstep = (samp_rate/fftsize)/1.0e6
        self.freqlow = freqlow = (ifreq-(samp_rate/2.0))/1.0e6
        self.freqhigh = freqhigh = (ifreq+(samp_rate/2.0))/1.0e6
        self.filechoice = filechoice = 0
        self.fftrate = fftrate = int(samp_rate/fftsize)
        self.doplow = doplow = -((samp_rate/2.0)/ifreq)*299792.0
        self.dophigh = dophigh = ((samp_rate/2.0)/ifreq)*299792.0
        self.dc_gain = dc_gain = 100
        self.data_rate = data_rate = 10
        self.correct_baseline = correct_baseline = False
        self.azimut = azimut = 180
        self.amsl = amsl = 600
        self.actual_freq = actual_freq = ifreq
        self.LMST = LMST = ra_funcs.cur_sidereal(Longitude+tiktok).replace(",",":")

        ##################################################
        # Blocks
        ##################################################

        self.Main = Qt.QTabWidget()
        self.Main_widget_0 = Qt.QWidget()
        self.Main_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Main_widget_0)
        self.Main_grid_layout_0 = Qt.QGridLayout()
        self.Main_layout_0.addLayout(self.Main_grid_layout_0)
        self.Main.addTab(self.Main_widget_0, 'GSR')
        self.top_grid_layout.addWidget(self.Main, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._latitude_range = qtgui.Range(-90.00, 90.00, 0.1, 44.695978, 20)
        self._latitude_win = qtgui.RangeWidget(self._latitude_range, self.set_latitude, "Latitude : ", "counter", float, QtCore.Qt.Horizontal)
        self.Main_grid_layout_0.addWidget(self._latitude_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        self._ifreq_tool_bar = Qt.QToolBar(self)
        self._ifreq_tool_bar.addWidget(Qt.QLabel("Tuned Frequency" + ": "))
        self._ifreq_line_edit = Qt.QLineEdit(str(self.ifreq))
        self._ifreq_tool_bar.addWidget(self._ifreq_line_edit)
        self._ifreq_line_edit.editingFinished.connect(
            lambda: self.set_ifreq(eng_notation.str_to_num(str(self._ifreq_line_edit.text()))))
        self.Main_grid_layout_0.addWidget(self._ifreq_tool_bar, 1, 0, 1, 1)
        for r in range(1, 2):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        self._Longitude_range = qtgui.Range(-180, 180, 0.1, longitude, 20)
        self._Longitude_win = qtgui.RangeWidget(self._Longitude_range, self.set_Longitude, "Longitude : ", "counter", float, QtCore.Qt.Horizontal)
        self.Main_grid_layout_0.addWidget(self._Longitude_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        _velocity_check_box = Qt.QCheckBox("Velocity / Frequency")
        self._velocity_choices = {True: 1, False: 0}
        self._velocity_choices_inv = dict((v,k) for k,v in self._velocity_choices.items())
        self._velocity_callback = lambda i: Qt.QMetaObject.invokeMethod(_velocity_check_box, "setChecked", Qt.Q_ARG("bool", self._velocity_choices_inv[i]))
        self._velocity_callback(self.velocity)
        _velocity_check_box.stateChanged.connect(lambda i: self.set_velocity(self._velocity_choices[bool(i)]))
        self.Main_grid_layout_0.addWidget(_velocity_check_box, 3, 2, 1, 1)
        for r in range(3, 4):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        self._itinteg_range = qtgui.Range(1, 300, 1, tinteg, 100)
        self._itinteg_win = qtgui.RangeWidget(self._itinteg_range, self.set_itinteg, "TP Integration Time", "counter_slider", float, QtCore.Qt.Horizontal)
        self.Main_grid_layout_0.addWidget(self._itinteg_win, 5, 0, 1, 1)
        for r in range(5, 6):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        self._isinteg_range = qtgui.Range(1, 300, 1, sinteg, 100)
        self._isinteg_win = qtgui.RangeWidget(self._isinteg_range, self.set_isinteg, "Spectral Integration Time", "counter_slider", float, QtCore.Qt.Horizontal)
        self.Main_grid_layout_0.addWidget(self._isinteg_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        self.formatter = formatter.blk(formatter=None, filepat='tp-%04d%02d%02d'+'_'+prefix, extension='.csv', logtime=logtime, fmtstr='%11.9f', nchan=1, localtime=False if utc != 0 else True, longitude=Longitude, legend="GMT,LMST,TP,DEC=%f,LONGITUDE=%f,LATITUDE=%f,AMSL=%f,FREQ=%f,BW=%f" % (decln,longitude,latitude,amsl,ifreq/1.0e6, srate/1.0e6))
        # Create the options list
        self._filechoice_options = [0, 1, 2]
        # Create the labels list
        self._filechoice_labels = ['No file', 'CSV file', 'ezRA file']
        # Create the combo box
        # Create the radio buttons
        self._filechoice_group_box = Qt.QGroupBox("File type choice" + ": ")
        self._filechoice_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._filechoice_button_group = variable_chooser_button_group()
        self._filechoice_group_box.setLayout(self._filechoice_box)
        for i, _label in enumerate(self._filechoice_labels):
            radio_button = Qt.QRadioButton(_label)
            self._filechoice_box.addWidget(radio_button)
            self._filechoice_button_group.addButton(radio_button, i)
        self._filechoice_callback = lambda i: Qt.QMetaObject.invokeMethod(self._filechoice_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._filechoice_options.index(i)))
        self._filechoice_callback(self.filechoice)
        self._filechoice_button_group.buttonClicked[int].connect(
            lambda i: self.set_filechoice(self._filechoice_options[i]))
        self.Main_grid_layout_0.addWidget(self._filechoice_group_box, 3, 3, 1, 1)
        for r in range(3, 4):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        # Create the options list
        self._dc_gain_options = [100, 1000, 10000, 100000, 1000000]
        # Create the labels list
        self._dc_gain_labels = ['x100', 'x1000', 'x10000', 'x100000', 'x1000000']
        # Create the combo box
        # Create the radio buttons
        self._dc_gain_group_box = Qt.QGroupBox("Detector Output Mult." + ": ")
        self._dc_gain_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._dc_gain_button_group = variable_chooser_button_group()
        self._dc_gain_group_box.setLayout(self._dc_gain_box)
        for i, _label in enumerate(self._dc_gain_labels):
            radio_button = Qt.QRadioButton(_label)
            self._dc_gain_box.addWidget(radio_button)
            self._dc_gain_button_group.addButton(radio_button, i)
        self._dc_gain_callback = lambda i: Qt.QMetaObject.invokeMethod(self._dc_gain_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._dc_gain_options.index(i)))
        self._dc_gain_callback(self.dc_gain)
        self._dc_gain_button_group.buttonClicked[int].connect(
            lambda i: self.set_dc_gain(self._dc_gain_options[i]))
        self.Main_grid_layout_0.addWidget(self._dc_gain_group_box, 5, 3, 1, 1)
        for r in range(5, 6):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        _correct_baseline_check_box = Qt.QCheckBox("Baseline Correction")
        self._correct_baseline_choices = {True: True, False: False}
        self._correct_baseline_choices_inv = dict((v,k) for k,v in self._correct_baseline_choices.items())
        self._correct_baseline_callback = lambda i: Qt.QMetaObject.invokeMethod(_correct_baseline_check_box, "setChecked", Qt.Q_ARG("bool", self._correct_baseline_choices_inv[i]))
        self._correct_baseline_callback(self.correct_baseline)
        _correct_baseline_check_box.stateChanged.connect(lambda i: self.set_correct_baseline(self._correct_baseline_choices[bool(i)]))
        self.Main_grid_layout_0.addWidget(_correct_baseline_check_box, 3, 1, 1, 1)
        for r in range(3, 4):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        self.vectorlogger = vectorlogger.blk(fftsize=fftsize, formatter=None, filepat='fft-%04d%02d%02d'+'_'+prefix, extension='.csv', logtime=logtime*3, fmtstr='%6.2f', localtime=False if utc != 0 else True, fftshift=False, longitude=longitude)
        self._variable_qtgui_label_rf_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_rf_formatter = None
        else:
            self._variable_qtgui_label_rf_formatter = lambda x: str(x)

        self._variable_qtgui_label_rf_tool_bar.addWidget(Qt.QLabel("RF SDR Parameters"))
        self._variable_qtgui_label_rf_label = Qt.QLabel(str(self._variable_qtgui_label_rf_formatter(self.variable_qtgui_label_rf)))
        self._variable_qtgui_label_rf_tool_bar.addWidget(self._variable_qtgui_label_rf_label)
        self.Main_grid_layout_0.addWidget(self._variable_qtgui_label_rf_tool_bar, 0, 0, 1, 1)
        for r in range(0, 1):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        self._variable_qtgui_label_Location_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_Location_formatter = None
        else:
            self._variable_qtgui_label_Location_formatter = lambda x: str(x)

        self._variable_qtgui_label_Location_tool_bar.addWidget(Qt.QLabel("Location Parameters"))
        self._variable_qtgui_label_Location_label = Qt.QLabel(str(self._variable_qtgui_label_Location_formatter(self.variable_qtgui_label_Location)))
        self._variable_qtgui_label_Location_tool_bar.addWidget(self._variable_qtgui_label_Location_label)
        self.Main_grid_layout_0.addWidget(self._variable_qtgui_label_Location_tool_bar, 0, 1, 1, 1)
        for r in range(0, 1):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        self._variable_qtgui_label_3_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_3_formatter = None
        else:
            self._variable_qtgui_label_3_formatter = lambda x: str(x)

        self._variable_qtgui_label_3_tool_bar.addWidget(Qt.QLabel("Astronomy Parameters"))
        self._variable_qtgui_label_3_label = Qt.QLabel(str(self._variable_qtgui_label_3_formatter(self.variable_qtgui_label_3)))
        self._variable_qtgui_label_3_tool_bar.addWidget(self._variable_qtgui_label_3_label)
        self.Main_grid_layout_0.addWidget(self._variable_qtgui_label_3_tool_bar, 0, 3, 1, 1)
        for r in range(0, 1):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        self._variable_qtgui_label_1_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_1_formatter = None
        else:
            self._variable_qtgui_label_1_formatter = lambda x: str(x)

        self._variable_qtgui_label_1_tool_bar.addWidget(Qt.QLabel("Azimut : "))
        self._variable_qtgui_label_1_label = Qt.QLabel(str(self._variable_qtgui_label_1_formatter(self.variable_qtgui_label_1)))
        self._variable_qtgui_label_1_tool_bar.addWidget(self._variable_qtgui_label_1_label)
        self.Main_grid_layout_0.addWidget(self._variable_qtgui_label_1_tool_bar, 1, 2, 1, 1)
        for r in range(1, 2):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_0_formatter = None
        else:
            self._variable_qtgui_label_0_formatter = lambda x: str(x)

        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel("Antenna Parameters"))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.Main_grid_layout_0.addWidget(self._variable_qtgui_label_0_tool_bar, 0, 2, 1, 1)
        for r in range(0, 1):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        self.stripchart_0 = stripchart_0.blk(decim=data_rate, daily=86400)
        self.single_pole_iir_filter_xx_1 = filter.single_pole_iir_filter_ff((ra_funcs.getalpha(1.0/isinteg,fftrate)), fftsize)
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff((ra_funcs.getalpha(1.0/itinteg,samp_rate/split_ratio)), 1)
        self.qtgui_vector_sink_f_1 = qtgui.vector_sink_f(
            fftsize,
            doplow if (velocity == True) else freqlow,
            (((dophigh-doplow)/fftsize) if (velocity == 1) else freqstep),
            "Red shift(km/s)"  if (velocity == 1) else  "Frequency (MHz)",
            'Rel power (dB)',
            "Doppler Velocity" if (velocity == 1) else "Frequency",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_1.set_update_time((1.0/(data_rate)))
        self.qtgui_vector_sink_f_1.set_y_axis((-100), 10)
        self.qtgui_vector_sink_f_1.enable_autoscale(True)
        self.qtgui_vector_sink_f_1.enable_grid(True)
        self.qtgui_vector_sink_f_1.set_x_axis_units("km/s" if (velocity == 1) else "MHz")
        self.qtgui_vector_sink_f_1.set_y_axis_units('dB')
        self.qtgui_vector_sink_f_1.set_ref_level(0)


        labels = ["Spectrum", "Spectrum", '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_1.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_1.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_1.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_1.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_1_win = sip.wrapinstance(self.qtgui_vector_sink_f_1.qwidget(), Qt.QWidget)
        self.Main_grid_layout_0.addWidget(self._qtgui_vector_sink_f_1_win, 4, 0, 1, 4)
        for r in range(4, 5):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 4):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            86400,
            0,
            (-(1/3600)),
            "Drift Time  (Hours)",
            "Detector Power",
            "Total Power (Daily)",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time((1.0/(data_rate)))
        self.qtgui_vector_sink_f_0.set_y_axis((-140), 10)
        self.qtgui_vector_sink_f_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0.enable_grid(True)
        self.qtgui_vector_sink_f_0.set_x_axis_units('')
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)


        labels = ['Sky', '', '', 'Detector(West)', '',
            '', '', '', '', '']
        widths = [2, 1, 1, 2, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "magenta", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1, 1, 1, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.Main_grid_layout_0.addWidget(self._qtgui_vector_sink_f_0_win, 6, 0, 1, 4)
        for r in range(6, 7):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 4):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        self.pacer_probe = blocks.probe_signal_f()
        def _pacer_probe():
          while True:

            val = self.pacer_probe.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_pacer,val))
              except AttributeError:
                self.set_pacer(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (1))
        _pacer_thread = threading.Thread(target=_pacer_probe)
        _pacer_thread.daemon = True
        _pacer_thread.start()
        self.osmosdr_source_1 = osmosdr.source(
            args="numchan=" + str(1) + " " + "airspy=0,bias=1,pack=0"
        )
        self.osmosdr_source_1.set_sample_rate(samp_rate)
        self.osmosdr_source_1.set_center_freq(actual_freq, 0)
        self.osmosdr_source_1.set_freq_corr(0, 0)
        self.osmosdr_source_1.set_dc_offset_mode(0, 0)
        self.osmosdr_source_1.set_iq_balance_mode(0, 0)
        self.osmosdr_source_1.set_gain_mode(False, 0)
        self.osmosdr_source_1.set_gain(40, 0)
        self.osmosdr_source_1.set_if_gain(20, 0)
        self.osmosdr_source_1.set_bb_gain(20, 0)
        self.osmosdr_source_1.set_antenna('', 0)
        self.osmosdr_source_1.set_bandwidth(0, 0)
        self._irfgain_range = qtgui.Range(0, 100, 2.5, rfgain, 100)
        self._irfgain_win = qtgui.RangeWidget(self._irfgain_range, self.set_irfgain, "RF Gain", "counter", float, QtCore.Qt.Horizontal)
        self.Main_grid_layout_0.addWidget(self._irfgain_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        self._idecln_tool_bar = Qt.QToolBar(self)

        if None:
            self._idecln_formatter = None
        else:
            self._idecln_formatter = lambda x: str(x)

        self._idecln_tool_bar.addWidget(Qt.QLabel("Declination target :  "))
        self._idecln_label = Qt.QLabel(str(self._idecln_formatter(self.idecln)))
        self._idecln_tool_bar.addWidget(self._idecln_label)
        self.Main_grid_layout_0.addWidget(self._idecln_tool_bar, 2, 3, 1, 1)
        for r in range(2, 3):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        self.flipper = flipper.blk(fftsize=fftsize, enabled=False)
        self.fft_vxx_0 = fft.fft_vcc(fftsize, True, window.blackmanharris(fftsize), True, 1)
        self.ezRAvectorlogger = ezRAvectorlogger.blk(fftsize=fftsize, formatter=None, filepat='ezRA%04d%02d%02d'+'_'+prefix, extension='.txt', logtime=logtime*3, fmtstr='%6.2f', localtime=False if utc != 0 else True, fftshift=False, longitude=longitude, legend="lat %g  long %g  amsl %g  name %s\nfreqMin %g  freqMax %g  freqBinQty %g" % (latitude,Longitude,amsl,prefix,freqlow,freqhigh,fftsize))
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fftsize)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_float*fftsize,0,filechoice)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*fftsize)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, fftsize, (-20*math.log10(fftsize)-10*math.log10(winpower/fftsize)))
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_ff((1.0/split_ratio)*dc_gain, 1)
        self.blocks_keep_one_in_n_1 = blocks.keep_one_in_n(gr.sizeof_float*fftsize, (int(fftrate/data_rate)))
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_float*1, (int(int(samp_rate/data_rate)/split_ratio)))
        self.blocks_integrate_xx_0 = blocks.integrate_ff(split_ratio, 1)
        self.blocks_complex_to_mag_squared_1 = blocks.complex_to_mag_squared(fftsize)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.baseline_compensate = baseline_compensate.blk(fftsize=fftsize, collect=True if correct_baseline == False else False)
        self._altitude_range = qtgui.Range(-180.00, 180.00, 0.1, alt, 20)
        self._altitude_win = qtgui.RangeWidget(self._altitude_range, self.set_altitude, "Altitude :  ", "counter", float, QtCore.Qt.Horizontal)
        self.Main_grid_layout_0.addWidget(self._altitude_win, 2, 2, 1, 1)
        for r in range(2, 3):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        self._LMST_tool_bar = Qt.QToolBar(self)

        if None:
            self._LMST_formatter = None
        else:
            self._LMST_formatter = lambda x: str(x)

        self._LMST_tool_bar.addWidget(Qt.QLabel("LMST :  "))
        self._LMST_label = Qt.QLabel(str(self._LMST_formatter(self.LMST)))
        self._LMST_tool_bar.addWidget(self._LMST_label)
        self.Main_grid_layout_0.addWidget(self._LMST_tool_bar, 1, 3, 1, 1)
        for r in range(1, 2):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.Main_grid_layout_0.setColumnStretch(c, 1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.baseline_compensate, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_1, 0), (self.single_pole_iir_filter_xx_1, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.formatter, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.stripchart_0, 0))
        self.connect((self.blocks_keep_one_in_n_1, 0), (self.baseline_compensate, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.single_pole_iir_filter_xx_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.flipper, 0))
        self.connect((self.blocks_selector_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_selector_0, 2), (self.ezRAvectorlogger, 0))
        self.connect((self.blocks_selector_0, 1), (self.vectorlogger, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_1, 0))
        self.connect((self.flipper, 0), (self.qtgui_vector_sink_f_1, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.pacer_probe, 0))
        self.connect((self.single_pole_iir_filter_xx_1, 0), (self.blocks_keep_one_in_n_1, 0))
        self.connect((self.stripchart_0, 0), (self.qtgui_vector_sink_f_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "gsr")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_dmult(self):
        return self.dmult

    def set_dmult(self, dmult):
        self.dmult = dmult

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_ifreq(self.freq)

    def get_logtime(self):
        return self.logtime

    def set_logtime(self, logtime):
        self.logtime = logtime
        self.ezRAvectorlogger.logtime = self.logtime*3
        self.formatter.logtime = self.logtime
        self.vectorlogger.logtime = self.logtime*3

    def get_longitude(self):
        return self.longitude

    def set_longitude(self, longitude):
        self.longitude = longitude
        self.set_Longitude(self.longitude)
        self.ezRAvectorlogger.longitude = self.longitude
        self.formatter.legend = "GMT,LMST,TP,DEC=%f,LONGITUDE=%f,LATITUDE=%f,AMSL=%f,FREQ=%f,BW=%f" % (self.decln,self.longitude,self.latitude,self.amsl,self.ifreq/1.0e6, self.srate/1.0e6)
        self.vectorlogger.longitude = self.longitude

    def get_rfgain(self):
        return self.rfgain

    def set_rfgain(self, rfgain):
        self.rfgain = rfgain
        self.set_irfgain(self.rfgain)

    def get_sinteg(self):
        return self.sinteg

    def set_sinteg(self, sinteg):
        self.sinteg = sinteg
        self.set_isinteg(self.sinteg)

    def get_srate(self):
        return self.srate

    def set_srate(self, srate):
        self.srate = srate
        self.set_samp_rate(self.srate)
        self.formatter.legend = "GMT,LMST,TP,DEC=%f,LONGITUDE=%f,LATITUDE=%f,AMSL=%f,FREQ=%f,BW=%f" % (self.decln,self.longitude,self.latitude,self.amsl,self.ifreq/1.0e6, self.srate/1.0e6)

    def get_tinteg(self):
        return self.tinteg

    def set_tinteg(self, tinteg):
        self.tinteg = tinteg
        self.set_itinteg(self.tinteg)

    def get_utc(self):
        return self.utc

    def set_utc(self, utc):
        self.utc = utc
        self.ezRAvectorlogger.localtime = False if self.utc != 0 else True
        self.formatter.localtime = False if self.utc != 0 else True
        self.vectorlogger.localtime = False if self.utc != 0 else True

    def get_vf(self):
        return self.vf

    def set_vf(self, vf):
        self.vf = vf
        self.set_velocity(self.vf)

    def get_alt(self):
        return self.alt

    def set_alt(self, alt):
        self.alt = alt
        self.set_altitude(self.alt)

    def get_latitude(self):
        return self.latitude

    def set_latitude(self, latitude):
        self.latitude = latitude
        self.set_decln(self.altitude-self.latitude)
        self.ezRAvectorlogger.legend = "lat %g  long %g  amsl %g  name %s\nfreqMin %g  freqMax %g  freqBinQty %g" % (self.latitude,self.Longitude,self.amsl,self.prefix,self.freqlow,self.freqhigh,self.fftsize)
        self.formatter.legend = "GMT,LMST,TP,DEC=%f,LONGITUDE=%f,LATITUDE=%f,AMSL=%f,FREQ=%f,BW=%f" % (self.decln,self.longitude,self.latitude,self.amsl,self.ifreq/1.0e6, self.srate/1.0e6)

    def get_altitude(self):
        return self.altitude

    def set_altitude(self, altitude):
        self.altitude = altitude
        self.set_decln(self.altitude-self.latitude)

    def get_pacer(self):
        return self.pacer

    def set_pacer(self, pacer):
        self.pacer = pacer
        self.set_tiktok(self.pacer*0.0)

    def get_decln(self):
        return self.decln

    def set_decln(self, decln):
        self.decln = decln
        self.set_declnstr( str("%3.2f" % self.decln) if (self.decln<0) else "+"+str("%3.2f" % (self.decln)))
        self.set_prefix( "%3.2f" % (self.decln))
        self.formatter.legend = "GMT,LMST,TP,DEC=%f,LONGITUDE=%f,LATITUDE=%f,AMSL=%f,FREQ=%f,BW=%f" % (self.decln,self.longitude,self.latitude,self.amsl,self.ifreq/1.0e6, self.srate/1.0e6)

    def get_tiktok(self):
        return self.tiktok

    def set_tiktok(self, tiktok):
        self.tiktok = tiktok
        self.set_LMST(ra_funcs.cur_sidereal(self.Longitude+self.tiktok).replace(",",":"))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_dophigh(((self.samp_rate/2.0)/self.ifreq)*299792.0)
        self.set_doplow(-((self.samp_rate/2.0)/self.ifreq)*299792.0)
        self.set_fftrate(int(self.samp_rate/self.fftsize))
        self.set_freqhigh((self.ifreq+(self.samp_rate/2.0))/1.0e6)
        self.set_freqlow((self.ifreq-(self.samp_rate/2.0))/1.0e6)
        self.set_freqstep((self.samp_rate/self.fftsize)/1.0e6)
        self.blocks_keep_one_in_n_0.set_n((int(int(self.samp_rate/self.data_rate)/self.split_ratio)))
        self.osmosdr_source_1.set_sample_rate(self.samp_rate)
        self.single_pole_iir_filter_xx_0.set_taps((ra_funcs.getalpha(1.0/self.itinteg,self.samp_rate/self.split_ratio)))

    def get_ifreq(self):
        return self.ifreq

    def set_ifreq(self, ifreq):
        self.ifreq = ifreq
        self.set_actual_freq(self.ifreq)
        self.set_dophigh(((self.samp_rate/2.0)/self.ifreq)*299792.0)
        self.set_doplow(-((self.samp_rate/2.0)/self.ifreq)*299792.0)
        self.set_freqhigh((self.ifreq+(self.samp_rate/2.0))/1.0e6)
        self.set_freqlow((self.ifreq-(self.samp_rate/2.0))/1.0e6)
        Qt.QMetaObject.invokeMethod(self._ifreq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.ifreq)))
        self.formatter.legend = "GMT,LMST,TP,DEC=%f,LONGITUDE=%f,LATITUDE=%f,AMSL=%f,FREQ=%f,BW=%f" % (self.decln,self.longitude,self.latitude,self.amsl,self.ifreq/1.0e6, self.srate/1.0e6)

    def get_gmt(self):
        return self.gmt

    def set_gmt(self, gmt):
        self.gmt = gmt

    def get_fftsize(self):
        return self.fftsize

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize
        self.set_fftrate(int(self.samp_rate/self.fftsize))
        self.set_freqstep((self.samp_rate/self.fftsize)/1.0e6)
        self.set_winpower(sum([x*x for x in window.blackman_harris(self.fftsize)]))
        self.ezRAvectorlogger.legend = "lat %g  long %g  amsl %g  name %s\nfreqMin %g  freqMax %g  freqBinQty %g" % (self.latitude,self.Longitude,self.amsl,self.prefix,self.freqlow,self.freqhigh,self.fftsize)
        self.qtgui_vector_sink_f_1.set_x_axis(self.doplow if (self.velocity == True) else self.freqlow, (((self.dophigh-self.doplow)/self.fftsize) if (self.velocity == 1) else self.freqstep))

    def get_declnstr(self):
        return self.declnstr

    def set_declnstr(self, declnstr):
        self.declnstr = declnstr
        self.set_idecln(self.declnstr)

    def get_Longitude(self):
        return self.Longitude

    def set_Longitude(self, Longitude):
        self.Longitude = Longitude
        self.set_LMST(ra_funcs.cur_sidereal(self.Longitude+self.tiktok).replace(",",":"))
        self.ezRAvectorlogger.legend = "lat %g  long %g  amsl %g  name %s\nfreqMin %g  freqMax %g  freqBinQty %g" % (self.latitude,self.Longitude,self.amsl,self.prefix,self.freqlow,self.freqhigh,self.fftsize)
        self.formatter.longitude = self.Longitude

    def get_winpower(self):
        return self.winpower

    def set_winpower(self, winpower):
        self.winpower = winpower

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity
        self._velocity_callback(self.velocity)
        self.qtgui_vector_sink_f_1.set_x_axis(self.doplow if (self.velocity == True) else self.freqlow, (((self.dophigh-self.doplow)/self.fftsize) if (self.velocity == 1) else self.freqstep))
        self.qtgui_vector_sink_f_1.set_x_axis_units("km/s" if (self.velocity == 1) else "MHz")

    def get_variable_qtgui_label_rf(self):
        return self.variable_qtgui_label_rf

    def set_variable_qtgui_label_rf(self, variable_qtgui_label_rf):
        self.variable_qtgui_label_rf = variable_qtgui_label_rf
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_rf_label, "setText", Qt.Q_ARG("QString", str(self._variable_qtgui_label_rf_formatter(self.variable_qtgui_label_rf))))

    def get_variable_qtgui_label_Location(self):
        return self.variable_qtgui_label_Location

    def set_variable_qtgui_label_Location(self, variable_qtgui_label_Location):
        self.variable_qtgui_label_Location = variable_qtgui_label_Location
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_Location_label, "setText", Qt.Q_ARG("QString", str(self._variable_qtgui_label_Location_formatter(self.variable_qtgui_label_Location))))

    def get_variable_qtgui_label_3(self):
        return self.variable_qtgui_label_3

    def set_variable_qtgui_label_3(self, variable_qtgui_label_3):
        self.variable_qtgui_label_3 = variable_qtgui_label_3
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_3_label, "setText", Qt.Q_ARG("QString", str(self._variable_qtgui_label_3_formatter(self.variable_qtgui_label_3))))

    def get_variable_qtgui_label_1(self):
        return self.variable_qtgui_label_1

    def set_variable_qtgui_label_1(self, variable_qtgui_label_1):
        self.variable_qtgui_label_1 = variable_qtgui_label_1
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_1_label, "setText", Qt.Q_ARG("QString", str(self._variable_qtgui_label_1_formatter(self.variable_qtgui_label_1))))

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0))))

    def get_today(self):
        return self.today

    def set_today(self, today):
        self.today = today

    def get_split_ratio(self):
        return self.split_ratio

    def set_split_ratio(self, split_ratio):
        self.split_ratio = split_ratio
        self.blocks_keep_one_in_n_0.set_n((int(int(self.samp_rate/self.data_rate)/self.split_ratio)))
        self.blocks_multiply_const_xx_0.set_k((1.0/self.split_ratio)*self.dc_gain)
        self.single_pole_iir_filter_xx_0.set_taps((ra_funcs.getalpha(1.0/self.itinteg,self.samp_rate/self.split_ratio)))

    def get_seconds(self):
        return self.seconds

    def set_seconds(self, seconds):
        self.seconds = seconds

    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.ezRAvectorlogger.filepat = 'ezRA%04d%02d%02d'+'_'+self.prefix
        self.ezRAvectorlogger.legend = "lat %g  long %g  amsl %g  name %s\nfreqMin %g  freqMax %g  freqBinQty %g" % (self.latitude,self.Longitude,self.amsl,self.prefix,self.freqlow,self.freqhigh,self.fftsize)
        self.formatter.filepat = 'tp-%04d%02d%02d'+'_'+self.prefix
        self.vectorlogger.filepat = 'fft-%04d%02d%02d'+'_'+self.prefix

    def get_ltp(self):
        return self.ltp

    def set_ltp(self, ltp):
        self.ltp = ltp

    def get_itinteg(self):
        return self.itinteg

    def set_itinteg(self, itinteg):
        self.itinteg = itinteg
        self.single_pole_iir_filter_xx_0.set_taps((ra_funcs.getalpha(1.0/self.itinteg,self.samp_rate/self.split_ratio)))

    def get_isinteg(self):
        return self.isinteg

    def set_isinteg(self, isinteg):
        self.isinteg = isinteg
        self.single_pole_iir_filter_xx_1.set_taps((ra_funcs.getalpha(1.0/self.isinteg,self.fftrate)))

    def get_irfgain(self):
        return self.irfgain

    def set_irfgain(self, irfgain):
        self.irfgain = irfgain

    def get_idecln(self):
        return self.idecln

    def set_idecln(self, idecln):
        self.idecln = idecln
        Qt.QMetaObject.invokeMethod(self._idecln_label, "setText", Qt.Q_ARG("QString", str(self._idecln_formatter(self.idecln))))

    def get_freqstep(self):
        return self.freqstep

    def set_freqstep(self, freqstep):
        self.freqstep = freqstep
        self.qtgui_vector_sink_f_1.set_x_axis(self.doplow if (self.velocity == True) else self.freqlow, (((self.dophigh-self.doplow)/self.fftsize) if (self.velocity == 1) else self.freqstep))

    def get_freqlow(self):
        return self.freqlow

    def set_freqlow(self, freqlow):
        self.freqlow = freqlow
        self.ezRAvectorlogger.legend = "lat %g  long %g  amsl %g  name %s\nfreqMin %g  freqMax %g  freqBinQty %g" % (self.latitude,self.Longitude,self.amsl,self.prefix,self.freqlow,self.freqhigh,self.fftsize)
        self.qtgui_vector_sink_f_1.set_x_axis(self.doplow if (self.velocity == True) else self.freqlow, (((self.dophigh-self.doplow)/self.fftsize) if (self.velocity == 1) else self.freqstep))

    def get_freqhigh(self):
        return self.freqhigh

    def set_freqhigh(self, freqhigh):
        self.freqhigh = freqhigh
        self.ezRAvectorlogger.legend = "lat %g  long %g  amsl %g  name %s\nfreqMin %g  freqMax %g  freqBinQty %g" % (self.latitude,self.Longitude,self.amsl,self.prefix,self.freqlow,self.freqhigh,self.fftsize)

    def get_filechoice(self):
        return self.filechoice

    def set_filechoice(self, filechoice):
        self.filechoice = filechoice
        self._filechoice_callback(self.filechoice)
        self.blocks_selector_0.set_output_index(self.filechoice)

    def get_fftrate(self):
        return self.fftrate

    def set_fftrate(self, fftrate):
        self.fftrate = fftrate
        self.blocks_keep_one_in_n_1.set_n((int(self.fftrate/self.data_rate)))
        self.single_pole_iir_filter_xx_1.set_taps((ra_funcs.getalpha(1.0/self.isinteg,self.fftrate)))

    def get_doplow(self):
        return self.doplow

    def set_doplow(self, doplow):
        self.doplow = doplow
        self.qtgui_vector_sink_f_1.set_x_axis(self.doplow if (self.velocity == True) else self.freqlow, (((self.dophigh-self.doplow)/self.fftsize) if (self.velocity == 1) else self.freqstep))

    def get_dophigh(self):
        return self.dophigh

    def set_dophigh(self, dophigh):
        self.dophigh = dophigh
        self.qtgui_vector_sink_f_1.set_x_axis(self.doplow if (self.velocity == True) else self.freqlow, (((self.dophigh-self.doplow)/self.fftsize) if (self.velocity == 1) else self.freqstep))

    def get_dc_gain(self):
        return self.dc_gain

    def set_dc_gain(self, dc_gain):
        self.dc_gain = dc_gain
        self._dc_gain_callback(self.dc_gain)
        self.blocks_multiply_const_xx_0.set_k((1.0/self.split_ratio)*self.dc_gain)

    def get_data_rate(self):
        return self.data_rate

    def set_data_rate(self, data_rate):
        self.data_rate = data_rate
        self.blocks_keep_one_in_n_0.set_n((int(int(self.samp_rate/self.data_rate)/self.split_ratio)))
        self.blocks_keep_one_in_n_1.set_n((int(self.fftrate/self.data_rate)))
        self.qtgui_vector_sink_f_0.set_update_time((1.0/(self.data_rate)))
        self.qtgui_vector_sink_f_1.set_update_time((1.0/(self.data_rate)))
        self.stripchart_0.decim = self.data_rate

    def get_correct_baseline(self):
        return self.correct_baseline

    def set_correct_baseline(self, correct_baseline):
        self.correct_baseline = correct_baseline
        self._correct_baseline_callback(self.correct_baseline)
        self.baseline_compensate.collect = True if self.correct_baseline == False else False

    def get_azimut(self):
        return self.azimut

    def set_azimut(self, azimut):
        self.azimut = azimut

    def get_amsl(self):
        return self.amsl

    def set_amsl(self, amsl):
        self.amsl = amsl
        self.ezRAvectorlogger.legend = "lat %g  long %g  amsl %g  name %s\nfreqMin %g  freqMax %g  freqBinQty %g" % (self.latitude,self.Longitude,self.amsl,self.prefix,self.freqlow,self.freqhigh,self.fftsize)
        self.formatter.legend = "GMT,LMST,TP,DEC=%f,LONGITUDE=%f,LATITUDE=%f,AMSL=%f,FREQ=%f,BW=%f" % (self.decln,self.longitude,self.latitude,self.amsl,self.ifreq/1.0e6, self.srate/1.0e6)

    def get_actual_freq(self):
        return self.actual_freq

    def set_actual_freq(self, actual_freq):
        self.actual_freq = actual_freq
        self.osmosdr_source_1.set_center_freq(self.actual_freq, 0)

    def get_LMST(self):
        return self.LMST

    def set_LMST(self, LMST):
        self.LMST = LMST
        Qt.QMetaObject.invokeMethod(self._LMST_label, "setText", Qt.Q_ARG("QString", str(self._LMST_formatter(self.LMST))))



def argument_parser():
    description = 'A simple spectro radiometer for radiastronmy'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--dmult", dest="dmult", type=eng_float, default=eng_notation.num_to_str(float(100)),
        help="Set Detector Multiplier [default=%(default)r]")
    parser.add_argument(
        "--freq", dest="freq", type=eng_float, default=eng_notation.num_to_str(float(1420.4058e6)),
        help="Set RF Frequency (Hz) [default=%(default)r]")
    parser.add_argument(
        "--logtime", dest="logtime", type=eng_float, default=eng_notation.num_to_str(float(5.0)),
        help="Set Logging Interval (secs) [default=%(default)r]")
    parser.add_argument(
        "--longitude", dest="longitude", type=eng_float, default=eng_notation.num_to_str(float(2.552186)),
        help="Set Longitude [default=%(default)r]")
    parser.add_argument(
        "--rfgain", dest="rfgain", type=eng_float, default=eng_notation.num_to_str(float(49)),
        help="Set RF Gain (dB) [default=%(default)r]")
    parser.add_argument(
        "--sinteg", dest="sinteg", type=eng_float, default=eng_notation.num_to_str(float(60.0)),
        help="Set Integraton Time(secs) for Spectrum [default=%(default)r]")
    parser.add_argument(
        "--srate", dest="srate", type=eng_float, default=eng_notation.num_to_str(float(2.5e6)),
        help="Set Sample Rate (SPS) [default=%(default)r]")
    parser.add_argument(
        "--tinteg", dest="tinteg", type=eng_float, default=eng_notation.num_to_str(float(60)),
        help="Set Integraton Time(secs) for TP [default=%(default)r]")
    parser.add_argument(
        "--utc", dest="utc", type=intx, default=1,
        help="Set Log in UTC time [default=%(default)r]")
    parser.add_argument(
        "--vf", dest="vf", type=intx, default=1,
        help="Set vf [default=%(default)r]")
    return parser


def main(top_block_cls=gsr, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(dmult=options.dmult, freq=options.freq, logtime=options.logtime, longitude=options.longitude, rfgain=options.rfgain, sinteg=options.sinteg, srate=options.srate, tinteg=options.tinteg, utc=options.utc, vf=options.vf)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()

"""Main module."""

"""
Created on Thu Feb 13 15:59:48 2020

@author: RAEK2031
"""

import sys
from os import makedirs, remove, stat
from os.path import dirname, isdir, isfile, join

import matplotlib.pyplot as plt
import mne
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button, RectangleSelector
from mne.channels._standard_montage_utils import _read_theta_phi_in_degrees
from mne.defaults import HEAD_SIZE_DEFAULT

mne.set_log_level('WARNING')

print(f'RE script imported.')


def ABto1020():
    return {'A1': 'Fp1', 'A2': 'AF7', 'A3': 'AF3', 'A4': 'F1', 'A5': 'F3',
            'A6': 'F5', 'A7': 'F7', 'A8': 'FT7', 'A9': 'FC5', 'A10': 'FC3',
            'A11': 'FC1', 'A12': 'C1', 'A13': 'C3', 'A14': 'C5',
            'A15': 'T7', 'A16': 'TP7', 'A17': 'CP5', 'A18': 'CP3',
            'A19': 'CP1', 'A20': 'P1', 'A21': 'P3', 'A22': 'P5',
            'A23': 'P7', 'A24': 'P9', 'A25': 'PO7', 'A26': 'PO3',
            'A27': 'O1', 'A28': 'Iz', 'A29': 'Oz', 'A30': 'POz',
            'A31': 'Pz', 'A32': 'CPz', 'B1': 'Fpz', 'B2': 'Fp2',
            'B3': 'AF8', 'B4': 'AF4', 'B5': 'AFz', 'B6': 'Fz', 'B7': 'F2',
            'B8': 'F4', 'B9': 'F6', 'B10': 'F8', 'B11': 'FT8',
            'B12': 'FC6', 'B13': 'FC4', 'B14': 'FC2', 'B15': 'FCz',
            'B16': 'Cz', 'B17': 'C2', 'B18': 'C4', 'B19': 'C6',
            'B20': 'T8', 'B21': 'TP8', 'B22': 'CP6', 'B23': 'CP4',
            'B24': 'CP2', 'B25': 'P2', 'B26': 'P4', 'B27': 'P6',
            'B28': 'P8', 'B29': 'P10', 'B30': 'PO8', 'B31': 'PO4',
            'B32': 'O2'}


def addbox(x, y, ax, text=False, ypos=False, size=False, **kwargs):
    """
    Add a box object with text to a plot.

    Parameters
    ----------
    x : list
        The x range of the box.
    y : list
        The y range of the box.
    ax : axis
        :class:`~matplotlib.axes.Axes` object to plot into.
    text : str, optional
        Text on the created box. The default is False.
    ypos : float, optional
        Location of the text in proportion of the figure hight. False means at
        the bottom of the plot. The default is False.
    size : int | float, optional
        Size of the text. The default is False.

    Returns
    -------
    None.

    """
    if y == False:
        y = ax.get_ylim()
    if not kwargs:
        kwargs = {'facecolor': 'gray', 'alpha': 0.2}
    ax.add_patch(Rectangle(xy=(x[0], y[0]), width=float(
        np.diff(x)), height=float(np.diff(y)), **kwargs))
    if text:
        lim = ax.get_ylim()
        ax.annotate(text, xy=(np.mean(x), float(
            lim[0] + (np.diff(lim)*ypos))), size=size, ha='center')


def color_linestyle(names, colors, linestyles=False):
    """
    Generate keyword arguments for color and linestyles

    Parameters
    ----------
    names : list
        ERP names.
    colors : list
        Colors.
    linestyles : list, optional
        Linestyles. The default is False.

    Returns
    -------
    dict
        Dictionary with keyword arguments.

    """
    if not linestyles:
        linestyles = len(names)*['-']
    return {k: {name: cl for name, cl in zip(names, v)} for k, v in [['colors', colors], ['linestyles', linestyles]]}


def DIFF(a, b, data):
    """
    Generate difference wave between condition A and B.

    Parameters
    ----------
    a : str
        Condition A.
    b : str
        Condition B.
    erp : dict
        Dictionary with subjectnumber as key and mne.epochs as value.

    Returns
    -------
    list
        DESCRIPTION.

    """
    return mne.combine_evoked([data[a].average(), data[b].average()], weights=(1, -1))


def ERP_average(cond, erp, fp, bads=False, name=False):
    data = erp[fp].copy().drop(bads)
    evoked = DIFF(*tuple(cond.split(' - ')),
                  data) if ' - ' in cond else data[cond].average()
    if name:
        evoked.comment = name
    return evoked


def ERP(conds, data, fps, names=False, lp30=False, bads=False, crop=(None, None), baseline=None, reference=False):
    """
    Generate dictionary with conditions as keys and evokeds as values.
    Calculate difference waves by using minus " - " between conditions.

    Parameters
    ----------
    conds : list
        Names of conditions to include.
    erp : dict
        Dictionary with subject number as key and epochs as values.
    fps : list
        Subjects to include.
    names : list, optional
        Desired names of the conditions. If false, use original names.
        The default is False.
    lp30 : bool
        Apply 30hz low pass filter to the data.
    bads : dict
        Exclude bad trials. Provided as a dictionary with subject id as keys
        and list of bad trial indices as value.
    crop : list
        Start and stop for crop
    baseline : list
        Start and stop for baseline
    Returns
    -------
    dict
        Dictionary with ERPs.

    """
    if not isinstance(fps, (list, np.ndarray)):
        fps = [fps]
    if not isinstance(conds, (list, np.ndarray)):
        conds = [conds]

    d = {k: [] for k in (conds if not names else names)}
    for fp in loadbar(fps, f'Averaging {", ".join(conds)}'):
        for cond, name in zip(conds, conds if not names else names):
            if baseline:
                d[name] += [ERP_average(cond, data, fp, bads[fp] if bads else False).copy().crop(
                    *crop).apply_baseline(baseline=baseline)]
            else:
                d[name] += [ERP_average(cond, data, fp, bads[fp]
                                        if bads else False).copy().crop(*crop)]
    if (len(list(d)) == 1) & (names == False):
        d = d[list(d)[0]]
    if lp30:
        d = LP30hz(d)
    if reference:
        for cond in list(d):
            for i in d[cond]:
                i.set_eeg_reference(ref_channels=reference)
    return d


def extr_mean_amp(evoked, times, channels, ts, freqs=False, fqs=False):
    '''
    Extract mean amplitudes from a time interval and channel selection.

    Parameters
    ----------
    evoked : MNE evoked numpy array
    times : list (all t)
    channels : list
        List of channels with each item as a channel index
    ts : list
        List of two time points, a time range in seconds (e.g., [0.1, 0.2])

    Returns
    -------
    float
        Mean amplitude
    '''
    time = time_selection(times, *ts)
    if freqs is not False:
        freqs = np.where(np.in1d(freqs, fqs))[0]
        out = evoked[channels][:, freqs][:, :, time].mean()
    else:
        out = evoked[channels][:, time].mean()*1e6
    return out


def LP30hz(data):
    """
    Apply 30 hz low-pass filter for figures.

    Parameters
    ----------
    erp : dict | list
        Dictionary with condition as key and list of epochs as value or list
        of epochs.

    Returns
    -------
    list
        List of low-pass filtered evokeds.

    """
    x = data.copy()
    if type(x) == dict:
        for cond in loadbar(list(x), 'Applying a 30Hz low-pass filter...'):
            for fp in x[cond]:
                fp.filter(h_freq=30, l_freq=None, n_jobs=-1)
    elif type(x) == list:
        for fp in loadbar(x, 'Applying a 30Hz low-pass filter...'):
            fp.filter(h_freq=30, l_freq=None, n_jobs=-1)
    else:
        x.filter(h_freq=30, l_freq=None, n_jobs=-1)
    return x


def loadbar(it, title='Loading', size=80):
    """
    Loadbar for iterables.

    Parameters
    ----------
    it : iterable
        Iterable to loop through.
    title : str, optional
        Title of the loadbar. The default is 'Loading'.
    env : str (anaconda or spyder)
        Loadbar that works in spyder or anaconda prompt
    size : int, optional
        Lenght of loadbar. The default is 80.

    Yields
    ------
    item : iterable
        Feed iterable through.

    """

    file = sys.stdout
    count = len(it)

    def show(j):
        x = int(size*j/count)
        file.write('%s [%s%s] %i/%i\r' %
                   (title, "#"*x, "."*(size-x), j, count))
        file.flush()
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write('\n')
    file.flush()


class MakeIOfiles:
    kind_ext = {'log': '.tsv', 'bdf': '.bdf', 'raw': '-raw.fif', 'eve': '-eve.fif', 'ica': '-ica.fif',
                'bad_trials': '_bad_trials.txt', 'bad_channels': '_bad_channels.txt',
                'epo': '-epo.fif', 'ave': '-ave.fif', 'cov': '-cov.fif', 'tfr': '-tfr.h5'}

    def __init__(self, main, format_function=False, data_folder=False, files_folder=False, folder_format=False, file_format=False):
        self.main = main
        self.format_function = format_function
        self.data_folder = data_folder
        self.files_folder = files_folder
        self.folder_format = folder_format
        self.file_format = file_format
        self.paths, self.functions = self.create_paths()

    def __repr__(self):
        s = 'Files: '
        # nfiles = {kind: sum(isfile(self.format_path(kind, ids)) for ids in [1]) for kind in self.kind_ext}
        # s += ''.join([f'{kind}: {n}, ' for kind, n in nfiles.items()])
        class_name = self.__class__.__name__
        return '<%s | %s>' % (class_name, s)

    def __call__(self, kind, ids=None):
        return self.format_path(kind, ids)

    def create_paths(self):
        files = join(self.main, 'MNE', 'files')
        data = join(self.main, 'data')
        paths = {'files': files,
                 'data': data,
                 'results': join(self.main, 'results'),
                 'figures': join(self.main, 'results', 'figures'),
                 'individuals': join(self.main, 'results', 'figures', 'individuals')}

        parts = ['data_folder', 'files_folder',
                 'folder_format', 'file_format', 'format_function']
        standard_forms = [data, files, 'fp%02d', 'fp%02d', lambda x: [x]*2]
        defaults = {part: {kind: iformat for kind in self.kind_ext}
                    for part, iformat in zip(parts, standard_forms)}
        data_special = {'data_folder': {'log': join(data, 'log'), 'bdf': join(
            data, 'bdf')}, 'folder_format': {'bdf': False}, 'format_function': {'bdf': lambda x: [x]}}
        for part, values in data_special.items():
            defaults[part].update(values)

        for part, values in dict(zip(parts, map(eval, ['self.'+i for i in parts]))).items():
            if isinstance(values, dict):
                defaults[part].update(values)
            elif isinstance(values, str) or callable(values):
                defaults[part].update({kind: values for kind in self.kind_ext})

        exclude = {kind: 'data_folder' if kind not in [
            'log', 'bdf'] else 'files_folder' for kind in self.kind_ext}
        paths.update({kind: join(*[defaults[part][kind] for part in [part for part in parts if not exclude[kind] == part] if (
            defaults[part][kind] != False) and (part != 'format_function')])+ext for kind, ext in self.kind_ext.items()})
        return paths, defaults['format_function']

    def format_path(self, kind, ids):
        if ids:
            path = self.paths[kind] % tuple(self.functions[kind](ids))
        else:
            path = self.paths[kind]
        return path

    @staticmethod
    def create_directories(file):
        if not isdir(dirname(file)):
            print(f'Making: {file}.')
            makedirs(dirname(file))

    def save(self, values, kind, ids, make_dirs=False):
        '''
        Save `bad_channels` or `bad_trials`

        Parameters
        ----------
        values : list
            list of bad channels (str) or trials (indices)
        kind : str (`bad_channels` or `bad_trials`)
            `bad_channels` or `bad_trials`
        ids : any
            Subject identifier
        make_dirs : bool (default = False)
            Make directories to the file.
        Returns
        -------
        None
        '''
        file = self.format_path(kind, ids)
        if make_dirs:
            self.create_directories(file)
        with open(file, 'w') as f:
            f.write(','.join(map(str, values)))

    def load(self, kind, ids):
        '''
        Load `bad_channels` or `bad_trials`

        Parameters
        ----------
        kind : str (`bad_channels` or `bad_trials`)
            `bad_channels` or `bad_trials`
        ids : any
            Subject identifier

        Returns
        -------
        list of bad trials or channels
        '''
        file = self.format_path(kind, ids)
        value_type = {'bad_trials': int, 'bad_channels': str}[kind]
        if isfile(file):
            if stat(file).st_size == 0:
                values = []
            else:
                with open(file, 'r') as f:
                    values = list(map(value_type, f.readline().split(',')))
        else:
            print(f'No {kind} file. Making empty list.')
            values = []
        return values


def preprocess_stats(iofiles, fps, ret=False, header='Preprocessing stats'):
    """
    Descriptive statistics of number of interpolated channels, removed trials,
    and applied ICA components.

    Parameters
    ----------
    iofiles : dict
        Dictionary with folder structure.
    n_trials : int
        Total number of trials.
    fps : list
        List of subjects values.
    ret : bool, optional
        True to return dataframe with statistics. The default is False.
    header : str
        Header for the print. The default is "Preprocessing stats".

    Returns
    -------
    pandas dataframe
        Statistics.

    """
    chs = [len(iofiles.load('bad_channels', fp)) for fp in fps]
    all_trs = np.array(
        [mne.read_epochs(iofiles('epo', fp), preload=False).__len__() for fp in fps])
    trs = np.array([len(iofiles.load('bad_trials', fp)) for fp in fps])
    icas = [len(mne.preprocessing.read_ica(iofiles('ica', fp)).exclude)
            for fp in fps]
    Section(header)
    print(
        f'Subjects = {len(fps)}, trials = {np.mean(all_trs)} (max: {max(all_trs)}, min: {min(all_trs)})')
    print(
        f'Interpolated channels M = {np.mean(chs):.02f} (SD = {np.std(chs):.02f}).')
    print(
        f'Components removed M = {np.mean(icas):.02f} (SD = {np.std(icas):.02f}).')
    print(f'Trials removed M = {np.mean(trs):.02f} (SD = {np.std(trs):.02f}), corresponding to M = {np.mean(trs/all_trs)*100:.02f}% (SD = {np.std(trs/all_trs)*100:.02f}).')
    if ret:
        return pd.DataFrame({'fp': fps, 'bad_ch': chs, 'trials': trs, 'icas': icas})


def make_mask(channels, times, mask_channels):
    """
    Makes a mask to highlight channels.

    Parameters
    ----------
    channels : list
        All channels.
    times : list
        List of timepoints.
    mask_channels : list
        The channels to highlight.

    Returns
    -------
    list
        Boolean mask.
    """
    mask = np.zeros(shape=(len(channels), len(times)), dtype=bool)
    mask[np.array(mask_channels)] = True
    return mask


def time_selection(times, start, stop):
    """
    Get sample indices for a time selection.

    Parameters
    ----------
    times : list
        Sample times.
    start : float
        Start time in seconds.
    stop : float
        End time in seconds.

    Returns
    -------
    list
        Sample indices of time selection.

    """
    ix = np.where((times >= start) & (times <= stop))
    return list(ix[0])


def Section(text='text'):
    """
    Print heading like separator with custom text.

    Parameters
    ----------
    text : str, optional
        Optional heading text. The default is 'text'.

    Returns
    -------
    None.

    """
    print('{:=<78} #\n{:^80}\n{:=<78} #'.format('# ', text, '# '))


def make_montage(funcdir):
    DATA = """
    Fp1	-92	-72
    AF7	-92	-54
    AF3	-74	-65
    F1	-50	-68
    F3	-60	-51
    F5	-75	-41
    F7	-92	-36
    FT7	-92	-18
    FC5	-72	-21
    FC3	-50	-28
    FC1	-32	-45
    C1	-23	0
    C3	-46	0
    C5	-69	0
    T7	-92	0
    TP7	-92	18
    CP5	-72	21
    CP3	-50	28
    CP1	-32	45
    P1	-50	68
    P3	-60	51
    P5	-75	41
    P7	-92	36
    P9	-115	36
    PO7	-92	54
    PO3	-74	65
    O1	-92	72
    Iz	115	-90
    Oz	92	-90
    POz	69	-90
    Pz	46	-90
    CPz	23	-90
    Fpz	92	90
    Fp2	92	72
    AF8	92	54
    AF4	74	65
    AFz	69	90
    Fz	46	90
    F2	50	68
    F4	60	51
    F6	75	41
    F8	92	36
    FT8	92	18
    FC6	72	21
    FC4	50	28
    FC2	32	45
    FCz	23	90
    Cz	0	0
    C2	23	0
    C4	46	0
    C6	69	0
    T8	92	0
    TP8	92	-18
    CP6	72	-21
    CP4	50	-28
    CP2	32	-45
    P2	50	-68
    P4	60	-51
    P6	75	-41
    P8	92	-36
    P10	115	-36
    PO8	92	-54
    PO4	74	-65
    O2	92	-72
    Nz	 115	 90
    LPA	-115	  0
    RPA	 115	  0
    MyNas	 115	 90
    MyCheek	 -112	 -72
    """

    with open(join(funcdir, 'chs.tsv'), 'w') as fout:
        fout.write(DATA)


def load_montage(funcdir):
    file = join(funcdir, 'chs.tsv')
    if not isfile(file):
        make_montage(funcdir)
    montage = _read_theta_phi_in_degrees(fname=file, head_size=HEAD_SIZE_DEFAULT,
                                         fid_names=['Nz', 'LPA', 'RPA'],
                                         add_fiducials=False)
    remove(file)
    return(montage)


class Highlighter(object):
    '''
    Credit to Joe Kington:
    https://stackoverflow.com/a/31926249
    '''

    def __init__(self, ax, x, y):
        self.ax = ax
        self.canvas = ax.figure.canvas
        self.x, self.y = x, y
        self.mask = np.zeros(x.shape, dtype=bool)
        self._highlight = ax.scatter([], [], s=2, color='yellow', zorder=10)
        self.selector = RectangleSelector(ax, self, useblit=True)

    def __call__(self, event1, event2):
        self.mask |= self.inside(event1, event2)
        xy = np.column_stack([self.x[self.mask], self.y[self.mask]])
        self._highlight.set_offsets(xy)
        self.canvas.draw()

    def inside(self, event1, event2):
        """Returns a boolean mask of the points inside the rectangle defined by
        event1 and event2."""
        # Note: Could use points_inside_poly, as well
        x0, x1 = sorted([event1.xdata, event2.xdata])
        y0, y1 = sorted([event1.ydata, event2.ydata])
        mask = ((self.x > x0) & (self.x < x1) &
                (self.y > y0) & (self.y < y1))
        return mask


def toggle(ar1, ar2):
    for i in ar1:
        if i in ar2:
            ar2 = np.delete(ar2, np.where(ar2 == i))
        elif i not in ar2:
            ar2 = np.sort(np.append(ar2, i))
    return(ar2)


def rejectvisual(epochs, fp, start, stop, selected):
    ch_index = np.array([epochs.ch_names.index(ch)
                         for ch in epochs.ch_names])  # channel indicies
    trial_index = np.arange(len(epochs))  # Trial indicies
    # Time interval within epoch to extract peak to peak from
    time_interval = np.where((epochs.times >= start) & (epochs.times <= stop))
    # List of trials with list of channels containing peak to peak amplitudes
    ptp = np.array([[np.ptp(ch[time_interval]) for ch in t] for t in epochs])
    # loop while trials or channels are selected
    if selected != []:
        trial_index = toggle(np.array(selected), np.arange(len(epochs)))
    else:
        trial_index = np.arange(len(epochs))
    test = 1

    def plot_bad_trials(event):
        scale = np.median([max(ptp[bad_trials][:, ch]) for ch in ch_index])
        epochs[bad_trials].plot(picks=ch_index, n_channels=len(
            ch_index), scalings=dict(eeg=scale), title='FP: %s' % fp, n_epochs=40)

    def plot_good_trials(event):
        scale = np.median([max(ptp[trial_index][:, ch]) for ch in ch_index])
        epochs[trial_index].plot(picks=ch_index, n_channels=len(
            ch_index), scalings=dict(eeg=scale), title='FP: %s' % fp, n_epochs=40)
    while test != 0:
        bad_trials = np.setdiff1d(np.arange(len(epochs)), trial_index)
        bad_channels = np.setdiff1d(np.arange(len(epochs.ch_names)), ch_index)
        ptp_clean = ptp.copy()
        ptp_clean[bad_trials] = np.zeros(np.shape(ptp[bad_trials]))
        # Make plot
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(
            2, 2, figsize=[14, 8], frameon=False)
        fig.suptitle('Subject: %s' % fp, fontsize=16)
        ax1.set_xlabel('Trial number')
        ax1.set_ylabel('Channel')
        ax2.set_xlabel('µV')
        ax2.set_ylabel('Channel')
        ax3.set_xlabel('Trial number')
        ax3.set_ylabel('µV')
        ax4.set_xlabel('Trial number')
        ax4.set_ylabel('µV')
        text = 'Drag the mouse over the trials you wish to reject. Toggle channels by selecting them.\n\nEpoch interval: %.0f to %.0f ms.\nSelected trials: %i/%i (%.2f%%)\nSelected channels: %i/%i' % (
            start*1000, stop*1000, len(bad_trials), len(epochs), len(bad_trials)/len(epochs)*100, len(bad_channels), len(epochs.ch_names))
        plt.gcf().text(0.02, 0.02, text, fontsize=12)
        # Add button to plot bad trials
        plt.subplots_adjust(top=0.92, bottom=0.18, left=0.06, right=0.96,
                            hspace=0.1, wspace=0.15)
        # Left, bottom, right, top
        axbutton1 = plt.axes([0.85, 0.02, 0.1, 0.04])
        axbutton2 = plt.axes([0.75, 0.02, 0.1, 0.04])
        btn1 = Button(axbutton1, 'Plot bad trials',
                      color='white', hovercolor='gray')
        btn2 = Button(axbutton2, 'Plot good trials',
                      color='white', hovercolor='gray')
        btn1.on_clicked(plot_bad_trials)
        btn2.on_clicked(plot_good_trials)

        # fig 1: Heatmap of x = trials, y = channels, z = max amplitude
        z1 = np.transpose(ptp_clean[:, ch_index])
        y1 = np.array(epochs.ch_names)[ch_index]  # names as y axis
        ax1.imshow(z1, aspect="auto")
        ax1.set_xlim([-1, len(epochs)])
        ax1.set_yticks(np.arange(len(y1)))
        ax1.set_yticklabels(y1)

        # fig 2: Max ptp amplitude per channel across trials
        x2 = np.array([max(ptp[trial_index, ch]) * 1e6 for ch in ch_index])
        y2 = ch_index
        ax2.scatter(x2, y2, color='blue', s=0.8)
        ax2.set_yticks(np.arange(len(y1)))
        ax2.set_yticklabels(y1)
        ax2.invert_yaxis()
        mask_ch_del = Highlighter(ax2, x2, y2)

        # fig 3: Max amplitude per trial across channels
        x3 = trial_index
        y3 = np.array([max(trial) * 1e6 for trial in ptp[trial_index]])
        ax3.scatter(x3, y3, color='blue', s=0.8)
        ax3.set_xlim([-1, len(epochs)])
        mask_tr_del = Highlighter(ax3, x3, y3)

        # fig 4: Removed trials
        x4 = np.setdiff1d(np.arange(len(epochs)), trial_index)
        y4 = np.array([max(trial) * 1e6 for trial in ptp[bad_trials]])
        ax4.scatter(x4, y4, color='blue', s=0.8)
        ax4.set_xlim([-1, len(epochs)+1])
        mask_tr_add = Highlighter(ax4, x4, y4)
        plt.show()

        # Remove selected trials from trial index
        ch_index = toggle(y2[mask_ch_del.mask], ch_index)
        trial_index = toggle(x3[mask_tr_del.mask], trial_index)
        trial_index = toggle(x4[mask_tr_add.mask], trial_index)
        bad_channels = np.setdiff1d(np.arange(len(epochs.ch_names)), ch_index)
        bad_trials = np.setdiff1d(np.arange(len(epochs)), trial_index)

        # print('Bad trials:', bad_trials)
        test = sum(np.concatenate(
            [mask_ch_del.mask, mask_tr_del.mask, mask_tr_add.mask]))
        if len(bad_channels) != 0:
            test = 1
            print('Bad channels:', np.array(epochs.ch_names)[bad_channels])
            x = input(
                'Add channels back (blank to leave out selected channels): ') or 'n'
            if x == 'all':
                ch_index = toggle(bad_channels, ch_index)
            elif x != 'n':
                ch_index = toggle([epochs.ch_names.index(ch)
                                   for ch in x.split(' ')], ch_index)
    return bad_trials

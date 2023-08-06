"""sonusai speech_enh

usage: speech_enh [-hvntxp] PFILE MIXDB [-i MIXID] [-g MINGAIN] [-m MODEL] [-w KMODEL] [-b BATCH]

options:
   -h, --help
   -v, --verbose                Be verbose.
   -n, --noise-est-enable       Extract noise in addition to speech and include metrics
   -t, --tru-est-mode           Calculate extraction using truth and include metrics
   -x, --disable-wav-write      Disable write of .wav files
   -p, --plot-enable            Write plot PDF for each mixture
   -g MINGAIN, --min-tgain      Optional minimum target gain threshold [default: 0.01]
   -m MODEL, --model MODEL      Optional .onnx model used if PFILE is .wav to generate prediction data
   -w KMODEL, --weights KMODEL  Keras model weights file, required if PFILE is a Keras .py Sonusai hypermodel
   -i MIXID, --mixid MIXID      Mixtures in MIXDB to use. [default: *]
   -b BATCH, --batch BATCH      Batch size if .py hypermodel is provided [default: 8]

Run speech enhancement using PFILE model or prediction file and dataset MIXDB SonusAI mixture database JSON file.

Speech is estimated using a given extraction method on the mixture transform, and optionally noise is also
extracted.

TBD:
Plot prediction data PFILE and optionally metrics and truth if feature+truth file is provided.
PFILE is an .hdf5 file with predict dataset or a .wav with a -m MODEL used to run prediction.

Spectrograms are plotted for truth types energy_f, snr_f, and mapped_snr_f.

INPUT is a hdf file one of the following:

    * WAV
      Using the given model, generate feature data and run prediction. A model file must be
      provided. The MIXID is ignored. If --energy is specified, plot predict data as energy.

    * JSON
      Using the given mixture database, generate feature and truth data. Run prediction if
      a model is given. The MIXID is required. (--energy is ignored.)

    * HDF5
      Using the given mixture database, generate feature and truth data. Run prediction if
      a model is given. The MIXID is required. (--energy is ignored.)

Prediction data will be written to OUTPUT if a model file is given and OUTPUT is specified.

There will be one plot per active truth index. In addition, the top 5 prediction classes are determined and
plotted if needed (i.e., if they were not already included in the truth plots). For plots generated using a
mixture database, then the target will also be displayed. If mixup is active, then each target involved will
be added to the corresponding truth plot.

Inputs:
    MODEL   A SonusAI trained ONNX model file. If a model file is given, prediction data will be
            generated.
    INPUT   A WAV file, or
            a JSON file containing a SonusAI mixture database, or
            an HDF5 file containing:
                attribute:  mixdb (required)

Outputs:
    {INPUT}-plot.pdf or {INPUT}-mix{MIXID}-plot.pdf
    plot.log
    OUTPUT (if MODEL and OUTPUT are both specified)

"""
from typing import List
from typing import Union

import matplotlib.pyplot as plt
import numpy as np

from sonusai import logger
from sonusai.mixture.mixdb import MixtureDatabase


def abs2(x):
    return x.real ** 2 + x.imag ** 2


def spec_plot(mixture: np.ndarray,
              feature: np.ndarray,
              predict: Union[np.ndarray, None] = None,
              target: Union[np.ndarray, None] = None,
              labels: Union[List[str], None] = None,
              title: str = '') -> plt.figure:
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.utils import int16_to_float

    num_plots = 4 if predict is not None else 2
    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the waveform
    x_axis = np.arange(len(mixture), dtype=np.float32) / SAMPLE_RATE
    ax[0].plot(x_axis, int16_to_float(mixture), label='Mixture')
    ax[0].set_xlim(x_axis[0], x_axis[-1])
    # ax[0].set_ylim([-1.025, 1.025])
    if target is not None:  # Plot target time-domain waveform on top of mixture
        color = 'tab:blue'
        ax[0].plot(x - axis, int16_to_float(target), color=color, label='Target')
        ax[0].set_ylabel('magnitude', color=color)
        # ax[0].tick_params(axis='y', labelcolor=color)
    ax[0].set_title('Waveform')

    # Plot the spectrogram
    ax[1].imshow(np.transpose(feature), aspect='auto', interpolation='nearest', origin='lower')
    ax[1].set_title('Feature')

    if predict is not None:
        # Plot and label the model output scores for the top-scoring classes.
        mean_predict = np.mean(predict, axis=0)
        num_classes = predict.shape[-1]
        top_n = min(10, num_classes)
        top_class_indices = np.argsort(mean_predict)[::-1][:top_n]
        ax[2].imshow(np.transpose(predict[:, top_class_indices]), aspect='auto', interpolation='nearest', cmap='gray_r')
        y_ticks = range(0, top_n)
        ax[2].set_yticks(y_ticks, [labels[top_class_indices[x]] for x in y_ticks])
        ax[2].set_ylim(-0.5 + np.array([top_n, 0]))
        ax[2].set_title('Class Scores')

        # Plot the probabilities
        ax[3].plot(predict[:, top_class_indices])
        ax[3].legend(np.array(labels)[top_class_indices], loc='best')
        ax[3].set_title('Class Probabilities')

    fig.suptitle(title)

    return fig


def spec_energy_plot(mixture: np.ndarray,
                     feature: np.ndarray,
                     target: Union[np.ndarray, None] = None,
                     truth_f: Union[np.ndarray, None] = None,
                     predict: Union[np.ndarray, None] = None,
                     tp_title: str = '') -> plt.figure:
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.utils import int16_to_float

    num_plots = 2
    if truth_f is not None:
        num_plots += 1
    if predict is not None:
        num_plots += 1

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the waveform
    p = 0
    x_axis = np.arange(len(mixture), dtype=np.float32) / SAMPLE_RATE
    ax[p].plot(x_axis, int16_to_float(mixture), label='Mixture', color='mistyrose')
    ax[0].set_ylabel('magnitude', color='tab:blue')
    ax[p].set_xlim(x_axis[0], x_axis[-1])
    # ax[p].set_ylim([-1.025, 1.025])
    if target is not None:  # Plot target time-domain waveform on top of mixture
        ax[0].plot(x_axis, int16_to_float(target), label='Target', color='tab:blue')
        # ax[0].tick_params(axis='y', labelcolor=color)
    ax[p].set_title('Waveform')

    # Plot the spectrogram
    p += 1
    ax[p].imshow(np.transpose(feature), aspect='auto', interpolation='nearest', origin='lower')
    ax[p].set_title('Feature')

    if truth_f is not None:
        p += 1
        ax[p].imshow(np.transpose(truth_f), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Truth ' + tp_title)

    if predict is not None:
        p += 1
        ax[p].imshow(np.transpose(predict), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Predict ' + tp_title)

    return fig


def spec3_plot(predict: np.ndarray,
               truth_f: Union[np.ndarray, None] = None,
               feature: Union[np.ndarray, None] = None,
               tp_title: str = '') -> plt.figure:
    """
    Plot up to three spectrograms:
        First is feature if provided
        2nd is prediction (must be provided)
        3rd is truth if provided
    """
    num_plots = 1
    if truth_f is not None:
        num_plots += 1
    if feature is not None:
        num_plots += 1

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # # Plot the waveform
    # p = 0
    # x_axis = np.arange(len(mixture), dtype=np.float32) / SAMPLE_RATE
    # ax[p].plot(x_axis, int16_to_float(mixture), label='Mixture')
    # ax[p].set_xlim(x_axis[0], x_axis[-1])
    # ax[p].set_ylim([-1.025, 1.025])
    # ax[p].set_title('Waveform')

    # Plot the spectrogram
    p = 0
    if feature is not None:
        ax[p].imshow(np.transpose(feature), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Feature')
        p += 1

    if num_plots == 1:  # plt will not make an array if only 1
        ax.imshow(np.transpose(predict), aspect='auto', interpolation='nearest', origin='lower')
        ax.set_title('Predict ' + tp_title)
    else:
        ax[p].imshow(np.transpose(predict), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Predict ' + tp_title)

    if truth_f is not None:
        p += 1
        ax[p].imshow(np.transpose(truth_f), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Truth ' + tp_title)

    return fig


def class_plot(mixture: np.ndarray,
               target: Union[np.ndarray, None] = None,
               truth_f: Union[np.ndarray, None] = None,
               predict: Union[np.ndarray, None] = None,
               label: str = '') -> plt.figure:
    """
    Plot mixture waveform with optional prediction and/or truth together in a single plot.
    The target waveform can optionally be provided, and prediction and truth can have multiple classes.

    Inputs:
      mixture       required, numpy array (samples, 1)
      target        optional, list of numpy arrays (samples, 1)
      truth_f       optional, numpy array (frames, 1)
      predict       optional, numpy array (frames, 1)
      label         optional, label name to use when plotting

    """
    from sonusai import SonusAIError
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.utils import int16_to_float

    if mixture.ndim != 1:
        raise SonusAIError('Too many dimensions in mixture')

    if target is not None and target.ndim != 1:
        raise SonusAIError('Too many dimensions in target')

    # Set default to 1 frame when there is no truth or predict data
    frames = 1
    if truth_f is not None and predict is not None:
        if truth_f.ndim != 1:
            raise SonusAIError('Too many dimensions in truth_f')
        t_frames = len(truth_f)

        if predict.ndim != 1:
            raise SonusAIError('Too many dimensions in predict')
        p_frames = len(predict)

        frames = min(t_frames, p_frames)
    elif truth_f is not None:
        if truth_f.ndim != 1:
            raise SonusAIError('Too many dimensions in truth_f')
        frames = len(truth_f)
    elif predict is not None:
        if predict.ndim != 1:
            raise SonusAIError('Too many dimensions in predict')
        frames = len(predict)

    samples = (len(mixture) // frames) * frames

    # x-axis in sec
    x_axis = np.arange(samples, dtype=np.float32) / SAMPLE_RATE

    fig, ax = plt.subplots(1, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the time-domain waveforms then truth/prediction on second axis
    ax.plot(x_axis, int16_to_float(mixture[0:samples]), color='mistyrose', label='Mixture')
    color = 'red'
    ax.set_xlim(x_axis[0], x_axis[-1])
    # ax.set_ylim([-1.025, 1.025])
    ax.set_ylabel(f'Amplitude', color=color)
    ax.tick_params(axis='y', labelcolor=color)

    # Plot target time-domain waveform
    if target is not None:
        ax.plot(x_axis, int16_to_float(target[0:samples]), color='blue', label='Target')

    # instantiate 2nd y-axis that shares the same x-axis
    if truth_f is not None or predict is not None:
        y_label = 'Truth/Predict'
        if truth_f is None:
            y_label = 'Predict'
        if predict is None:
            y_label = 'Truth'

        ax2 = ax.twinx()

        color = 'black'
        ax2.set_xlim(x_axis[0], x_axis[-1])
        ax2.set_ylim([-0.025, 1.025])
        ax2.set_ylabel(y_label, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        if truth_f is not None:
            ax2.plot(x_axis, expand_frames_to_samples(truth_f, samples), color='green', label='Truth')

        if predict is not None:
            ax2.plot(x_axis, expand_frames_to_samples(predict, samples), color='brown', label='Predict')

    # set only on last/bottom plot
    ax.set_xlabel('time (s)')

    fig.suptitle(label)

    return fig


def mix3_plot(mixture: np.ndarray,
              target: Union[np.ndarray, None] = None,
              wav1: Union[np.ndarray, None] = None,
              wav2: Union[np.ndarray, None] = None,
              label: str = '') -> plt.figure:
    """
    Plot mixture waveform with other waveforms (prediction, truth, etc.) together in a second plot.
    The target waveform can optionally be provided which is overlayed on top of mixture.

    Inputs:
      mixture       required, numpy array (samples, 1)
      target        optional, list of numpy arrays (samples, 1)
      wav1          optional, numpy array (frames, 1)
      wav2          optional, numpy array (frames, 1)
      label         optional, label name to use when plotting

    """
    from sonusai import SonusAIError
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.utils import int16_to_float

    if mixture.ndim != 1:
        raise SonusAIError('Too many dimensions in mixture')

    if target is not None and target.ndim != 1:
        raise SonusAIError('Too many dimensions in target')

    # Set default to 1 frame when there is no truth or wav2 data
    frames = 1
    if wav1 is not None and wav2 is not None:
        if wav1.ndim != 1:
            raise SonusAIError('Too many dimensions in wav1')
        t_frames = len(wav1)

        if wav2.ndim != 1:
            raise SonusAIError('Too many dimensions in wav2')
        p_frames = len(wav2)

        frames = min(t_frames, p_frames)
    elif wav1 is not None:
        if wav1.ndim != 1:
            raise SonusAIError('Too many dimensions in wav1')
        frames = len(wav1)
    elif wav2 is not None:
        if wav2.ndim != 1:
            raise SonusAIError('Too many dimensions in wav2')
        frames = len(wav2)

    samples = (len(mixture) // frames) * frames

    num_plots = 1
    if wav1 is not None or wav2 is not None:
        num_plots += 1

    # x-axis in sec
    x_axis = np.arange(samples, dtype=np.float32) / SAMPLE_RATE

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the mixture and optional truth waveforms
    p = 0
    ax[p].plot(x_axis, int16_to_float(mixture[0:samples]), color='mistyrose', label='Mixture')
    color = 'red'
    ax[p].set_xlim(x_axis[0], x_axis[-1])
    # ax[p].set_ylim([-1.025, 1.025])
    ax[p].set_ylabel(f'Amplitude', color=color)
    ax[p].tick_params(axis='y', labelcolor=color)

    # Plot target time-domain waveform
    if target is not None:
        ax[p].plot(x_axis, int16_to_float(target[0:samples]), color='blue', label='Target')

    # instantiate 2nd plot
    if wav1 is not None or wav2 is not None:
        p += 1
        y_label = 'wav1/wav2'
        if wav1 is None:
            y_label = 'wav2'
        if wav2 is None:
            y_label = 'wav1'

        if wav1 is not None:
            ax[p].plot(x_axis, expand_frames_to_samples(wav1, samples), color='green', label=y_label)

        if wav2 is not None:
            ax[p].plot(x_axis, expand_frames_to_samples(wav2, samples), color='brown', label=y_label)

        # ax2 = ax.twinx()
        #
        # color = 'black'
        # ax2.set_xlim(x_axis[0], x_axis[-1])
        # ax2.set_ylim([-0.025, 1.025])
        # ax2.set_ylabel(y_label, color=color)
        # ax2.tick_params(axis='y', labelcolor=color)

    # set only on last/bottom plot
    ax[p].set_xlabel('time (s)')

    fig.suptitle(label)

    return fig


def expand_frames_to_samples(x: np.ndarray, samples: int) -> np.ndarray:
    samples_per_frame = samples // len(x)
    return np.reshape(np.tile(np.expand_dims(x, 1), [1, samples_per_frame]), samples)


def get_pt_from_h5(filename: str, mixdb: MixtureDatabase, mixid: int, dataset: str):
    """
    Read 'truth_f' or 'predict' dataset for a given mixid from a .h5 file.  If a timestep
    dimension exists then reshape to remove it.

    Returns array (num_frames x num_classes) or np.empty(0) if dataset does not exist
    """
    # from sonusai.mixture import convert_mixid_to_list
    from sonusai.mixture import get_file_frame_segments
    from sonusai.mixture import get_slices
    import h5py

    try:
        with h5py.File(filename, 'r') as f:
            if dataset not in f:
                return np.empty(0)

            if f[dataset].ndim == 3:
                timesteps = f[dataset].shape[1]
                num_classes = f[dataset].shape[2]
            else:
                timesteps = 0
                num_classes = f[dataset].shape[1]

            file_frame_segments = get_file_frame_segments(mixdb, [mixid])
            if timesteps == 0:
                in_slice, out_slice = get_slices(file_frame_segments[mixid], 0)
                da = f[dataset][in_slice]
            else:
                orig_length = file_frame_segments[mixid].length
                orig_start = file_frame_segments[mixid].start
                file_frame_segments[mixid].length = int(np.ceil(file_frame_segments[mixid].length / timesteps))
                file_frame_segments[mixid].start = int(np.floor(file_frame_segments[mixid].start / timesteps))
                in_slice, out_slice = get_slices(file_frame_segments[mixid], 0)
                da = f[dataset][in_slice]
                da = np.reshape(da, (da.shape[0] * timesteps, num_classes))
                soffset = orig_start - file_frame_segments[mixid].start * timesteps
                da = da[soffset:(soffset + orig_length)]

    except Exception as e:
        return np.empty(0)

    return da


def calculate_unmapped_snr_f(mapped_snr_f: np.ndarray,
                             snr_db_mean: np.ndarray,
                             snr_db_std: np.ndarray,
                             limit_en=False,
                             upper_thr=.9999,
                             lower_thr=.0001) -> np.ndarray:
    """ Calculate unmapped SNR energy from mapped SNR per bin/class.
        Input mapped_snr_f typically frames x bins (bins = num_classes) i.e. truth_f or predict data
        limiter can be applied as min(upper_thr,mapped_snr_f) and max(lower_thr,mapped_snr_f)
        which is useful for metrics that need to avoid +/-inf.
        Note: verified as exact match inverse of calculate_map_snr_f() without thresholds
              default thresholds of .0001, .9999 are equiv to snr_f of
    """
    import scipy.special as sc

    old_err = np.seterr(divide='ignore', invalid='ignore')
    if limit_en:
        mapped_snr_f = np.maximum(np.minimum(mapped_snr_f, upper_thr), lower_thr)
    snr_db = np.double(snr_db_std) * np.sqrt(2) * sc.erfinv(2 * np.double(mapped_snr_f) - 1)
    unmapped_snr_f = 10 ** ((snr_db + np.double(snr_db_mean)) / 10)
    np.seterr(**old_err)

    return np.single(unmapped_snr_f)


def mean_square_error(ytrue: np.ndarray, ypred: np.ndarray, squared=False) -> np.ndarray:
    """ Calculate mean square error or root mean square error between ytrue, ypred.
        Typical inputs expected to be size frames x classes/bins
        returns:
          err    mean over both dimensions
          err_c  mean-over-dim0 i.e. a value per class/bin
          err_f  mean-over-dim1 i.e. a value per frame
    """
    sqerr = np.square(ytrue - ypred)
    err_c = np.mean(sqerr, axis=0)  # mean over frames for value per class
    err_f = np.mean(sqerr, axis=1)  # mean over classes for value per frame
    err = np.mean(sqerr)  # mean over all
    if not squared:
        err_c = np.sqrt(err_c)
        err_f = np.sqrt(err_f)
        err = np.sqrt(err)

    return err, err_c, err_f


def log_error(ytrue: np.ndarray, ypred: np.ndarray) -> np.ndarray:
    """ Calculate log error between ytrue, ypred which are complex or real float numpy arrays
        Typical inputs expected to be size frames x classes/bins
        returns:
          logerr    mean over both dimensions, scalar value
          logerr_c  mean-over-dim0 i.e. a value per class/bin
          logerr_f  mean-over-dim1 i.e. a value per frame
    """
    ytsq = np.real(ytrue * np.conjugate(ytrue))
    ypsq = np.real(ypred * np.conjugate(ypred))
    lgerr = abs(10 * np.log10((ytsq + np.finfo(np.float32).eps) / (ypsq + np.finfo(np.float32).eps)))
    # lgerr = abs(10*np.log10(ytsq / (ypsq + np.finfo(np.float32).eps)+np.finfo(np.float32).eps))
    logerr_c = np.mean(lgerr, axis=0)  # mean over frames for value per class
    logerr_f = np.mean(lgerr, axis=1)  # mean over classes for value per frame
    logerr = np.mean(lgerr)

    return logerr, logerr_c, logerr_f


def calculate_transform_from_audio(audio: np.ndarray, tf_gen=None) -> np.ndarray:
    from pyaaware import ForwardTransform
    from sonusai.mixture import DEFAULT_FRAME_SIZE

    if tf_gen is None:
        tf = ForwardTransform(N=DEFAULT_FRAME_SIZE * 4, R=DEFAULT_FRAME_SIZE)
    else:
        tf = tf_gen

    transform = tf.execute_all(audio)

    return transform.transpose()


def calculate_audio_from_transform(transform: np.ndarray, itf_gen=None, trim=True) -> np.ndarray:
    """
    Apply inverse transform to input transform bins x frames to generate audio samples
    Trim mode removes starting samples so output waveform will be time-aligned with
    input waveform to the transform.
    """
    from pyaaware import InverseTransform
    from sonusai.mixture import DEFAULT_FRAME_SIZE

    if itf_gen is None:
        itf = InverseTransform(N=DEFAULT_FRAME_SIZE * 4, R=DEFAULT_FRAME_SIZE)
    else:
        itf = itf_gen

    audio = itf.execute_all(transform.transpose())
    if trim:
        audio = audio[itf.N - itf.R:]

    return audio


def calculate_energy_f_from_audio(audio: np.ndarray, feature_gen) -> np.ndarray:
    """
    Calculate energy_f from time-domain audio given specified feature generator.
    """
    from sonusai.mixture import get_pad_length
    from sonusai.utils.int16_to_float import int16_to_float
    from pyaaware import ForwardTransform
    from sonusai.mixture.feature import get_feature_stats

    fs = get_feature_stats(feature_mode=feature_gen.feature_mode,
                           frame_size=feature_gen.frame_size,
                           num_classes=feature_gen.num_classes,
                           truth_mutex=feature_gen.truth_mutex)

    audio = np.pad(array=audio,
                   pad_width=(0, get_pad_length(len(audio), fs.feature_step_samples)),
                   mode='constant',
                   constant_values=0)

    target_fft = ForwardTransform(N=feature_gen.frame_size * 4, R=feature_gen.frame_size)

    frames = int(len(audio) / fs.feature_step_samples)
    bins = feature_gen.bin_end - feature_gen.bin_start + 1
    energy_f = np.zeros((frames, bins), dtype=np.single)
    idx = 0
    for offset in range(0, len(audio), feature_gen.frame_size):
        energy_f[idx, :] = np.single(
            target_fft.energy_f(int16_to_float(audio[offset:offset + feature_gen.frame_size])))
        idx += 1

    return energy_f


def calculate_energy_f_from_mixid(mixdb: MixtureDatabase, mixid: int) -> np.ndarray:
    """
    Calculate energy_f of mixid mixture waveform in mixdb (energy_f = power spectral density)
    Simply re-generate mixture and transform
    Note: only matches direct bin modes:  b**NN****, i.e. blh28bs1, bcr28bs1, ...
    """
    from sonusai.utils.int16_to_float import int16_to_float
    from pyaaware import ForwardTransform
    from sonusai.mixture.audio_db import get_mixture_data

    mixture, _, target, noise, _, _ = get_mixture_data(mixdb=mixdb, mixid=mixid)

    tf = ForwardTransform(N=mixdb.frame_size * 4, R=mixdb.frame_size)
    mix_energy_f = tf.energy_f(int16_to_float(mixture))
    noise_energy_f = tf.energy_f(int16_to_float(noise))
    target_energy_f = tf.energy_f(int16_to_float(target))

    return mix_energy_f, target_energy_f, noise_energy_f


def mmse_stsa(xi, gamma):
    """
    Computes the MMSE-STSA gain function.
    Argument/s:
      xi - a priori SNR.
      gamma - a posteriori SNR.
    Returns:
      gain - MMSE-STSA gain function.
   """
    from scipy.special import i0, i1

    old_err = np.seterr(divide='ignore', invalid='ignore', over='ignore')
    nu = np.multiply(xi, np.divide(gamma, np.add(1, xi)))
    gain = np.multiply(np.multiply(np.multiply(np.divide(np.sqrt(np.pi), 2),
                                               np.divide(np.sqrt(nu), gamma)), np.exp(np.divide(-nu, 2))),
                       np.add(np.multiply(np.add(1, nu), i0(np.divide(nu, 2))),
                              np.multiply(nu, i1(np.divide(nu, 2)))))  # MMSE-STSA gain function.
    idx = np.isnan(gain) | np.isinf(gain)  # replace by Wiener gain.
    gain[idx] = np.divide(xi[idx], np.add(1, xi[idx]))  # Wiener gain.
    np.seterr(**old_err)

    return gain


def speech_est_from_snr_f(mixture_tf,
                          snr_f,
                          min_tgain,
                          apost_snr=None,
                          gfunc='mmse_stsa') -> (np.ndarray, np.ndarray):
    """
    Compute speech estimate from transform and estimation/prediction data
    Inputs:
      mixture_tf:    mixture transform data (frames x bins complex float)
      snr_f:         a-priori snr_f prediction or truth_f data (frames x bins)
                     zero-padded in frame dimension if less than mixture_tf frames
      gfunc:         gain function type, i.e. 'mmse_stsa'
    Outputs:
      speech_est_tf: speech estimate transform data (frames x bins complex float)
      target_gain:   gain data (frames x bins)
      apost_snr      a-posteriori SNR estimated from snr_f (a-priori snr)
    """

    # TBD use gfunc type for other functions
    if apost_snr is None:
        apost_snr = np.maximum(snr_f + 1, 1e-12)  # a-posteriori snr estimate, limited to -120db
    target_gain = np.maximum(mmse_stsa(snr_f, apost_snr), min_tgain)
    speech_est_tf = mixture_tf * np.pad(target_gain, ((0, mixture_tf.shape[0] - target_gain.shape[0]), (0, 0)),
                                        'constant')

    return speech_est_tf, target_gain, apost_snr


def noise_est_from_snr_f(mixture_tf,
                         snr_f,
                         apost_snr=None) -> (np.ndarray, np.ndarray):
    """
    Compute noise estimate from transform and estimation/prediction data (snr_f)
    Inputs:
      mixture_tf:    mixture transform data (frames x bins complex float)
      snr_f:         a-priori snr_f prediction or truth_f data (frames x bins)
                     frames can be smaller than mixture_tf frames, calculated gain
                     will be zero-padded.
      apost_snr      a-posteriori SNR estimated from snr_f (a-priori snr).
                     Calculated internally if not provided
    Outputs:
      noise_est_tf:  speech estimate transform data (frames x bins complex float)
      noise_gain:    gain data (frames x bins), zero-padded in frame dimension if
                     less than mixture_tf frames
      apost_snr      a-posteriori SNR estimated from snr_f (a-priori snr)
    """

    if apost_snr is None:
        apost_snr = np.maximum(snr_f + 1, 1e-12)  # a-posteriori snr estimate, limited to -120db

    noise_gain = (1 / np.square(1 + snr_f) + snr_f / ((1 + snr_f) * apost_snr))
    noise_gain = np.pad(noise_gain, ((0, mixture_tf.shape[0] - noise_gain.shape[0]), (0, 0)), 'constant')
    noise_est_tf = mixture_tf * noise_gain

    return noise_est_tf, noise_gain, apost_snr


def calculate_pesq(speech_ref: np.ndarray, speech_est: np.ndarray, error_value=0.0):
    """
    Computes the PESQ score of speech estimate audio vs. the clean speech estimate audio.
    Upon error, assigns a value of 0, or user specified value in error_value
    Argument/s:
      speech_ref - speech reference audio, np.ndarray vector of samples.
      speech_est - speech estimated audio, np.ndarray vector of samples.
    Returns:
      score - float value between -0.5 to 4.5.
   """
    from pesq import pesq

    try:
        score = pesq(16000, speech_ref, speech_est, mode='wb')
    except Exception as e:
        logger.debug(f'PESQ error {e}')
        score = error_value

    return score


def _write_wav(name: str, data: np.ndarray) -> None:
    import wave

    from sonusai.mixture import SAMPLE_BYTES
    from sonusai.mixture import SAMPLE_RATE

    with wave.open(name, mode='w') as f:
        f.setnchannels(1)
        f.setsampwidth(SAMPLE_BYTES)
        f.setframerate(SAMPLE_RATE)
        f.writeframesraw(data)
        logger.debug(f'Wrote {name}')


def float_to_int16(x: np.ndarray) -> np.ndarray:
    """Convert float (32b or 64b) range +/1 array to int16 array to +/- 32768"""
    return np.int16(x * 32768)


def run_sonusai_hypermodel(hypermodel, model, feature):
    """ Run hypermodel prediction on non-reshaped feature data """
    from sonusai.data_generator.utils import get_frames_per_batch
    from sonusai.utils import reshape_inputs
    from sonusai.utils import reshape_outputs
    # Pad with zeros in order to create an entire batches of data
    frames = feature.shape[0]
    frames_per_batch = get_frames_per_batch(hypermodel.batch_size, hypermodel.timesteps)
    padding = frames_per_batch - feature.shape[0] % frames_per_batch
    feature = np.pad(array=feature,
                     pad_width=((0, padding), (0, 0), (0, 0)),
                     mode='constant',
                     constant_values=0)
    feature, _, _, _, _, _ = reshape_inputs(feature=feature,
                                            batch_size=hypermodel.batch_size,
                                            timesteps=hypermodel.timesteps,
                                            flatten=hypermodel.flatten,
                                            add1ch=hypermodel.add1ch)
    predict = model.predict(feature, verbose=1)
    predict, _, _ = reshape_outputs(predict=predict, timesteps=hypermodel.timesteps)
    predict = predict[:frames, :]
    return predict


def main():
    from os.path import basename
    from os.path import splitext
    from os.path import isdir
    import h5py
    from docopt import docopt
    from matplotlib.backends.backend_pdf import PdfPages
    import pandas as pd

    from pyaaware import Predict
    from pyaaware import ForwardTransform
    from pyaaware import InverseTransform
    import sonusai
    from sonusai.utils import trim_docstring
    from sonusai import SonusAIError
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    from sonusai.utils.int16_to_float import int16_to_float
    from sonusai.mixture import DEFAULT_FRAME_SIZE
    from sonusai.mixture.mixdb import get_mrecords_from_mixids
    from sonusai.mixture import convert_mixids_to_list

    from sonusai.mixture import get_mixture_data

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    pred_name = args['PFILE']
    input_name = args['MIXDB']
    model_name = args['--model']
    weights_name = args['--weights']
    mixid = args['--mixid']
    min_tgain = float(args['--min-tgain'])
    batch_size = int(args['--batch'])
    truth_est_mode = args['--tru-est-mode']
    disable_wav = args['--disable-wav-write']
    plot_en = args['--plot-enable']
    noise_est_en = args['--noise-est-enable']

    if pred_name is None:
        raise SonusAIError(f'{pred_name} not provided')

    if input_name is None:
        raise SonusAIError(f'{input_name} not provided')

    log_name = 'plot.log'
    create_file_handler(log_name)
    update_console_handler(verbose)
    initial_log_messages('plot')

    ###### Setup input file (truth)
    logger.info(f'Input:  {input_name}')
    iext = splitext(input_name)[1]
    ipath = splitext(input_name)[0]
    ibase_name = basename(splitext(input_name)[0])
    if iext == '.json':
        from sonusai.mixture.mixdb import load_mixdb
        logger.info(f'Input file is .json file, attempting to load mixdb')
        mixdb = load_mixdb(input_name)
        num_mixtures = len(mixdb.mixtures)
        # Review truth settings, use first target assuming all are the same
        settings = mixdb.targets[0].truth_settings[0]
        logger.info(f'Truth function is {settings.function} (est. from first target)')
        # Setup the transforms, TBD include in config file
        if mixdb.feature[-2] == 's':  # a hack until tf stuff is in config, if stride, assuming s1
            itf = InverseTransform(N=DEFAULT_FRAME_SIZE * 4, R=DEFAULT_FRAME_SIZE)
            tfg = ForwardTransform(N=DEFAULT_FRAME_SIZE * 4, R=DEFAULT_FRAME_SIZE, ttype='stft-olsa-hanns')
        else:  # if it is 'b' or 'd'
            itf = InverseTransform(N=256, R=128, ttype='stft-olsa-hann')
            tfg = ForwardTransform(N=256, R=128, ttype='stft-olsa-hann')

        logger.debug(f'Setup forward transform with N={tfg.N}, R={tfg.R}, ttype={tfg.ttype}')
        logger.debug(f'Setup inverse transform with N={itf.N}, R={itf.R}, ttype={itf.ttype}')
        mixid_padding = mixdb.mixid_padding  # set if mixid, else if ft subdir
        mixid = convert_mixids_to_list(mixdb, mixid)

    else:
        logger.info(f'Truth .h5 input not supported yet.')
        raise SystemExit(1)

    ##### Setup predict file
    keras_model = None
    onnx_model = None
    pext = splitext(pred_name)[1]
    pbase_name = basename(splitext(pred_name)[0])
    if isdir(pred_name):
        logger.info(f'Prediction is a subdir, assuming it contains a set of prediction .h5 files')
        # TBD
    elif pext == ".wav":
        logger.info(f'Prediction is .wav, attempting model load from:  {model_name}')
        if model_name is not None:
            mbase_name = basename(splitext(model_name)[0])
            try:
                onnx_model = Predict(model_name)
            except Exception as e:
                raise SonusAIError(f'Error loading ONNX model {model_name}, exiting. Msg: {e}')

            logger.debug(f'Model feature name {model.feature}')
            logger.debug(f'Model input shape  {model.input_shape}')
            logger.debug(f'Model output shape {model.output_shape}')
        else:
            raise SonusAIError('Must specify -m .onnx model file when prediction input is .wav')
        output_dir = '.'
    elif pext == ".h5":
        logger.info(f'Prediction file is an HDF5 file, attempting to load predict data')
        with h5py.File(pred_name, 'r') as f:
            if 'predict' in f:
                predict = np.array(f['/predict'])

        if predict.ndim > 2:  # Check if timestep dimension and reshape to remove
            predict = np.reshape(predict, (predict.shape[0] * predict.shape[1], predict.shape[2]))

        # TBD Generate predict_wav here from predict data, assumes transform invertible
        output_dir = '.'
    else:  # assume it's a Sonusai Keras .py file
        if weights_name is None:
            raise SonusAIError(f'Error: weight file not provided for {pred_name}, exiting.')
        logger.info('Attempting Sonusai Keras .py hypermodel load')
        from sonusai.utils import import_keras_model
        import keras_tuner as kt
        try:
            pymodel = import_keras_model(pred_name)
            hypermodel = pymodel.MyHyperModel()
            if hypermodel.timesteps >= 0:
                timesteps = 1
            else:
                timesteps = 0
            from sonusai.utils import check_keras_overrides
            check_keras_overrides(pymodel, mixdb.feature, mixdb.num_classes, timesteps, batch_size)
            hypermodel = pymodel.MyHyperModel(feature=mixdb.feature,
                                              num_classes=mixdb.num_classes,
                                              timesteps=timesteps,
                                              batch_size=batch_size)
            logger.info(f'Building model with batch_size {batch_size} and timesteps {hypermodel.timesteps}')
            keras_model = hypermodel.build_model(kt.HyperParameters())
            logger.info(f'Loading weights from {weights_name}')
            keras_model.load_weights(weights_name)
            # create output directory
            from datetime import datetime
            from os import mkdir
            output_dir = f'spenh-eval-{ibase_name}-{datetime.now():%Y%m%d}'
            try:
                mkdir(output_dir)
            except OSError as _:
                output_dir = f'spenh-eval-{ibase_name}-{datetime.now():%Y%m%d-%H%M%S}'
                try:
                    mkdir(output_dir)
                except OSError as error:
                    logger.error(f'Could not create directory, {output_dir}: {error}')
                    raise SystemExit(1)

        except Exception as e:
            logger.exception(f'Error: {pred_name} hypermodel load or build_model() failed, msg: {e}.')
            raise SystemExit(1)

    basepath = output_dir + '/'

    mrecords = get_mrecords_from_mixids(mixdb, mixid)
    num_mrecords = len(mrecords)
    logger.info(f'Processing {num_mrecords} mixtures ...')

    ######### Main loop for each mixid run predition, estimation, metrics
    truth_f = None
    noise_est_f = None
    for mi in range(num_mrecords):
        ti = mixdb.mixtures[mi].target_file_index[0]  # first target index only
        settings = mixdb.targets[ti].truth_settings[0]  # first truth function only
        snr_db_mean = settings.config['snr_db_mean']
        snr_db_std = settings.config['snr_db_std']

        # 1) Generate feature and mixture transform data
        mixture, class_audio, noise, feature, truth_f = get_mixture_data(mixdb, mrecords[mi])
        mixture = int16_to_float(mixture)
        mixture_tf = calculate_transform_from_audio(mixture, tf_gen=tfg)
        # Note: Todo make target, noise, and truth_f are optional
        target = int16_to_float(class_audio[0])
        noise = int16_to_float(noise)
        target_tf = calculate_transform_from_audio(target, tfg)
        noise_tf = calculate_transform_from_audio(noise, tfg)

        # 2) Run prediction
        if keras_model is not None:
            predict = run_sonusai_hypermodel(hypermodel, keras_model, feature)
        elif onnx_model is not None:
            predict = model.execute(feature)  # TBD create function reshape+predict to the onnx model batch, tstep
        # TBD add predict data file output

        # 3) Estimate speech and noise tf and .wav
        pred_snr_f = calculate_unmapped_snr_f(predict, snr_db_mean, snr_db_std,
                                              True)  # Apply default limits for unmapping and metrics
        speech_est_f, target_gain, apost_snr = speech_est_from_snr_f(mixture_tf, pred_snr_f, min_tgain,
                                                                     gfunc='mmse_stsa')
        speech_est_wav = calculate_audio_from_transform(speech_est_f, itf)
        # Todo make optional if noise enabled cli switch
        noise_est_f, noise_gain, _ = noise_est_from_snr_f(mixture_tf, pred_snr_f, apost_snr)
        noise_est_wav = calculate_audio_from_transform(noise_est_f, itf)

        # 4) Calculate speech and noise metrics (optional, if truth_f avail, and target, noise, etc.)
        if truth_f is not None:
            mixidstr = f'{mi:0{mixid_padding}}'  # mixid string for file outputs
            # SNR est accuracy: spectral distortion metric effectively the rmse of unmapped snr's in db
            truth_f_db = 10 * np.log10(truth_f + np.finfo(np.float32).eps)
            predict_db = 10 * np.log10(pred_snr_f + np.finfo(np.float32).eps)
            sd_snr, sd_snr_bin, sd_snr_frame = mean_square_error(truth_f_db, predict_db)
            # Speech PSD estimation accuracy symmetric mean log-spectral distortion (logerr):
            lerr_sp, lerr_sp_bin, lerr_sp_frame = log_error(target_tf, speech_est_f)
            # Speech intelligibility measure - PESQ
            pesq_speech = calculate_pesq(target, speech_est_wav)
            pesq_mixture = calculate_pesq(target, mixture)
            pesq_impr = pesq_speech - pesq_mixture  # pesq improvement
            pesq_impr_pc = pesq_impr / (pesq_mixture + np.finfo(np.float32).eps) * 100  # pesq improvement %
            if noise_est_f is not None:
                lerr_n, lerr_n_bin, lerr_n_frame = log_error(noise_tf, noise_est_f)

            # 5) Save per mixture metric results
            # Single row in table of scalar metrics per mixture
            mtable1_col = ['MXSNR', 'MXPESQ', 'PESQ', 'PESQi', 'PESQi%', 'SNRSD', 'SPLERR', 'NLERR', 'SPFILE', 'NFILE']
            ni = mixdb.mixtures[mi].noise_file_index
            metr1 = [mixdb.mixtures[mi].snr, pesq_mixture, pesq_speech, pesq_impr, pesq_impr_pc, sd_snr, lerr_sp,
                     lerr_n, basename(mixdb.targets[ti].name), basename(mixdb.noises[ni].name)]
            mtab1 = pd.DataFrame([metr1], columns=mtable1_col, index=[mi])
            # Stats of per frame estimation metrics
            efs_table2_col = ['Max', 'Min', 'Avg', 'Median']
            efs_table2_row = ['SNRSD', 'SPLERR', 'NLERR']
            metr2 = [[np.max(sd_snr_frame), np.min(sd_snr_frame), np.mean(sd_snr_frame), np.median(sd_snr_frame)],
                     [np.max(lerr_sp_frame), np.min(lerr_sp_frame), np.mean(lerr_sp_frame), np.median(lerr_sp_frame)],
                     [np.max(lerr_n_frame), np.min(lerr_n_frame), np.mean(lerr_n_frame), np.median(lerr_n_frame)]]
            mtab2 = pd.DataFrame(metr2, columns=efs_table2_col, index=efs_table2_row)

            mtab2flat_col = ['MXSNR', 'SNRSD Max', 'SNRSD Min', 'SNRSD Avg', 'SNRSD Median',
                             'SPLERR Max', 'SPLERR Min', 'SPLERR Avg', 'SPLERR Median',
                             'NLERR Max', 'NLERR Min', 'NLERR Avg', 'NLERR Median']
            tmp = np.insert(np.array(metr2), 0, mixdb.mixtures[mi].snr).reshape(1, 13)
            mtab2_flat = pd.DataFrame(tmp, columns=mtab2flat_col, index=[mi])
            if 'all_mtab1' in locals():  # Update all mixture table
                all_mtab1 = pd.concat([all_mtab1, mtab1])
                all_mtab2 = pd.concat([all_mtab2, mtab2_flat])
            else:  # create the table if it doesn't exist
                all_mtab1 = mtab1
                all_mtab2 = mtab2_flat

            metric_fname = basepath + mixidstr + '-spenh-metrics.txt'
            with open(metric_fname, 'w') as f:
                print('Speech enhancement metrics:', file=f)
                print(mtab1.round(2).to_string(), file=f)
                print('', file=f)
                print(f'Extraction statistics over {mixture_tf.shape[0]} frames:', file=f)
                print(mtab2.round(2).to_string(), file=f)
                print('', file=f)
                print(f'Target path: {mixdb.targets[ti].name}', file=f)
                print(f'Noise path: {mixdb.noises[ni].name}', file=f)
                # print(f'PESQ improvement: {pesq_impr:0.2f}, {pesq_impr_pc:0.1f}%', file=f)

            # 6) Estimate speech from truth to test the extraction-reconstruction methods, and calc metrics
            if truth_est_mode is True:
                truth_snr_f = calculate_unmapped_snr_f(truth_f, snr_db_mean, snr_db_std, True)
                speech_trest_f, tru_target_gain, apost_snr = \
                    speech_est_from_snr_f(mixture_tf, truth_snr_f, min_tgain, gfunc='mmse_stsa')
                speech_trest_wav = calculate_audio_from_transform(speech_trest_f, itf)
                noise_trest_f, noise_gain, _ = noise_est_from_snr_f(mixture_tf, truth_snr_f, apost_snr)
                noise_trest_wav = calculate_audio_from_transform(noise_trest_f, itf)

                # Speech PSD estimation accuracy symmetric mean log-spectral distortion (logerr):
                lerr_sptr, lerr_sptr_bin, lerr_sptr_frame = log_error(target_tf, speech_trest_f)
                # Speech intelligibility measure - PESQ
                pesq_speechtr = calculate_pesq(target, speech_trest_wav)
                pesq_impr_sptr = pesq_speechtr - pesq_mixture  # pesq improvement
                pesq_impr_pctr = pesq_impr_sptr / (pesq_mixture + np.finfo(np.float32).eps) * 100  # pesq improvement %
                lerr_ntr, lerr_ntr_bin, lerr_ntr_frame = log_error(noise_tf, noise_trest_f)

                mtable3_col = ['MXSNR', 'MXPESQ', 'PESQ', 'PESQi', 'PESQi%', 'SPLERR', 'NLERR']
                metr3 = [mixdb.mixtures[mi].snr, pesq_mixture, pesq_speechtr, pesq_impr_sptr, pesq_impr_pctr, lerr_sptr,
                         lerr_ntr]
                mtab3 = pd.DataFrame([metr3], columns=mtable3_col, index=[mi])

                # Stats of per frame estimation metrics
                efs_table4_col = ['Max', 'Min', 'Avg', 'Median']
                efs_table4_row = ['SPLERR', 'NLERR']
                metr4 = [[np.max(lerr_sptr_frame), np.min(lerr_sptr_frame), np.mean(lerr_sptr_frame),
                          np.median(lerr_sptr_frame)],
                         [np.max(lerr_ntr_frame), np.min(lerr_ntr_frame), np.mean(lerr_ntr_frame),
                          np.median(lerr_ntr_frame)]]
                mtab4 = pd.DataFrame(metr4, columns=efs_table4_col, index=efs_table4_row)

                # Append extraction metrics to metrics file:
                with open(metric_fname, 'a') as f:
                    print('', file=f)
                    print('Speech enhancement metrics of extraction method using truth:', file=f)
                    print(mtab3.round(2).to_string(), file=f)
                    print('', file=f)
                    print('Truth extraction statistics over frames:', file=f)
                    print(mtab4.round(2).to_string(), file=f)

                # Append to all mixture table
                mtab4flat_col = ['MXSNR', 'SPLERR Max', 'SPLERR Min', 'SPLERR Avg', 'SPLERR Median',
                                 'NLERR Max', 'NLERR Min', 'NLERR Avg', 'NLERR Median']
                tmp = np.insert(np.array(metr4), 0, mixdb.mixtures[mi].snr).reshape(1, 9)  # Insert MXSNR
                mtab4_flat = pd.DataFrame(tmp, columns=mtab4flat_col, index=[mi])
                if 'all_mtab3' in locals():  # Update all mixture table
                    all_mtab3 = pd.concat([all_mtab3, mtab3])
                    all_mtab4 = pd.concat([all_mtab4, mtab4_flat])
                else:  # create the table if it doesn't exist
                    all_mtab3 = mtab3
                    all_mtab4 = mtab4_flat

        # 7) write wav files
        if disable_wav is False:
            _write_wav(name=basepath + mixidstr + '-mixture.wav', data=float_to_int16(mixture))
            _write_wav(name=basepath + mixidstr + '-speech_est.wav', data=float_to_int16(speech_est_wav))
            if noise_est_f is not None:
                _write_wav(name=basepath + mixidstr + '-noise_est.wav', data=float_to_int16(noise_est_wav))
            if truth_f is not None:
                _write_wav(name=basepath + mixidstr + '-target.wav', data=float_to_int16(target))
                _write_wav(name=basepath + mixidstr + '-noise.wav', data=float_to_int16(noise))
                if truth_est_mode is True:
                    _write_wav(name=basepath + mixidstr + '-speech_trest.wav', data=float_to_int16(speech_trest_wav))
                    _write_wav(name=basepath + mixidstr + '-noise_trest.wav', data=float_to_int16(noise_trest_wav))

        # 8) Write out plot file
        if plot_en is True:
            plot_fname = basepath + mixidstr + '-spenh-plots.pdf'

            # Original size (frames, stride, num_bands)
            # Decimate in the stride dimension
            # Reshape to get frames*decimated_stride, num_bands
            if feature is not None:
                if feature.ndim != 3:
                    raise SonusAIError(f'feature does not have 3 dimensions: frames, stride, num_bands')
                spectrogram = feature[:, -step:, :]
                spectrogram = np.reshape(spectrogram,
                                         (spectrogram.shape[0] * spectrogram.shape[1], spectrogram.shape[2]))
            else:
                spectrogram = None

            with PdfPages(pdf_name) as pdf:
                if mixture is None:
                    pdf.savefig(spec3_plot(predict=10 * np.log10(predict + np.finfo(np.float32).eps),
                                           truth_f=10 * np.log10(truth_f + np.finfo(np.float32).eps),
                                           feature=spectrogram,
                                           tp_title=tfunc_name))
                else:
                    pdf.savefig(spec_energy_plot(mixture=mixture,
                                                 target=target,
                                                 feature=spectrogram,
                                                 truth_f=10 * np.log10(truth_f + np.finfo(np.float32).eps),
                                                 predict=10 * np.log10(predict + np.finfo(np.float32).eps),
                                                 tp_title=tfunc_name))

                    if target_tf is not None:
                        tg_spec = 10 * np.log10(abs2(target_tf) + np.finfo(np.float32).eps)
                        tg_est_spec = 10 * np.log10(abs2(target_est) + np.finfo(np.float32).eps)
                        # n_spec = np.reshape(n_spec,(n_spec.shape[0] * n_spec.shape[1], n_spec.shape[2]))
                        pdf.savefig(spec3_plot(predict=tg_est_spec,  # tbd change to tg_est when avail
                                               truth_f=tg_spec,
                                               feature=spectrogram,
                                               tp_title='target energy_f'))

                    if snr_sd is not None:
                        n_spec = 10 * np.log10(abs2(noise_tf) + np.finfo(np.float32).eps)
                        n_est_spec = 10 * np.log10(abs2(noise_est) + np.finfo(np.float32).eps)
                        pdf.savefig(spec3_plot(predict=n_est_spec,
                                               truth_f=n_spec,
                                               feature=spectrogram,
                                               tp_title='noise energy_f'))

                        pdf.savefig(mix3_plot(mixture=noise_wav_est * 32768,
                                              target=noise,
                                              wav1=snr_sd_frame,
                                              wav2=None,
                                              label='Noise est'))

                        pdf.savefig(mix3_plot(mixture=target_wav_est * 32768,
                                              target=target,
                                              wav1=snr_sd_frame,
                                              wav2=None,
                                              label='Target est'))

            logger.info(f'Wrote plots to {pdf_name}')

    # 9) Done with mixtures, write out summary metrics
    # Calculate SNR summary for
    all_mtab1_sorted = all_mtab1.sort_values(by=['MXSNR', 'SPFILE'])
    all_mtab2_sorted = all_mtab2.sort_values(by=['MXSNR'])
    mtab_snr_summary = all_mtab1_sorted.query('MXSNR==' + str(mixdb.snrs[0])).mean(numeric_only=True).to_frame().T
    mtab_snr_summary_em = all_mtab2_sorted.query('MXSNR==' + str(mixdb.snrs[0])).mean(numeric_only=True).to_frame().T
    for snri in range(1, len(mixdb.snrs)):
        mtab_snr_summary = pd.concat([mtab_snr_summary,
                                      all_mtab1_sorted.query('MXSNR==' + str(mixdb.snrs[snri])).mean(
                                          numeric_only=True).to_frame().T])
        mtab_snr_summary_em = pd.concat([mtab_snr_summary_em,
                                         all_mtab2_sorted.query('MXSNR==' + str(mixdb.snrs[snri])).mean(
                                             numeric_only=True).to_frame().T])

    if truth_est_mode is True:
        all_mtab3_sorted = all_mtab3.sort_values(by=['MXSNR'])
        all_mtab4_sorted = all_mtab4.sort_values(by=['MXSNR'])
        mtab_snr_summary_tr = all_mtab1_sorted.query('MXSNR==' + str(mixdb.snrs[0])).mean(
            numeric_only=True).to_frame().T
        mtab_snr_summary_emtr = all_mtab2_sorted.query('MXSNR==' + str(mixdb.snrs[0])).mean(
            numeric_only=True).to_frame().T
        for snri in range(1, len(mixdb.snrs)):
            mtab_snr_summary_tr = pd.concat([mtab_snr_summary_tr,
                                             all_mtab3_sorted.query('MXSNR==' + str(mixdb.snrs[snri])).mean(
                                                 numeric_only=True).to_frame().T])
            mtab_snr_summary_emtr = pd.concat([mtab_snr_summary_emtr,
                                               all_mtab4_sorted.query('MXSNR==' + str(mixdb.snrs[snri])).mean(
                                                   numeric_only=True).to_frame().T])

    if num_mrecords > 1:
        metric_summary_fname = basepath + 'spenh-metrics-summary.txt'
        with open(metric_summary_fname, 'w') as f:
            print(f'Speech enhancement metrics avg over each SNR:', file=f)
            print(mtab_snr_summary.round(2).to_string(), file=f)
            print('', file=f)
            print(f'Extraction statistics stats avg over each SNR:', file=f)
            print(mtab_snr_summary_em.round(2).to_string(), file=f)
            print('', file=f)

            print(f'Speech enhancement metrics stats over all {num_mrecords} mixtures:', file=f)
            print(all_mtab1.describe().round(2).to_string(), file=f)
            print('', file=f)
            print(f'Extraction statistics stats over all {num_mrecords} mixtures:', file=f)
            print(all_mtab2.describe().round(2).to_string(), file=f)
            print('', file=f)

            if truth_est_mode is True:
                print(f'Truth-based speech enhancement metrics avg over each SNR:', file=f)
                print(mtab_snr_summary_tr.round(2).to_string(), file=f)
                print('', file=f)
                print(f'Truth-based extraction statistics stats avg over each SNR:', file=f)
                print(mtab_snr_summary_emtr.round(2).to_string(), file=f)
                print('', file=f)

                print(f'Truth-based speech enhancement metrics stats over all {num_mrecords} mixtures:', file=f)
                print(all_mtab3.describe().round(2).to_string(), file=f)
                print('', file=f)
                print(f'Truth-based extraction statistic stats over all {num_mrecords} mixtures:', file=f)
                print(all_mtab4.describe().round(2).to_string(), file=f)
                print('', file=f)

            print('Speech enhancement metrics all-mixtures list:', file=f)
            print(all_mtab1.round(2).to_string(), file=f)
            print('', file=f)
            print('Extraction statistics all-mixtures list:', file=f)
            print(all_mtab2.round(2).to_string(), file=f)

            # Write summary to .csv file
            metric_summary_csvfname = basepath + 'spenh-metrics-summary.csv'
            pd.DataFrame([f'Speech enhancement metrics stats over {num_mrecords} mixtures:']).to_csv \
                (metric_summary_csvfname, mode='a', encoding='utf-8', index=False, header=False)
            all_mtab1.describe().round(2).to_csv(metric_summary_csvfname, encoding='utf-8')
            pd.DataFrame(['']).to_csv(metric_summary_csvfname, mode='a', encoding='utf-8', index=False, header=False)

            pd.DataFrame([f'Extraction statistics stats over {num_mrecords} mixtures:']).to_csv \
                (metric_summary_csvfname, mode='a', encoding='utf-8', index=False, header=False)
            all_mtab2.describe().round(2).to_csv(metric_summary_csvfname, mode='a', encoding='utf-8')
            pd.DataFrame(['']).to_csv(metric_summary_csvfname, mode='a', encoding='utf-8', index=False, header=False)

            pd.DataFrame(['Speech enhancement metrics of extraction method using truth, stats:']).to_csv \
                (metric_summary_csvfname, mode='a', encoding='utf-8', index=False, header=False)
            all_mtab3.describe().round(2).to_csv(metric_summary_csvfname, mode='a', encoding='utf-8')
            pd.DataFrame(['']).to_csv(metric_summary_csvfname, mode='a', encoding='utf-8', index=False, header=False)

            pd.DataFrame(['Truth extraction statistics stats:']).to_csv \
                (metric_summary_csvfname, mode='a', encoding='utf-8', index=False, header=False)
            all_mtab4.describe().round(2).to_csv(metric_summary_csvfname, mode='a', encoding='utf-8')
            pd.DataFrame(['']).to_csv(metric_summary_csvfname, mode='a', encoding='utf-8', index=False, header=False)

            metric_spenhcsv_fname = basepath + 'spenh-metrics-lst.csv'
            pd.DataFrame(['Speech enhancement metrics list:']).to_csv \
                (metric_spenhcsv_fname, mode='a', encoding='utf-8', index=False, header=False)
            all_mtab1.round(2).to_csv(metric_spenhcsv_fname, mode='a', encoding='utf-8')

            metric_estatcsv_fname = basepath + 'spenh-metrics-estats-lst.csv'
            pd.DataFrame(['Extraction statistics list:']).to_csv \
                (metric_estatcsv_fname, mode='a', encoding='utf-8', index=False, header=False)
            all_mtab2.round(2).to_csv(metric_estatcsv_fname, mode='a', encoding='utf-8')

            if truth_est_mode is True:
                metric_spenhcsv_fname = basepath + 'spenh-metrics-tru-lst.csv'
                pd.DataFrame(['Speech enhancement metrics list:']).to_csv \
                    (metric_spenhcsv_fname, mode='a', encoding='utf-8', index=False, header=False)
                all_mtab3.round(2).to_csv(metric_spenhcsv_fname, mode='a', encoding='utf-8')

                metric_estatcsv_fname = basepath + 'spenh-metrics-estats-tru-lst.csv'
                pd.DataFrame(['Extraction statistics list:']).to_csv \
                    (metric_estatcsv_fname, mode='a', encoding='utf-8', index=False, header=False)
                all_mtab4.round(2).to_csv(metric_estatcsv_fname, mode='a', encoding='utf-8')

    # if output_name:
    #     with h5py.File(name=output_name, mode='w') as f:
    #         f.create_dataset(name='predict', data=predict)
    #         logger.info(f'Wrote predict data to {output_name}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)

    # mixdb = None
    # mixture = None
    # target = None
    # truth_f = None
    # feature = None
    #
    # target_tf = None
    # noise_tf = None
    # t_indices = None
    # noise_est = None
    #
    # # Prediction input processing for outputs to predict, pext, model, and predict_wav
    #
    # predict = None
    # model = None
    # mixture_tf = None
    # predict_wav = None

    # step = int(mixdb.feature_samples / mixdb.feature_step_samples)
    # if isdir(ipath):
    #     # generate mixture data
    #     from sonusai.mixture.mixdb import get_mrecords_from_mixids
    #     mrecords = get_mrecords_from_mixids(mixdb, mixid)
    #     mixture, class_audio, noise, feature, truth_f = get_mixture_data(mixdb, mrecords[0])
    #     target = class_audio[0]
    #     mixture_tf = calculate_transform_from_audio(int16_to_float(mixture))
    #     noise_tf = calculate_transform_from_audio(int16_to_float(noise))
    #     target_tf = calculate_transform_from_audio(int16_to_float(target))
    # else:
    #     logger.info(f'Error: skipping truth_f load, .json has no corresponding feature+truth subdirectory')
    #
    #
    #
    # predict_wav = read_audio(pred_name)
    # predict_tf = calculate_transform_from_audio(int16_to_float(predict_wav))
    # predict_feature = get_feature_from_audio(audio=predict_wav, model=model)
    # fs = get_feature_stats(feature_mode=model.feature,
    #                        frame_size=DEFAULT_FRAME_SIZE,
    #                        num_classes=model.output_shape[-1],
    #                        truth_mutex=model.mutex)
    # step = fs.step
    # logger.info(f'Running prediction on .wav audio samples {len(mixture)}')
    # logger.debug(f'Feature data shape {feature.shape}')
    #
    # # if feature.shape[0] < model.input_shape[0]:
    # #     raise SonusAIError(f'Model has batch size {model.input_shape[0]} which is'
    # #                        f'larger than .wav frames of {feature.shape[0]} \n'
    # #                        f'Consider using a model with a smaller batch size or'
    # #                        f' a mixture with more data.')
    # predict = model.execute(predict_feature)
    # if predict.ndim > 2:  # Check if timestep dimension and reshape to remove
    #     predict = np.reshape(predict, (predict.shape[0] * predict.shape[1], predict.shape[2]))

    #         logger.info(f'Assuming input file is an HDF5 file, attempting to load feature and truth_f data')
    #         try:
    #             with h5py.File(input_name, 'r') as f:
    #                         truth_f = np.array(f['/truth_f'])
    #                         feature = np.array(f['/feature'])
    #         except Exception as e:
    #             logger.info(f'Error loading truth_f from {input_name}, skipping. Msg: {e}')
    #
    #     if feature.ndim > 2:  # Check if timestep dimension and reshape to remove
    #         feature = np.reshape(feature, (feature.shape[0] * feature.shape[1], feature.shape[2]))
    #
    # if mixture_tf is None and feature is not None:
    #     mixture_tf = int16_to_float(feature)  # No !!, need full transform

    # predict = None
    # labels = None
    # indices = list()
    # if pext is not None and pext == '.h5':
    #     logger.info(f'Reading predict data for mixture {mixid} from {pred_name}')
    #     if mixdb is not None:
    #         predict = get_pt_from_h5(pred_name, mixdb, mixid, 'predict')
    #     else:
    #         with h5py.File(input_name, 'r') as f:
    #             if 'predict' in f:
    #                 predict = f['predict']

    # base_name = basename(splitext(pred_name)[0])
    # logger.info(f'Prediction input is an .wav file, attempting to load model')
    #
    # if ext == '.wav':
    #     if pred_name is None or pext != "onnx":
    #         raise SonusAIError('Must specify MODEL when input is WAV')
    #
    # elif ext == '.h5':   #['.json', '.h5']:
    #     if mixid is None:
    #         raise SonusAIError('Must specify MIXID when input is H5')
    #
    #     from sonusai.mixture import mixdb_from_json
    #     with h5py.File(input_name, 'r') as f:
    #         if 'mixdb' in f.attrs:
    #             mixdb = mixdb_from_json(f.attrs['mixdb'])
    #             print_mixture_details(mixdb=mixdb, mixid=mixid, desc_len=24, print_fn=logger.info,
    #                               all_class_counts=False)
    #             # TBD: Exit if truth_function is NOT an *_f
    #             #ti = mixdb.mixtures[mixid]  #target index
    #             logger.info(f'Reading truth for mixture {mixid}')
    #             truth_f = get_pt_from_h5(input_name,mixdb,mixid,'truth_f')
    #             if 'feature' in f:
    #                 print('tbd')
    #
    # if ext == '.json' or mixdb is not None:
    #     if mixid is None:
    #         raise SonusAIError('Must specify MIXID when input is JSON')
    #
    #     if mixdb is None:
    #         mixdb = load_mixdb(input_name)
    #     #print_mixture_details(mixdb=mixdb, mixid=mixid, desc_len=24, print_fn=logger.info)
    #     fs = get_feature_stats(feature_mode=mixdb.feature,
    #                            frame_size=DEFAULT_FRAME_SIZE,
    #                            num_classes=mixdb.num_classes,
    #                            truth_mutex=mixdb.truth_mutex)
    #
    #     logger.info(f'Generating data for mixture {mixid}')
    #     try:
    #         md = get_mixture_data(mixdb=mixdb, mixid=mixid)
    #         mixture = md.mixture
    #         target = md.target[0]   # Only first target
    #         noise = md.noise
    #         feature = md.feature
    #         truth_f = md.truth_f
    #
    #         step = fs.step
    #         t_indices = [x - 1 for x in get_truth_indices_for_mixid(mixdb=mixdb, mixid=mixid)]
    #
    #         targets = [mixdb.targets[tfi] for tfi in mixdb.mixtures[mixid].target_file_index]
    #         truth_functions = list(set([sub2.function for sub1 in targets for sub2 in sub1.truth_settings]))
    #         energy = 'energy_f' in truth_functions or 'snr_f' in truth_functions
    #
    #         logger.debug(f'Audio samples      {len(mixture)}')
    #         logger.debug(f'Targets:')
    #         mixture_record = mixdb.mixtures[mixid]
    #         for n in range(len(mixture_record.target_file_index)):
    #             name = mixdb.targets[mixture_record.target_file_index[n]].name
    #             duration = mixdb.targets[mixture_record.target_file_index[n]].duration
    #             augmentation = mixdb.target_augmentations[mixture_record.target_augmentation_index[n]]
    #             logger.debug(f'  Name             {name}')
    #             logger.debug(f'  Duration         {duration}')
    #             logger.debug(f'  Augmentation     {augmentation}')
    #
    #         logger.debug(f'Feature shape      {feature.shape}')
    #         logger.debug(f'Truth shape        {truth_f.shape}')
    #
    #         # Also calc energy_f (psd) of target, mixture, and noise
    #         from sonusai.utils.int16_to_float import int16_to_float
    #         mixture_tf = calculate_transform_from_audio(int16_to_float(mixture))
    #         noise_tf = calculate_transform_from_audio(int16_to_float(noise))
    #         target_tf = calculate_transform_from_audio(int16_to_float(target))
    #
    #     except Exception as e:
    #         logger.info(f'Error generating mixture, skipping. Msg: {e}')
    #
    # else:
    #     raise SonusAIError(f'Unknown file type for {input_name}')

    # # Check truth function and unmap if mapped_snr_f and requested
    # snr_sd = None
    # noise_est = None
    # if mixdb is not None:   # if we have mixture data and can check truth function
    #     ti = mixdb.mixtures[mixid].target_file_index[0]  # first target index only
    #     truth_function = mixdb.targets[ti].truth_settings[0].function  # first truth setting only
    #     tfunc_name = truth_function
    #     if unmap_snr:
    #         if truth_function == 'mapped_snr_f':
    #             snr_db_mean = mixdb.targets[ti].truth_settings[0].config['snr_db_mean']
    #             snr_db_std = mixdb.targets[ti].truth_settings[0].config['snr_db_std']
    #             if truth_f is not None:
    #                 truth_f_mapped = truth_f
    #                 truth_f = calculate_unmapped_snr_f(truth_f,snr_db_mean,snr_db_std,True)
    #             if predict is not None:
    #                 predict_mapped = predict
    #                 predict = calculate_unmapped_snr_f(predict,snr_db_mean,snr_db_std,True)
    #             tfunc_name = 'snr_f (db)'
    #
    #     if mixture is not None:
    #         _write_wav(name=f'{pbase_name}_mixture_{mixid}.wav', data=mixture)
    #         if truth_function == 'mapped_snr_f' or truth_function == 'snr_f':
    #             if predict is not None:
    #                 # Use this helper function in the future:
    #                 #    truth, predict, num_classes = reshape_truth_predict(truth, predict, timesteps)
    #                 # calculate noise reduction from estimated snr_f (a-priori snr)
    #                 apost_snr = np.maximum(predict + 1, 0)  # a-posteriori snr from estimated a-priori snr
    #                 noise_gain = (1/np.square(1+predict) + predict/((1+predict)*apost_snr))
    #                 noise_gain = np.pad(noise_gain,((0,mixture_tf.shape[0] - noise_gain.shape[0]),(0,0)), 'constant')
    #                 noise_est = mixture_tf * noise_gain
    #                 noise_wav_est = calculate_audio_from_transform(noise_est)
    #                 #_write_wav(name=f'{base_name}_noise_{mixid}.wav', data=noise_wav)
    #                 _write_wav(name=f'{pbase_name}_noiseh_{mixid}.wav', data=float_to_int16(noise_wav_est))
    #                 _write_wav(name=f'{pbase_name}_noise_{mixid}.wav', data=noise)
    #
    #                 target_gain = np.maximum(mmse_stsa(predict, apost_snr),min_tgain)
    #                 target_est = mixture_tf * np.pad(target_gain,((0,mixture_tf.shape[0] - target_gain.shape[0]),(0,0)),'constant')
    #                 target_wav_est = calculate_audio_from_transform(target_est)
    #                 _write_wav(name=f'{pbase_name}_target_{mixid}.wav', data=target)
    #                 _write_wav(name=f'{pbase_name}_targeth_{mixid}.wav', data=float_to_int16(target_wav_est))
    #
    #                 target_pesq = calculate_pesq(target, target_wav_est)
    #                 mixture_pesq = calculate_pesq(target, mixture)
    #                 pesq_impr = target_pesq - mixture_pesq  # pesq improvement
    #                 pesq_impr_pc = pesq_impr / (mixture_pesq + np.finfo(np.float32).eps) * 100  # pesq improvement %
    #                 logger.info(f'PESQ score noisy mixture, target estimate: {mixture_pesq:.3}, '
    #                             f'{target_pesq:.3}, improvement: {pesq_impr:.3}, {pesq_impr_pc:.3}%')
    #
    #                 if truth_f is not None:
    #                     # SNR est accuracy: spectral distortion metric effectively the rmse of unmapped snr's in db
    #                     truth_f_db = 10 * np.log10(truth_f + np.finfo(np.float32).eps)
    #                     predict_db = 10 * np.log10(predict + np.finfo(np.float32).eps)
    #                     # Spectral distortion metric effectively rmse of db values (per frame, and per bin)
    #                     snr_sd, snr_sd_bin, snr_sd_frame = mean_square_error(truth_f_db,predict_db)
    #                     logger.info(f'snr_sd_bin: {snr_sd:.3} dB')
    #                     # Noise PSD estimation accuracy - symmetric mean log-spectral distortion (logerr):
    #                     if noise_est is not None:
    #                         n_logerr, n_logerr_bin, n_logerr_frame = log_error(noise_tf,noise_est)
    #                         logger.info(f'noise_logerr: {n_logerr:.3} dB')

    # # Add truth indices for target (if needed)
    # if t_indices is not None:
    #     for t_index in t_indices:
    #         if t_index not in indices:
    #             indices.append(t_index)

    # labels = get_label_names(num_labels=predict.shape[1], file=labels_name)
    #
    # # Report the highest-scoring classes and their scores.
    # p_max = np.max(predict, axis=0)
    # p_indices = np.argsort(p_max)[::-1][:5]
    # p_max_len = max([len(labels[i]) for i in p_indices])
    #
    # logger.info('Top 5 active prediction classes by max:')
    # for p_index in p_indices:
    #     logger.info(f'  {labels[p_index]:{p_max_len}s} {p_max[p_index]:.3f}')
    # logger.info('')
    #
    # indices = list(p_indices)

    # if mixdb is not None:
    #     title = f'{input_name} Mixture {mixid}'
    #     pdf_name = f'{pbase_name}-{ibase_name}-plot.pdf'
    # else:
    #     title = f'{input_name}'
    #     pdf_name = f'{pbase_name}-plot.pdf'

    # for index in indices:
    #     if energy:
    #         t_tmp = None
    #         if truth_f is not None:
    #             t_tmp = 10*np.log10(truth_f + np.finfo(np.float32).eps)
    #
    #         p_tmp = None
    #         if predict is not None:
    #             p_tmp = 10*np.log10(predict + np.finfo(np.float32).eps)
    #
    #         pdf.savefig(spec_energy_plot(mixture=mixture,
    #                                      feature=spectrogram,
    #                                      truth_f=t_tmp,
    #                                      predict=p_tmp))
    #     else:
    #         p_tmp = None
    #         if predict is not None:
    #             p_tmp = predict[:, index]
    #
    #         l_tmp = None
    #         if labels is not None:
    #             l_tmp = labels[index]
    #
    #         pdf.savefig(class_plot(mixture=mixture,
    #                                target=target[index],
    #                                truth_f=truth_f[:, index],
    #                                predict=p_tmp,
    #                                label=l_tmp))

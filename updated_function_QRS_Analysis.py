import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class ECG:
    def __init__(self, threshold_factor=0.65):
        self.threshold_factor = threshold_factor

    def peakfinder(self, derivative_arr):
        peaks = []
        i = 0
        while i < len(derivative_arr):
            current_max = derivative_arr[i]
            max_index = i
            maxm = False
            i += 1
            while i < len(derivative_arr) and derivative_arr[i] >= self.threshold_factor:
                maxm = True
                if derivative_arr[i] > current_max:
                    current_max = derivative_arr[i]
                    max_index = i
                i += 1
            if maxm:
                peaks.append(max_index)
                i += 1
        return peaks

    def peaks_deriv_to_orig(self, derivative_arr, peaks):
        R_peaks = []
        for peak in peaks:
            m = peak
            while derivative_arr[m] >= 0:
                m -= 1
            R_peaks.append(m)
        return R_peaks

    def heartbeat_calc(self, R_peaks):
        time = np.diff(R_peaks) * 2
        heartbeat = 60000 / time
        return heartbeat

    def Q_peaks_calc(self, orig_arr, R_peaks):
        Q_peaks = []
        for peak in R_peaks[1:-1]:  # Excluding first and last waveforms
            LB = peak - 40
            minimum = min(orig_arr[LB:peak])
            min_index = np.where(orig_arr == minimum)[0][0]
            Q_peaks.append(min_index)
        return Q_peaks

    def S_peaks_calc(self, orig_arr, R_peaks):
        S_peaks = []
        for peak in R_peaks[1:-1]:  # Excluding first and last waveforms
            UB = peak + 40
            maximum = max(orig_arr[peak:UB])
            max_index = np.where(orig_arr == maximum)[0][0]
            S_peaks.append(max_index)
        return S_peaks

    def calcQRS(self, Q_peaks, S_peaks):
        sampling_freq = 1
        x1 = 2.5
        TQRS = []
        for q_peak, s_peak in zip(Q_peaks, S_peaks):
            TQRS.append(2 * ((s_peak + x1) - (q_peak - x1)) / sampling_freq)
        return TQRS

if __name__ == "__main__":
    colnames = ['Time', 'Lead2']
    ds1 = pd.read_csv('9.csv', names=colnames, header=None)
    x = ds1.iloc[75000:80000, 1]

    ecg_processor = ECG()

    # Convert dataframes to arrays
    orig_arr = np.array(x)
    derivative_arr = np.diff(orig_arr)

    # Find peaks in the derivative array
    peaks = ecg_processor.peakfinder(derivative_arr)

    # Convert derivative peaks to original peaks
    R_peaks = ecg_processor.peaks_deriv_to_orig(derivative_arr, peaks)

    # Calculate heartbeats
    heartbeat = ecg_processor.heartbeat_calc(R_peaks)

    # Plot the heartbeat
    plt.plot(heartbeat)
    plt.show()

    # Calculate QRS complex
    Q_peaks = ecg_processor.Q_peaks_calc(orig_arr, R_peaks)
    S_peaks = ecg_processor.S_peaks_calc(orig_arr, R_peaks)
    TQRS = ecg_processor.calcQRS(Q_peaks, S_peaks)

    # Print QRS complex statistics
    print("Average QRS: {}".format(np.mean(TQRS)))
    print("Min QRS: {}".format(np.min(TQRS)))
    print("Max QRS: {}".format(np.max(TQRS)))

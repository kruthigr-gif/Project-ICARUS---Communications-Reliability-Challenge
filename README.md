Project ICARUS - Communications Reliability Challenge


Approach: algorithms and methods implemented
Digital Modulation and Demodulation (BPSK):
At the receiver side, demodulation consists of correlation with the carrier wave followed by threshold detection to recover the original bitstream. Digital signal processing algorithms to correct phase and frequency offsets caused by Doppler spread or oscillator inaccuracies.  Matched filtering, energy-based timing recovery, hard-decision threshold detection, FFT-based frequency offset estimation, and frequency correction were implemented.
Noise modeling and SNR calibration:
The SNR can be affected by several factors such as frequency, time of measurement, and intensity of the noise source. Statistical modeling of SNR allows to predict the deterioration of the signal due to noise exposure.
Error correction coding and decoding:
Typical error control schemes used for continuous transmission include convolution codes. Most of the satellite systems use concatenated encoder/decoder schemes. The code implements  Reed-Solomon decoding using an external library.
Synchronization and Doppler compensation:
The frequency offset estimation and correction techniques are vital for maintaining signal integrity and receiver synchronization. Typical methods include FFT-based frequency offset estimation and frequency correction by multiplying received signal samples with a complex exponential.


Engineering problem-solving:
Engineering problem solving involves a systematic approach to identifying, analyzing, and resolving problems within technical contexts. The process typically includes the stages of problem definition, data collection and analysis, development and testing of solutions, and refinement for optimal performance.

Challenges: major difficulties encountered and how they were addressed
Signal suffers from the Doppler shift, due to the relative motion between the satellite and the terminal. Being able to characterize the Doppler effect with the visible time of the satellite has allowed to resolve the problem of the Doppler shift. A FFT-based peak search has been used.
The significant delay which renders retransmission schemes inefficient; thus, efficient Forward Error Correction (FEC) coding is essential to maintain reliable communication. Concatenated coding schemes such as Reed-Solomon as outer codes combined with convolutional codes as inner are used to address the error.
Datasets can have inconsistent, missing keys, or different file names. To handle these it is important for automated processing.
Couldn’t use matplot for the graphs hence  implemented a text-based ASCII graph visualization method.
Implementation Notes: details of design decisions, assumptions, and Limitations .
Details of design decisions-
Implementation of Digital Modulation and Demodulation (BPSK)-
Matched filtering with a rectangular pulse and hard threshold detection for bit decisions. Timing recovery is done by energy maximization.
Accurate Noise Modeling and SNR Calibration:
Use of  dataset metadata for SNR values and AWGN noise implicitly is present in data.
Error Correction Coding and Decoding:
Reed-Solomon decoding , convolutional (Viterbi) decoder and selective decoder invocations by applying only the necessary modules.
Synchronization and Doppler Compensation:
Estimated frequency offset through FFT peak detection. Corrected Doppler shifts by multiplying received samples.
Assumptions-
Constant channel per Dataset Folder.
Reply on the meta.json files to give you correct information.
The decoder uses hard decisions) instead of computing probabilities.
Limitations-
Incomplete Convolutional Decode
No Carrier Phase Tracking
Limited Noise Modeling
Simplistic Timing Recovery
No Hardware or Real-Time Processing Integration
Graphs-
BER vs SNR curves for uncoded vs coded systems.
Constellation diagrams at representative SNRs.
Doppler effect compensation plots (before/after correction).



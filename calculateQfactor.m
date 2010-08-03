% This script calculates the Q factor based on a given probe PRN file
function [wc, delta_wc, Q] = calculateQfactor(probe_number)

%read file

%plot in time domain

%plot in frequency domain

%Eit
[hdr,fftdata] = hdrload('fft_Ex_p03a.prn');
plot(fftdata(:,2),fftdata(:,4))


probe_fft(1,'a',3,2);
probe_fft(2,'a',2,2);  
probe_fft(2,'a',2,3);

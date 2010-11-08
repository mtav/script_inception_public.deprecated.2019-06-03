function [fft_out,lambda,freq] = cFFT(datain,dt,NFFT)
	% function [fft_out,lambda,freq] = cFFT(datain,dt,NFFT)
	% datain = datain value in time domain
	% dt = timestep in time domain
	% NFFT = double the number of points you want in the output
	% fft_out = magnitude 
	% freq = frequency
	% lambda = wavelength = c0/freq

	Lin=length(datain);

	if exist('NFFT','var')==0
		disp('NFFT not given');
		NFFT = 2^nextpow2(Lin); % Next power of 2 from length of datain
	end

	fft_out = fft(datain,NFFT);

    Lout = length(fft_out);
	fft_out = fft_out(1:Lout/2);

    %relative frequency according to nyquist criterion
    nyqfreq = 1/dt;

	% freq = nyqfreq/2*linspace(0,1,length(fft_out));
    freq = nyqfreq/Lout*linspace(1,Lout/2,length(fft_out));

	%wavelength from FDTD frequency units
    lambda = get_c0()./freq;

	% make sure all vectors are column vectors
	fft_out = fft_out(:);
	lambda = lambda(:);
	freq = freq(:);

end

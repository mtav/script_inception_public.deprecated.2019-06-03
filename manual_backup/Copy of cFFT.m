function [Y,lambda,f]=cFFT(datain,dt)

    %perform fft on data defined by col
    y = fft(datain,2^17);
    N = length(y);
    %remove sum term from beginning of seq.
    %y(1) = [];
    %calculate magnitude of fft
    y_mag = abs(y);
    %calculate power of fft
    y_pow = y.* conj(y)/N;
    %relative frequency according to nyquist criterion
    nyqfreq = 1/dt;
    freq = nyqfreq*(1:N/2)/N;
    %wavelength from FDTD frequency units
    wl = 2.99792458e8./freq;

	f=freq;
	lambda=wl;
	
	Y = y(1:floor(N/2)) / length(datain);
		
end

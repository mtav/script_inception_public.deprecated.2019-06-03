function probe_fft(number,sim,start,col)

% PROBE_FFT Calculate the FFT from probe file data.
%	PROBE_FFT(number,'sim',start,col) performs FFT on multiple 
%	data sets in standard University of Bristol probe file fo-
%	rmats. The number of input files is defined by number.  The 
%	appended letter on probe files is given by 'sim' (e.g. 'a').
%	start tells the subroutine where to begin. Col defines the
%	data on which to perform the FFT.
%
%	An example function call for performing the FFT on the Ey data
%	from 12 files from simulation run 'c' starting at the 15th 
%	probe would be:	PROBE_FFT(12,'c',15,3).  This would produce
%	12 files named in the form 'fft_Ey_p15.prn' to 'fft_Ey_p27.prn'.
%	
%	Version 1, 28/11/2006. Ian Buss.

%% Define columns
data_cols = ['Ex';'Ey';'Ez';'Hx';'Hy';'Hz'];

%% Calculate FFT for number files
for ii=start:1:(number+start-1)
    %load in probe file data
    if ii<10
        file = ['p0',int2str(ii),sim,'.prn'];
    elseif ii>=10
        file = ['p',int2str(ii),sim,'.prn'];
    end
    [hdr,datain] = hdrload(file);
	
    %perform fft on data defined by col
    y = fft(datain(:,col),2^17);
    N = length(y);
    %remove sum term from beginning of seq.
    %y(1) = [];
    %calculate magnitude of fft
    y_mag = abs(y);
    %calculate power of fft
    y_pow = y.* conj(y)/N;
    %relative frequency according to nyquist criterion
    nyqfreq = 1/((datain(2,1)-datain(1,1))*1e-12);
    freq = nyqfreq*(1:N/2)/N;
    %wavelength from FDTD frequency units
    wl = 2.99792458e8./freq;
	
    %set up output file
    titles = [' frequency ','wavelength ','fft_',data_cols((col-1),1:2),...
        ' fft_',data_cols((col-1),1:2),'_pow','\n'];
    outfile = ['fft_',data_cols((col-1),1:2),'_',file];
    fid = fopen(outfile,'w');
    fprintf(fid,titles);
    fclose(fid);
    out = cat(2,freq',wl',y_mag(1:floor(N/2)),y_pow(1:floor(N/2)));
    save(outfile,'out','-append','-ascii');
end
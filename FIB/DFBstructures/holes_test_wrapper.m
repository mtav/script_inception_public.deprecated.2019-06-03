mag = 30000
%dwell = 5000;
dwell = 30000;%1.5*12*2400
%radius_mum = 0.5*1e-3*860.9;
radius_mum = 0.5*1e-3*1662.5;
Ntop = 10
Nbottom = 20
size_x_mum = 2*0.066
%size_y_mum = 0.200
size_y_mum = 0.5
rep = 2

DSTDIR='~/FIBstreamfiles/'

% Note: beamCurrent argument still unused

%beamCurrent = 4
%a = holes_test([DSTDIR,filesep,'loncar'],'loncar',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep);
%a = holes_test([DSTDIR,filesep,'DFBrectSpiral'],'DFBrectSpiral',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep);
%a = holes_test([DSTDIR,filesep,'DFBrectRaster'],'DFBrectRaster',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep);
%a = holes_test([DSTDIR,filesep,'DFBtriangle'],'DFBtriangle',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep);
%dwell = 30000;%12*2400

beamCurrent = 11
%a = holes_test([DSTDIR,filesep,'loncar'],'loncar',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep);
a = holes_test([DSTDIR,filesep,'DFBrectSpiral'],'DFBrectSpiral',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep);
a = holes_test([DSTDIR,filesep,'DFBrectSpiral'],'DFBrectSpiral',mag,dwell,beamCurrent,radius_mum,0,1,size_x_mum,size_y_mum,rep);
a = holes_test([DSTDIR,filesep,'DFBrectSpiral'],'DFBrectSpiral',mag,dwell,beamCurrent,radius_mum,1,0,size_x_mum,size_y_mum,rep);
%a = holes_test([DSTDIR,filesep,'DFBrectSpiral'],'DFBrectSpiral',mag,dwell,beamCurrent,radius_mum,0,Nbottom,size_x_mum,size_y_mum,rep);
%a = holes_test([DSTDIR,filesep,'DFBrectSpiral'],'DFBrectSpiral',mag,dwell,beamCurrent,radius_mum,Ntop,0,size_x_mum,size_y_mum,rep);
%a = holes_test([DSTDIR,filesep,'DFBrectRaster'],'DFBrectRaster',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep);
%a = holes_test([DSTDIR,filesep,'DFBtriangle'],'DFBtriangle',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep);

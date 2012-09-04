mag = 30000
%dwell = 5000;
dwell = 30000;%1.5*12*2400
%radius_mum = 0.5*1e-3*860.9;
%radius_mum = 0.5*1e-3*1662.5;
radius_mum = 0.5*1e-3*1286.5;
Ntop = 10
Nbottom = 20
size_x_mum = 2*0.066
%size_y_mum = 0.200
size_y_mum = 0.5
rep = 2

%DSTDIR='~/FIBstreamfiles/1286.5_separatefiles'
DSTDIR='~/FIBstreamfiles/2012-05-23-b'

% Note: beamCurrent argument still unused

%beamCurrent = 4
%a = holes_test([DSTDIR,filesep,'loncar'],'loncar',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,customconfig);
%a = holes_test([DSTDIR,filesep,'DFBrectSpiral'],'DFBrectSpiral',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,customconfig);
%a = holes_test([DSTDIR,filesep,'DFBrectRaster'],'DFBrectRaster',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,customconfig);
%a = holes_test([DSTDIR,filesep,'DFBtriangle'],'DFBtriangle',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,customconfig);
%dwell = 30000;%12*2400

beamCurrent = 11
%a = holes_test([DSTDIR,filesep,'loncar'],'loncar',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,customconfig);
%a = holes_test([DSTDIR,filesep,'all'],'custom',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,[1,0,1,1,0,1]);

%a = holes_test([DSTDIR,filesep,'bottom'],'custom',mag,dwell,beamCurrent,radius_mum,0,Nbottom,size_x_mum,size_y_mum,rep,[1,0,1,1,0,1]);
%a = holes_test([DSTDIR,filesep,'top'],'custom',mag,dwell,beamCurrent,radius_mum,Ntop,0,size_x_mum,size_y_mum,rep,[1,0,1,1,0,1]);

a = holes_test([DSTDIR,filesep,'left'],'custom',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,[1,0,1,1,0,0]);
a = holes_test([DSTDIR,filesep,'right'],'custom',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,[1,0,1,0,0,1]);

%a = holes_test([DSTDIR,filesep,'bottom_left'],'custom',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,[1,0,1,1,0,1]);
%a = holes_test([DSTDIR,filesep,'bottom_right'],'custom',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,[1,0,1,1,0,1]);

%a = holes_test([DSTDIR,filesep,'top_left'],'custom',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,[1,0,1,1,0,1]);
%a = holes_test([DSTDIR,filesep,'top_right'],'custom',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,[1,0,1,1,0,1]);

%a = holes_test([DSTDIR,filesep,'single'],'custom',mag,dwell,beamCurrent,radius_mum,0,1,size_x_mum,size_y_mum,rep,[1,0,1,1,0,1]);
%a = holes_test([DSTDIR,filesep,'single_left'],'custom',mag,dwell,beamCurrent,radius_mum,0,1,size_x_mum,size_y_mum,rep,[1,0,1,1,0,0]);
%a = holes_test([DSTDIR,filesep,'single_right'],'custom',mag,dwell,beamCurrent,radius_mum,0,1,size_x_mum,size_y_mum,rep,[1,0,1,0,0,1]);

%a = holes_test([DSTDIR,filesep,'DFBrectSpiral'],'DFBrectSpiral',mag,dwell,beamCurrent,radius_mum,0,Nbottom,size_x_mum,size_y_mum,rep,customconfig);
%a = holes_test([DSTDIR,filesep,'DFBrectSpiral'],'DFBrectSpiral',mag,dwell,beamCurrent,radius_mum,Ntop,0,size_x_mum,size_y_mum,rep,customconfig);
%a = holes_test([DSTDIR,filesep,'DFBrectRaster'],'DFBrectRaster',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,customconfig);
%a = holes_test([DSTDIR,filesep,'DFBtriangle'],'DFBtriangle',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,customconfig);

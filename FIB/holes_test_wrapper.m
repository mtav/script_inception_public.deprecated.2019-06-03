mag=30000
%dwell=5000;
dwell=30000;%1.5*12*2400
beamCurrent=4
radius_mum = 0.5*1e-3*860.9;
DSTDIR='~/FIBstreamfiles/'
a=holes_test([DSTDIR,filesep,'loncar'],'loncar',mag,dwell,beamCurrent,radius_mum);
a=holes_test([DSTDIR,filesep,'DFBrectSpiral'],'DFBrectSpiral',mag,dwell,beamCurrent,radius_mum);
a=holes_test([DSTDIR,filesep,'DFBrectRaster'],'DFBrectRaster',mag,dwell,beamCurrent,radius_mum);
a=holes_test([DSTDIR,filesep,'DFBtriangle'],'DFBtriangle',mag,dwell,beamCurrent,radius_mum);
%dwell=30000;%12*2400
beamCurrent=11
a=holes_test([DSTDIR,filesep,'loncar'],'loncar',mag,dwell,beamCurrent,radius_mum);
a=holes_test([DSTDIR,filesep,'DFBrectSpiral'],'DFBrectSpiral',mag,dwell,beamCurrent,radius_mum);
a=holes_test([DSTDIR,filesep,'DFBrectRaster'],'DFBrectRaster',mag,dwell,beamCurrent,radius_mum);
a=holes_test([DSTDIR,filesep,'DFBtriangle'],'DFBtriangle',mag,dwell,beamCurrent,radius_mum);


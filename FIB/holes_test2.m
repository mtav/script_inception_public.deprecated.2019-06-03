mag=30000
%dwell=5000;
dwell=30000;%1.5*12*2400
beamCurrent=4
DSTDIR='/tmp/test/'
a=holes_test([DSTDIR,filesep,'loncar'],'loncar',mag,dwell,beamCurrent);
a=holes_test([DSTDIR,filesep,'DFBrectSpiral'],'DFBrectSpiral',mag,dwell,beamCurrent);
a=holes_test([DSTDIR,filesep,'DFBrectRaster'],'DFBrectRaster',mag,dwell,beamCurrent);
a=holes_test([DSTDIR,filesep,'DFBtriangle'],'DFBtriangle',mag,dwell,beamCurrent);
%dwell=30000;%12*2400
beamCurrent=11
a=holes_test([DSTDIR,filesep,'loncar'],'loncar',mag,dwell,beamCurrent);
a=holes_test([DSTDIR,filesep,'DFBrectSpiral'],'DFBrectSpiral',mag,dwell,beamCurrent);
a=holes_test([DSTDIR,filesep,'DFBrectRaster'],'DFBrectRaster',mag,dwell,beamCurrent);
a=holes_test([DSTDIR,filesep,'DFBtriangle'],'DFBtriangle',mag,dwell,beamCurrent);


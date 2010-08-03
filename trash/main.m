function main
	%% starting
	fclose all;
	close all;
	clear all; 
	clc;
	disp('# starting');
	pause(0.1);

	%% creating rand data
	% x=0:0.25:12;
	% y0=3;
	% A=4;
	% w=5;
	% x0=6;
	% v=[y0,A,w,x0];
	% fprintf('Orig:  y0=%E  A=%E  w=%E  x0=%E\n',v(1),v(2),v(3),v(4)); 
	% y=fun(v,x)+0.02*(randn(size(x))-0.5);
	% figure;
	% plot(x,y,'.');

	%% saving rand data
	% fid=fopen('data.txt','w');
	% for n=1:length(x)
	%     fprintf(fid,'%E\t %E\n',x(n),y(n));
	% end
	% fclose(fid);
	% clear all;

	%% loading data from file
	d=load('data.txt');
	x=d(:,1);
	yOrig=d(:,2);

	% fitting
	x0=7;
	y0=2.5;
	A=5;
	w=4;
	vStart=[y0,A,w,x0];
	vEnd = mylorentzfit(x,yOrig, vStart)

	%% ending
	disp('# ending');
end

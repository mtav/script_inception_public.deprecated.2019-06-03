function plotResonanceEnergy()
	% function [ E, lambda ] = resonanceEnergy(nGaAs, nAlGaAs, n0, Lcav, radius)
	% resonanceEnergy(3.521,2.973,1,253)
	% arguments
	nGaAs=3.521;%no unit
	nAlGaAs=2.973;%no unit
	n0 = 1; % air refractive index
	Lcav = 253; % (nm)

	radius = [0:0.1:5];
	[ E, lambda, radius_vector, E_vector, lambda_vector ] = resonanceEnergy(nGaAs, nAlGaAs, n0, Lcav, radius);
	
	subplot(2,1,1);
	plot(radius_vector,E_vector,'r-','LineWidth',1);
	grid on;
	hold on;
	xlabel('Radius (\mum)');
	ylabel('dE (meV)');

	subplot(2,1,2);
	plot(radius_vector,lambda_vector,'r-','LineWidth',1);
	grid on;
	hold on;
	xlabel('Radius (\mum)');
	ylabel('\lambda (nm)');
	
	subplot(2,1,1);
	plot(radius,E,'o','LineWidth',1);
	grid on;
	hold on;
	xlabel('Radius (\mum)');
	ylabel('dE (meV)');

	subplot(2,1,2);
	plot(radius,lambda,'o','LineWidth',1);
	grid on;
	hold on;
	xlabel('Radius (\mum)');
	ylabel('\lambda (nm)');
end

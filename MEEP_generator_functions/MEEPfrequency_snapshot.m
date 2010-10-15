function MEEP_frequency_snapshot(FILE, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, frequency, starting_sample, E, H, J)

	function snapshot(plane,P1,P2, frequency)
		if plane == 1
			plane_name='X';
		elseif plane == 2
			plane_name='Y';
		else %plane == 3
			plane_name='Z';
		end
		fprintf(FILE,'FREQUENCY_SNAPSHOT **SNAPSHOT DEFINITION %s\n',plane_name);
		fprintf(FILE,'{\n');
		fprintf(FILE,'%d **FIRST\n', first);
		fprintf(FILE,'%d **REPETITION\n', repetition);
		fprintf(FILE,'%d **interpolate?\n', interpolate);
		fprintf(FILE,'%d **REAL DFT\n', real_dft);
		fprintf(FILE,'%d **MOD ONLY\n', mod_only);
		fprintf(FILE,'%d **MOD ALL\n', mod_all);
		fprintf(FILE,'%d **PLANE\n', plane);
		fprintf(FILE,'%E **X1\n', P1(1));
		fprintf(FILE,'%E **Y1\n', P1(2));
		fprintf(FILE,'%E **Z1\n', P1(3));
		fprintf(FILE,'%E **X2\n', P2(1));
		fprintf(FILE,'%E **Y2\n', P2(2));
		fprintf(FILE,'%E **Z2\n', P2(3));
		fprintf(FILE,'%E **FREQUENCY (HZ)\n', frequency);
		fprintf(FILE,'%d **STARTING SAMPLE\n', starting_sample);
		fprintf(FILE,'%d **EX\n', E(1));
		fprintf(FILE,'%d **EY\n', E(2));
		fprintf(FILE,'%d **EZ\n', E(3));
		fprintf(FILE,'%d **HX\n', H(1));
		fprintf(FILE,'%d **HY\n', H(2));
		fprintf(FILE,'%d **HZ\n', H(3));
		fprintf(FILE,'%d **JX\n', J(1));
		fprintf(FILE,'%d **JY\n', J(2));
		fprintf(FILE,'%d **JZ\n', J(3));
		fprintf(FILE,'}\n');
		fprintf(FILE,'\n');
	end
	
	for i = 1:length(frequency)
		if P1(plane) == P2(plane)
			snapshot(plane,P1,P2,frequency(i));
		else
			snapshot(1,[P1(1),P1(2),P1(3)],[P1(1),P2(2),P2(3)],frequency(i));
			snapshot(1,[P2(1),P1(2),P1(3)],[P2(1),P2(2),P2(3)],frequency(i));
			snapshot(2,[P1(1),P1(2),P1(3)],[P2(1),P1(2),P2(3)],frequency(i));
			snapshot(2,[P1(1),P2(2),P1(3)],[P2(1),P2(2),P2(3)],frequency(i));
			snapshot(3,[P1(1),P1(2),P1(3)],[P2(1),P2(2),P1(3)],frequency(i));
			snapshot(3,[P1(1),P1(2),P2(3)],[P2(1),P2(2),P2(3)],frequency(i));
		end
	end
	
end

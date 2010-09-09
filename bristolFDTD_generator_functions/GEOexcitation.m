function GEOexcitation(FILE, current_source, P1, P2, E, H, type, time_constant, amplitude, time_offset, frequency, param1, param2, param3, param4)
	fprintf(FILE,'EXCITATION **EXCITATION DEFINITION\n');
	fprintf(FILE,'{\n');
	fprintf(FILE,'%d ** CURRENT SOURCE \n', current_source);
	fprintf(FILE,'%E **X1\n', P1(1));
	fprintf(FILE,'%E **Y1\n', P1(2));
	fprintf(FILE,'%E **Z1\n', P1(3));
	fprintf(FILE,'%E **X2\n', P2(1));
	fprintf(FILE,'%E **Y2\n', P2(2));
	fprintf(FILE,'%E **Z2\n', P2(3));
	fprintf(FILE,'%d **EX\n', E(1));
	fprintf(FILE,'%d **EY\n', E(2));
	fprintf(FILE,'%d **EZ\n', E(3));
	fprintf(FILE,'%d **HX\n', H(1));
	fprintf(FILE,'%d **HY\n', H(2));
	fprintf(FILE,'%d **HZ\n', H(3));
	fprintf(FILE,'%d **GAUSSIAN MODULATED SINUSOID\n', type);
	fprintf(FILE,'%E **TIME CONSTANT\n', time_constant);
	fprintf(FILE,'%E **AMPLITUDE\n', amplitude);
	fprintf(FILE,'%E **TIME OFFSET\n', time_offset);
	fprintf(FILE,'%E **FREQ (HZ)\n', frequency);
	fprintf(FILE,'%d **UNUSED PARAMETER\n', param1);
	fprintf(FILE,'%d **UNUSED PARAMETER\n', param2);
	fprintf(FILE,'%d **UNUSED PARAMETER\n', param3);
	fprintf(FILE,'%d **UNUSED PARAMETER\n', param4);
	fprintf(FILE,'}\n');
	fprintf(FILE,'\n');
end

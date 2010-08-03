function GEOtime_snapshot(FILE, first, repetition, plane, P1, P2, E, H, J, power)
		
	function snapshot(plane,P1,P2)
		if plane == 1
			plane_name='X';
		elseif plane == 2
			plane_name='Y';
		else %plane == 3
			plane_name='Z';
		end

		fprintf(FILE,'SNAPSHOT **SNAPSHOT DEFINITION %s\n',plane_name);
		fprintf(FILE,'{\n');
		fprintf(FILE,'%d **FIRST\n', first);
		fprintf(FILE,'%d **REPETITION\n', repetition);
		fprintf(FILE,'%d **PLANE\n', plane);
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
		fprintf(FILE,'%d **JX\n', J(1));
		fprintf(FILE,'%d **JY\n', J(2));
		fprintf(FILE,'%d **JZ\n', J(3));
		fprintf(FILE,'%d **POW\n', power);
		fprintf(FILE,'}\n');
		fprintf(FILE,'\n');
	end
	
	if P1(plane) == P2(plane)
		snapshot(plane,P1,P2);
	else
		snapshot(1,[P1(1),P1(2),P1(3)],[P1(1),P2(2),P2(3)]);
		snapshot(1,[P2(1),P1(2),P1(3)],[P2(1),P2(2),P2(3)]);
		snapshot(2,[P1(1),P1(2),P1(3)],[P2(1),P1(2),P2(3)]);
		snapshot(2,[P1(1),P2(2),P1(3)],[P2(1),P2(2),P2(3)]);
		snapshot(3,[P1(1),P1(2),P1(3)],[P2(1),P2(2),P1(3)]);
		snapshot(3,[P1(1),P1(2),P2(3)],[P2(1),P2(2),P2(3)]);
	end
	
end

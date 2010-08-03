function ret = getinput(i)
	if i == 0
		ret = 'J:\optics\MikeT\Andrew_pillars_20100607_done\pillar_M2754_0_10';
	elseif i == 1
		ret = 'S:\Andrew_pillar_harminv\pillar_M2754_0_10';
	elseif i == 2
		ret = 'J:\optics\MikeT\Andrew_pillars_20100607_done';
	elseif i == 3
		% ret = 'S:\Andrew_pillar_harminv';
		ret = fullfile(getuserdir(),'DATA','Andrew_pillar_harminv');
	elseif i == 4
		ret = 'D:\DATA\Andrew_pillars';
	elseif i == 5
		ret = 'D:\DATA\Andrew_pillars\pillar_M2754_0_10';
	elseif i == 6
		ret = fullfile(getuserdir(),'loncar_structure');
	elseif i == 7
		ret = 'D:\DATA\Andrew_pillars\pillar_M2754_0_10';
	elseif i == 8
		ret = fullfile(getuserdir(),'DATA','Andrew_pillar_harminv','pillar_M2754_0_10');
		% ret = 'S:\Andrew_pillar_harminv\pillar_M2754_0_10';
		% 'D:\DATA\Andrew_pillars\pillar_M2754_0_10';
		% fullfile(getuserdir(),'DATA','newPillars','pillar_M2754_0_10_32000');
	else
		ret = '';
	end
end

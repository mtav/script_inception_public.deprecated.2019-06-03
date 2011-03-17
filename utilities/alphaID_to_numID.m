function [ numID, snap_plane, snap_time_number ] = alphaID_to_numID(alphaID, probe_ident)
	% Converts alpha IDs used by Bristol FDTD 2003 to numeric IDs
	% function [ numID, snap_plane, snap_time_number ] = alphaID_to_numID(alphaID, probe_ident)
	% examples:
	% z -> 26
	% a{ -> 26+27
	% MAXIMUM NUMBER OF SNAPSHOTS: 32767 (=(2^8)*(2^8)/2 -1)
	% MAXIMUM NUMBER OF SNAPSHOTS BEFORE RETURN to aa: 6938 = 26+256*27
	% MAXIMUM NUMBER OF SNAPSHOTS BEFORE DUPLICATE IDs: 4508 = 26+(6-(ord('a')-1)+256)*27+1 (6=character before non-printable bell character)
	% MAXIMUM NUMBER OF SNAPSHOTS BEFORE ENTERING DANGER AREA (non-printable characters): 836 = 26+(126-(ord('a')-1))*27
	
	function ret = div(A,B)
		ret = idivide(int32(A),int32(B));
	end
	
	if exist('probe_ident','var')==0
		probe_ident = 'id';
	end

	if(~ischar(alphaID))
		error('alphaID should be a string.')
	end
	
	% step 1: extract just alphaID
	% length_of_basename = length(snap_plane)+length(probe_ident)+2+length('.prn');
	
	alphaID_pattern = '([a-z\{\|\}~][a-z\{]|[a-z])';
	
	if length(alphaID)==1 | length(alphaID)==2
		[tokens match] =  regexp(alphaID, alphaID_pattern, 'tokens', 'match', 'warnings');
		if length(match)==1
			snap_plane = 'x';
			just_alphaID = alphaID;
			snap_time_number = 0;
		else
			error('Match error. Invalid alphaID.');
		end
	elseif length(alphaID)>2
		[tokens match] =  regexp(alphaID, ['([xyz])',alphaID_pattern,probe_ident,'(..)\.prn'], 'tokens', 'match', 'warnings');
		if length(match)==1
			snap_plane = tokens{:}(1);
			just_alphaID = tokens{:}{2};
			snap_time_number = str2num(tokens{:}{3});
		else
			error('Match error. Invalid alphaID.');
		end
	else
		error('Me thinks you made a little mistake in your alphaID...');
	end
	
	% snap_plane
	% just_alphaID
	% probe_ident
	% snap_time_number
	
	ilo = mod(snap_time_number,10);
	ihi = div(snap_time_number,10);
	
	% filename = strcat({snap_plane}, just_alphaID, {probe_ident}, char(ihi + double('0')), char(ilo + double('0')), '.prn');

	% disp(filename);
	
	% class(just_alphaID)
	% whos just_alphaID
	% size(just_alphaID)

	% disp('===MWAHAHAHAHHAHA===');
	if length(just_alphaID)==1
		% disp('single');
		numID = double(just_alphaID(1)) - double('a') + 1;
	else
		% disp('double');
		numID = 27*(double(just_alphaID(1)) - double('a') + 1) + (double(just_alphaID(2)) - double('a'));
	end

	% disp('===THE END===');
	% numID
end

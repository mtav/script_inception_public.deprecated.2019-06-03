function [dy,dV] = subGridMultiLayer(max_delta_Vector,thicknessVector)
	% Create a list of thicknesses for meshing
	% [dy,dV] = subGridMultiLayer(max_delta_Vector,thicknessVector)
	% dy = thicknessVector of the mesh
	% dV = list of final deltas used in the mesh
	% ex:
	% dy = [ 3,2,2,1,1,1 ]
	% dV = [ 3,2,1 ]

	if (nargin==0)
		max_delta_Vector = [1.76, 2.1385, 2.3535, 1];
		thicknessVector = [1, 0.5, 1, 1];
	end
	
	if( size(max_delta_Vector) ~= size(thicknessVector) )
		disp('FATAL ERROR: The 2 input vectors do not have the same size.');
		return
	end

	totalHeight = sum(thicknessVector);

	nLayers = length(thicknessVector);

	nCellsV = ceil( thicknessVector ./ max_delta_Vector );
	dV = thicknessVector ./ nCellsV;

	dy = [];
	for m=1:nLayers
		dy = [dy,dV(m)*ones(1,nCellsV(m))];
	end
end

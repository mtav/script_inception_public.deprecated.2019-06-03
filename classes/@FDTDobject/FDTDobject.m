% Class containing data necessary for FDTD simulations
classdef FDTDobject
   properties
    all_snapshots = [];
	time_snapshots =  [];
	frequency_snapshots =  [];
	excitations =  [];
    sphere_list =  [];
    block_list =  [];
    cylinder_list =  [];
    rotation_list =  [];
    probe_list =  [];
	xmesh = [];
	ymesh = [];
	zmesh = [];
    flag = struct('iMethod',{},'propCons',{},'flagOne',{},'flagTwo',{},'numSteps',{},'stabFactor',{},'id',{});
    boundaries = struct('type',{},'position',{});
    box = struct('lower',{},'upper',{});
   end
end

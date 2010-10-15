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
    flag = struct('iMethod',{0},'propCons',{0},'flagOne',{0},'flagTwo',{0},'numSteps',{0},'stabFactor',{0},'id',{'_id_'});
    boundaries = struct('type',{0,0,0,0,0,0},'position',{[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]});
    box = struct('lower',{[0,0,0]},'upper',{[0,0,0]});
   end
end

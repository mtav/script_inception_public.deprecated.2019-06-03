% Class containing data necessary for FDTD simulations
classdef FDTDobject
   properties
    % geometry objects
    sphere_list =  [];
    block_list =  [];
    cylinder_list =  [];
    rotation_list =  [];
    geometry_object_list = [];
    % mesh
  xmesh = [];
  ymesh = [];
  zmesh = [];
    % input
  excitations =  [];
    flag = struct('iMethod',{0},'propCons',{0},'flagOne',{0},'flagTwo',{0},'numSteps',{0},'stabFactor',{0},'id',{'_id_'});
    boundaries = struct('type',{0,0,0,0,0,0},'position',{[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]});
    box = struct('lower',{[0,0,0]},'upper',{[0,0,0]});
    % output
    all_snapshots = [];
  time_snapshots =  [];
  frequency_snapshots =  [];

  time_snapshots_X =  [];
  time_snapshots_Y =  [];
  time_snapshots_Z =  [];
    
  frequency_snapshots_X =  [];
  frequency_snapshots_Y =  [];
  frequency_snapshots_Z =  [];
    
    probe_list =  [];
   end
end

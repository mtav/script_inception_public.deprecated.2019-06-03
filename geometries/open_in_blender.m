function [status,result] = open_in_blender(FILE)
    [status,result] = system(['"C:\Program Files\Blender Foundation\Blender\blender" -P "',getenv('USERPROFILE'),'\Application Data\Blender Foundation\Blender\.blender\scripts\bfdtd_import.py" -- "',FILE,'"'])
end

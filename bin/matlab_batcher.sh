#!/bin/sh
# source : http://stackoverflow.com/questions/2001183/how-to-call-matlab-functions-from-linux-command-line

matlab_exec=matlab
X="${1}(${2})"
echo ${X} > matlab_command_${2}.m
cat matlab_command_${2}.m
${matlab_exec} -nojvm -nodisplay -nosplash < matlab_command_${2}.m
rm matlab_command_${2}.m

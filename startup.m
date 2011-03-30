function startup()
    disp('Recursively adding paths...');
    DEBUG=false;
    HOME=getuserdir();
    addpath([HOME,filesep,'MATLAB',filesep,'addpath_recurse']);
    addpath([HOME,filesep,'MATLAB',filesep,'utilities']);
    addpath_recurse([HOME,filesep,'MATLAB'],{'.git'},'begin',false,DEBUG);
    addpath_recurse([HOME,filesep,'Development',filesep,'script_inception_private'],{'.git'},'begin',false,DEBUG);
    disp('...done');
end

function userDir = getuserdir()
    %GETUSERDIR   return the user home directory.
    %   USERDIR = GETUSERDIR returns the user home directory using the registry
    %   on windows systems and using Java on non windows systems as a string
    %
    %   Example:
    %      getuserdir() returns on windows
    %           C:\Documents and Settings\MyName\Eigene Dateien

    if ispc
        % userDir = winqueryreg('HKEY_CURRENT_USER',...
            % ['Software\Microsoft\Windows\CurrentVersion\' ...
             % 'Explorer\Shell Folders'],'Personal');
        userDir = getenv('MYDOCUMENTS');
    else
%        userDir = char(java.lang.System.getProperty('user.home'));
        userDir = getenv('HOME');
    end
end

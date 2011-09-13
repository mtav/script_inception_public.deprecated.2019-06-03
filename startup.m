function startup()
    disp('Recursively adding paths...');

    DEBUG = false;
    HOME = getuserdir();
    PRIVATE_REPO_DIR = [HOME,filesep,'Development',filesep,'script_inception_private'];

    % Adapt those settings according to your setup and where you placed the repository
    PUBLIC_REPO_DIR = [HOME,filesep,'MATLAB'];
    %PUBLIC_REPO_DIR = 'C:\script_inception_public';

    addpath([PUBLIC_REPO_DIR,filesep,'addpath_recurse']);
    addpath([PUBLIC_REPO_DIR,filesep,'utilities']);
    addpath_recurse(PUBLIC_REPO_DIR,{'.git'},'begin',false,DEBUG);
    if exist(PRIVATE_REPO_DIR,'dir')
      addpath_recurse(PRIVATE_REPO_DIR,{'.git'},'begin',false,DEBUG);
    else
      disp(['PRIVATE_REPO_DIR = ',PRIVATE_REPO_DIR,' not found. Skipping it.'])
    end
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
        userDir = getenv('MYDOCUMENTS');
	if isempty(userDir)
          userDir = winqueryreg('HKEY_CURRENT_USER',['Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'],'Personal');
	end
    else
%        userDir = char(java.lang.System.getProperty('user.home'));
        userDir = getenv('HOME');
    end
end

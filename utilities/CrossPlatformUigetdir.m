function DIR = CrossPlatformUigetdir()
  if inoctave()
    pkg load zenity;
    DIR = zenity_file_selection('hello','directory');
  else
    DIR = uigetdir();
  end
end

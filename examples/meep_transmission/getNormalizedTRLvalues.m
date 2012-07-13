function [ frequency, transmission_normalized, reflection_normalized, loss ] = getNormalizedTRLvalues(reference_file, geometry_file)

  bend0 = dlmread(reference_file,',',0,1);
  bend = dlmread(geometry_file,',',0,1);

  frequency = bend(:,1);

  transmitted_flux = bend(:,2);
  reflected_flux = bend(:,3);
  incident_flux = bend0(:,2);

  total = incident_flux;
  %total = transmitted_flux - reflected_flux;

  transmission_normalized = transmitted_flux./total;
  reflection_normalized = -reflected_flux./total;

  loss = 1 - transmission_normalized - reflection_normalized;

end

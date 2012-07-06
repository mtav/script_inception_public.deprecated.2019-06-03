% script to plot photonic bandgap diagrams from MPB output
function plot_MPB(filename,scale_factor)
  [ folder, basename, ext ] = fileparts(filename);
  [header, rawdata] = readPrnFile(filename);
  %close all;
  figure;
  hold all;
  % scale_factor = 1.0;
  % scale_factor = 1.0/sqrt(2);
  data = scale_factor*rawdata;
  N = length(header);
  firstband = find(strcmp(header,'band_1'));
  for m=firstband:N
    plot(data(:,1),data(:,m))
  end
  legend(header(firstband:N),'Interpreter', 'none');
  title(filename,'Interpreter', 'none');

  %top = min(min(data(:,firstband+2:N)));
  %bot = max(max(data(:,firstband:firstband+1)));
  %top_line = hline(top,'r',num2str(top));
  %bot_line = hline(bot,'r',num2str(bot));

  % mid-gaps

  %i = 2
  %a = data(1+(i-1)*10,find(strcmp(header,'band_5')));
  %b = data(1+(i-1)*10,find(strcmp(header,'band_6')));
  %delta = abs(b-a);
  %hline(a,'r',num2str(a));
  %hline(b,'r',num2str(b));
  %text(1,0.5*(a+b),num2str(delta));

  i = 5
  a = data(1+(i-1)*10,find(strcmp(header,'band_2')))
  b = data(1+(i-1)*10,find(strcmp(header,'band_3')))
  delta = abs(b-a);
  %hline(a,'r',num2str(a));
  %hline(b,'r',num2str(b));
  %text(1,0.5*(a+b),num2str(delta));
  gap = abs(b-a)
  midgap = 0.5*(a+b)
  hline(midgap,'r',num2str(midgap));
  
  %midgap1=0.645561870915862
  %hline(midgap1,'r',num2str(midgap1));
  %midgap2=0.673605092161939
  %hline(midgap2,'r',num2str(midgap2));
  %midgap3=0.5*(midgap1+midgap2)
  %hline(midgap3,'r',num2str(midgap3));

  %hline(0.585,'b',num2str(0.585));

  spacepoints = {'X','U','L','\Gamma','W','K','X''','U''','W''','K''','W'''''};
  %spacepoints = {'X','U','L','\Gamma','X''','W''','K'''};
  for i=1:length(spacepoints)
    vline(data(1+(i-1)*10,1),'r',spacepoints{i});
  end
  print(gcf,'-dpng','-r300',[filename,'.png']);
end


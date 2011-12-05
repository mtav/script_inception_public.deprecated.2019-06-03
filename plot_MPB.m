% script to plot photonic bandgap diagrams from MPB output
function plot_MPB(filename)
  [ folder, basename, ext ] = fileparts(filename);
  [header, data] = readPrnFile(filename);
  close all;
  figure;
  hold all;
  N=length(header);
  firstband = find(strcmp(header,'band_1'));
  for m=firstband:N
    plot(data(:,1),data(:,m))
  end
  legend(header(firstband:N),'Interpreter', 'none');
  title(filename,'Interpreter', 'none');
  top = min(min(data(:,firstband+2:N)));
  bot = max(max(data(:,firstband:firstband+1)));
  top_line = hline(top,'r',['max = ',num2str(top)]);
  bot_line = hline(bot,'r',['min = ',num2str(bot)]);
  print(gcf,'-dpng','-r300',[filename,'.png']);
end

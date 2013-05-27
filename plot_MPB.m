% script to plot photonic bandgap diagrams from MPB output
function plot_MPB(filename,scale_factor,titolo)

  [ folder, basename, ext ] = fileparts(filename);
  [header, rawdata] = readPrnFile(filename);
  %close all;
  figure;

  %set(gca,'fontsize',14);
  %set(gcf, 'PaperSize', [8. 6.],'PaperPositionMode', 'auto');
  
  hold all;
  % scale_factor = 1.0;
  % scale_factor = 1.0/sqrt(2);
  %tofreq_factor = (get_c0/(4*6.35*1e-3))*1e-9; % convert to GHz for a=4*6.35mm
  tofreq_factor = 1
  data = tofreq_factor*scale_factor*rawdata;
  N = length(header);
  firstband = find(strcmp(header,'band_1'));
  for m=firstband:N
    plot(data(:,2),data(:,m),'markersize',10,'markerfacecolor','auto')
  end
  legend(header(firstband:N),'Interpreter', 'none','location','northeast');

  xlabel('direction','fontsize',16);
  ylabel('f=c_{0}/\lambda (GHz)','fontsize',16);

  %top = min(min(data(:,firstband+2:N)));
  %bot = max(max(data(:,firstband:firstband+1)));
  %mid = 0.5*(top+bot);
  %top_line = hline(top,'r',num2str(top));
  %mid_line = hline(mid,'r',num2str(mid));
  %bot_line = hline(bot,'r',num2str(bot));
  
  %disp(['top = ',num2str(top)]);
  %disp(['mid = ',num2str(mid)]);
  %disp(['bot = ',num2str(bot)]);

  % mid-gaps

  %i = 2
  %aa = data(1+(i-1)*10,find(strcmp(header,'band_5')));
  %b = data(1+(i-1)*10,find(strcmp(header,'band_6')));
  %delta = abs(b-aa);
  %hline(aa,'r',num2str(aa));
  %hline(b,'r',num2str(b));
  %text(1,0.5*(aa+b),num2str(delta));

  %i = 3 % L direction
  %aa = data(1+(i-1)*10,find(strcmp(header,'band_2')))
  %b = data(1+(i-1)*10,find(strcmp(header,'band_3')))
  %delta = abs(b-aa);
  %hline(aa,'r',num2str(aa));
  %hline(b,'r',num2str(b));
  %text(1,0.5*(aa+b),num2str(delta));
  %gap = abs(b-aa)
  %midgap = 0.5*(aa+b)
  %gapsize = gap/midgap
  %hline(midgap,'r',num2str(midgap));

  %i = 7;
  %maxi = data(1+(i-1)*10,find(strcmp(header,'band_3')));
  %i = 7;
  %mini = data(1+(i-1)*10,find(strcmp(header,'band_2')));
  %delta = abs(maxi-mini);
  %hline(aa,'r',num2str(aa));
  %hline(b,'r',num2str(b));
  %text(1,0.5*(aa+b),num2str(delta));
  %gap = abs(maxi-mini);
  %midgap = 0.5*(mini+maxi);
  %gapsize = gap/midgap;
  hold on;
  %hline(mini,'r',num2str(mini));
  %hline(midgap,'g',num2str(midgap));
  %hline(maxi,'b',num2str(maxi));
  
  %lambda0=1.55
  %lambda0 = 0.637;
  %a_value = midgap*lambda0;
  %lambda_mini = a_value/mini;
  %lambda_midgap = a_value/midgap;
  %lambda_maxi = a_value/maxi;
  
  %disp(['midgap = ',num2str(midgap)]);
  %disp(['lambda0 = ',num2str(lambda0)]);
  %disp(['a_value = ',num2str(a_value)]);
  %disp(['lambda_mini = ',num2str(lambda_mini)]);
  %disp(['lambda_midgap = ',num2str(lambda_midgap)]);
  %disp(['lambda_maxi = ',num2str(lambda_maxi)]);
  
  %midgap1=0.645561870915862
  %hline(midgap1,'r',num2str(midgap1));
  %midgap2=0.673605092161939
  %hline(midgap2,'r',num2str(midgap2));
  %midgap3=0.5*(midgap1+midgap2)
  %hline(midgap3,'r',num2str(midgap3));

  %hline(0.585,'b',num2str(0.585));

  %spacepoints = {'X','U','L','\Gamma','W','K','X''','U''','W''','K''','W'''''};
  %spacepoints = {'X','U','W'};
  %spacepoints = {'X','U','L','\Gamma','X''','W''','K'''};
  %spacepoints = {'\Gamma','X','U','L'};
  %for i=1:length(spacepoints)
    %vline(data(1+(i-1)*10,1),'r',spacepoints{i});
  %end
  
  
%set(gca,'Box','off');   %# Turn off the box surrounding the whole axes
%axesPosition = get(gca,'Position');          %# Get the current axes position


%a_over_lambda_range = get(gca,'YLim');
%a_over_lambda_range(1)=0.01
%set(gca, 'YLim', a_over_lambda_range)

%lambda_range = a_value./a_over_lambda_range

%hNewAxes = axes('Position',axesPosition,...  %# Place a new axes on top...
                %'Color','none',...           %#   ... with no background color
                %'YLim',lambda_range(end:-1:1) ,...            %#   ... and a different scale
                %'YAxisLocation','right',...  %#   ... located on the right
                %'XTick',[],...               %#   ... with no x tick marks
                %'Box','off');                %#   ... and no surrounding box
%ylabel(hNewAxes,'scale 2');  %# Add a label to the right y axis
%set(hNewAxes,'YDir','reverse');

  %titolo = [filename,', "log width:" w=0.2*a, "vertical 4-layer period:" a=',num2str(a_value),' mum, "horizontal period": d=a/sqrt(2)=',num2str(a_value/sqrt(2)),' mum'];
  %titolo = [filename,', w=0.2*a, a=',num2str(a_value),' mum, d=a/sqrt(2)=',num2str(a_value/sqrt(2)),' mum'];
  %title(titolo,'Interpreter', 'none','fontsize',20);
  %disp(['w=0.2*a, "*a vertical 4-layer period:" a=',num2str(a_value),' mum, "horizontal period": d=a/sqrt(2)=',num2str(a_value/sqrt(2)),' nm']);
  %disp(titolo);

  %set(gcf, 'Position', get(0,'Screensize')); % Maximize figure.
  %saveas(gcf,[filename,'.fig'],'fig');
  % octave compatible image saving
  %print(gcf,'-dpng','-r300',[filename,'.png']);
  %print('-r600','-dpng',[filename,'.png']);
  %print('-r600','-dpdf',[filename,'.pdf']);
end

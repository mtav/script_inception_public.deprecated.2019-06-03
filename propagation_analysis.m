function propagation_analysis(INFILENAME,AMPLITUDE,TIME_OFFSET,TIME_CONSTANT,FREQUENCY)

    % x=0.25;
    % delta=20*1/FREQUENCY;t=[TIME_OFFSET-delta/2:delta/100:TIME_OFFSET+delta/2];
    % t=t-x/get_c0();
    % plot(t+x/get_c0(),AMPLITUDE*exp(-log(2)*((t-TIME_OFFSET)/TIME_CONSTANT).^2).*sin(2*pi*FREQUENCY*t));
    % hold on;

    % x=10;
    % delta=20*1/FREQUENCY;t=[TIME_OFFSET-delta/2:delta/100:TIME_OFFSET+delta/2];
    % t=t-x/get_c0();
    % plot(t,AMPLITUDE*exp(-log(2)*((t-TIME_OFFSET)/TIME_CONSTANT).^2).*sin(2*pi*FREQUENCY*t));

    % x=20;
    % delta=20*1/FREQUENCY;t=[TIME_OFFSET-delta/2:delta/100:TIME_OFFSET+delta/2];
    % t=t-x/get_c0();
    % plot(t,AMPLITUDE*exp(-log(2)*((t-TIME_OFFSET)/TIME_CONSTANT).^2).*sin(2*pi*FREQUENCY*t));

    % x=30;
    % delta=20*1/FREQUENCY;t=[TIME_OFFSET-delta/2:delta/100:TIME_OFFSET+delta/2];
    % t=t-x/get_c0();
    % plot(t,AMPLITUDE*exp(-log(2)*((t-TIME_OFFSET)/TIME_CONSTANT).^2).*sin(2*pi*FREQUENCY*t));

    delta=20*1/FREQUENCY;
    t_init=[TIME_OFFSET-delta/2:delta/100:TIME_OFFSET+delta/2];
    hold on;
    % x=0;
    % t=t_init+x/get_c0();
    % plot(t,AMPLITUDE*exp(-log(2)*(((t-x/get_c0())-TIME_OFFSET)/TIME_CONSTANT).^2).*sin(2*pi*FREQUENCY*(t-x/get_c0())));
    % x=10;
    % toto(0);
    % toto(10);

    function plot_theory(x,style)
        t=t_init+x/get_c0();
        plot(t,AMPLITUDE*exp(-log(2)*(((t-x/get_c0())-TIME_OFFSET)/TIME_CONSTANT).^2).*sin(2*pi*FREQUENCY*(t-x/get_c0())),style);
    end
    
    function plot_simulation(file)
        [header, data] = readPrnFile(file);
        plot(data(:,1)*10^-12,data(:,2),'ko--');
    end

    plot_theory(0,'y-');
    
    plot_simulation('p01id.prn');
    plot_theory(0.25,'m-');
    
    plot_simulation('p02id.prn');
    plot_theory(10,'c-');
    
    plot_simulation('p03id.prn');
    plot_theory(20,'r-');
    
    plot_simulation('p04id.prn');
    plot_theory(30,'g-');
    
    plot_simulation('p01id.prn');
    plot_theory(40,'b-');

end

% function plot_probe_signal(INFILENAME,AMPLITUDE,TIME_OFFSET,TIME_CONSTANT,FREQUENCY,x)
    % delta=20*1/FREQUENCY;t=[TIME_OFFSET-delta/2:delta/100:TIME_OFFSET+delta/2];
    % t=t-x/get_c0();
    % plot(t,AMPLITUDE*exp(-log(2)*((t-TIME_OFFSET)/TIME_CONSTANT).^2).*sin(2*pi*FREQUENCY*t));
% end

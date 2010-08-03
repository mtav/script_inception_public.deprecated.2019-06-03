function hdrsave(filename,header,data)
% function hdrsave(filename,header,data)

% write header
file = fopen(filename,'w');
% fprintf(file,'%s\r\n',header);
fprintf(file,[header,'\r\n']);
fclose(file);

% write data
save(filename, 'data', '-ascii', '-double', '-tabs', '-append')

end

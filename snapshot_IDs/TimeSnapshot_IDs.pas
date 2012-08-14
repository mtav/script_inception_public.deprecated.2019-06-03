assign(ipfile,'i'+chr(snap_serial_number + ord('0'))+probe_ident+'00.prn');

ilo:=snap_time_number mod 10;ihi:=snap_time_number div 10;
{$IFNDEF small } with runtime_flags do {$ENDIF}

if snap_serial_number<10 then begin
assign(snapfile,snap_plane+chr(snap_serial_number + ord('0'))+probe_ident+chr(ihi + ord('0'))+chr(ilo + ord('0'))+'.prn');
rewrite(snapfile);
end else begin
assign(snapfile,snap_plane+chr((snap_serial_number div 10) + ord('0'))+chr((snap_serial_number mod 10) + ord('0'))+probe_ident+chr(ihi + ord('0'))+chr(ilo + ord('0'))+'.prn');
rewrite(snapfile);
end;

ilo:=snap_time_number mod 10;ihi:=snap_time_number div 10;
{$IFNDEF small } with runtime_flags do {$ENDIF}
if snap_serial_number<27 then begin
assign(snapfile,snap_plane+chr(snap_serial_number + ord('a')-1)+probe_ident+chr(ihi + ord('0'))+chr(ilo + ord('0'))+'.prn');
rewrite(snapfile);
end else begin
assign(snapfile,snap_plane+chr((snap_serial_number div 27) + ord('a')-1)+chr((snap_serial_number mod 27) + ord('a'))+probe_ident+chr(ihi + ord('0'))+chr(ilo + ord('0'))+'.prn');
rewrite(snapfile);
end;

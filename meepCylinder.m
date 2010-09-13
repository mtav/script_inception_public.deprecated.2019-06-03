function C=meepCylinder(center,radius,height,axis,epsilon)

if height==-1
    heightStr='infinity';
else
    heightStr=num2str(height,'%4.9g');
end

if  length(axis)
    axisStr=['(axis (vector3 ',num2str(axis,'%4.9g '),'))'];
else
    axisStr='';
end

C=['(make cylinder\r\n\t(center ',num2str(center,'%4.11g '),')\r\n\t(radius ',num2str(radius,'%4.9g'),')\r\n\t(height ',heightStr,')\r\n\t',axisStr,'(material (make dielectric (epsilon ',num2str(epsilon,'%4.9g'),'))))\r\n'];
		
            
            
% Center=struct('type',{'center'},'properties',{{center}});
% Size=struct('type',{'size'},'properties',{{size}});
% Epsilon=struct('type',{'epsilon'},'properties',{{epsilon}});
% Make=struct('type',{'make'},'properties',{{'dielectric',Epsilon}});
% Material=struct('type',{'material'},'properties',{{Make}});
% 
% B=struct('type',{'block'},'properties',{{Center,Size,Material}})
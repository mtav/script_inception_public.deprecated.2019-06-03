function C=meepSphere(center,radius,epsilon)

if size(center,2)==1
    center=center';
end

C=['(make sphere\r\n\t(center ',num2str(center,'%2.5f '),')\r\n\t(radius ',num2str(radius,'%2.5f'),')\r\n\t\t\r\n\t(material (make dielectric (epsilon ',num2str(epsilon,'%2.5f'),'))))\r\n'];
		
            
            
% Center=struct('type',{'center'},'properties',{{center}});
% Size=struct('type',{'size'},'properties',{{size}});
% Epsilon=struct('type',{'epsilon'},'properties',{{epsilon}});
% Make=struct('type',{'make'},'properties',{{'dielectric',Epsilon}});
% Material=struct('type',{'material'},'properties',{{Make}});
% 
% B=struct('type',{'block'},'properties',{{Center,Size,Material}})
clear all;

x=importdata('0_10_matlab_sorted_angles_data.txt',',',0);

y=importdata('0_11_matlab_diff_pot_data.txt',',',0);

[m,n]=size(x);

multiplicity = 3;

multiplicity2 = multiplicity*2;

total=1;%2^multiplicity;

r=zeros(total,1);

rows=n;

sum=0;

sign=1;

Da=zeros(1,multiplicity);

for b=0:total-1
for a=0:multiplicity-1
	
	if sign==1
		
		sum=sum+(2^(multiplicity-a)/2);

	else	

		sum=sum-(2^(multiplicity-a)/2);
	
	end

	if sum<=b
		Da(1,multiplicity-1-a+1)=0;
		sign=1;
	
	else
		Da(1,multiplicity-1-a+1)=pi;
		sign=-1;
	end		
	
end
	sum=0;
	sign=1;
	D(:,:,b+1)=Da;
	Da=zeros(1,multiplicity);
end

cT=0;
for i=1:n
 cT=cT+y(i); 
end

cT=cT/n;

for i=1:n
 y(i)=y(i)-cT;
end

r=zeros(total,1);

for k=1:total
 Dk=D(:,:,k);
% for i=1:n
 multcount=0;
 for j=1:2:multiplicity2
  cRodd=0;
  cReven=0;
%  j
%  multcount
%  j-multcount
  for i=1:n
	%if mod(j,2)==1
	    Ak(i,j)=cos((j-multcount)*pi/180.0.*x(i)); %THE j's ARE WRONG!!!!
            cRodd=cRodd+Ak(i,j);
	%else
	    Ak(i,j+1)=sin((j-multcount)*pi/180.0.*x(i));	
	    cReven=cReven+Ak(i,j+1);
	%end
    %Ak(i,j)=x(i);
  end
  cRodd=cRodd/n;
  cReven=cReven/n;
  for i=1:n
    %if mod(j,2)==1
	Ak(i,j)=Ak(i,j)-cRodd;
    %else
	Ak(i,j+1)=Ak(i,j+1)-cReven;
    %end    
  end
  multcount=multcount+1;   
 end
 
 A(:,:,k)=Ak;

 Bk=Ak'*Ak;

 B(:,:,k)=Bk;

% ck=inv(Bk)*Ak'*y';

 [Q1,R1]=qr(Ak,0);

 ck=inv(R1)*Q1'*y';

 c(:,k)=ck;

 for l1=1:n
  Yk(l1)=0;
  for l2=1:multiplicity2
   Yk(l1)=Yk(l1)+ck(l2).*Ak(l1,l2);
  end
 end 

 Y(:,k)=Yk;

 for p=1:n
  r(k)=r(k)+(y(p)-Yk(p)).*(y(p)-Yk(p));
 end

end

indexcount=1;
for b=1:2:multiplicity2
 forceconst(indexcount)=sqrt(c(b)*c(b)+c(b+1)*c(b+1));
 delta(indexcount)=(180.0/pi).*atan2(c(b+1),c(b));
 indexcount=indexcount+1;
end


for a=1:n
	Ycgff(a)=2.5*(1+cos(1*pi/180.0.*x(a)-pi))+1.5*(1+cos(2*pi/180.0.*x(a)-0))+0.5*(1+cos(3*pi/180.0.*x(a)-0));
    Yfftk(a)=0.483*(1+cos(1*pi/180.0.*x(a)-pi))+1.5020*(1+cos(2*pi/180.0.*x(a)-pi))+1.2920*(1+cos(3*pi/180.0.*x(a)-pi));
end
cTcgff=0;
cTfftk=0;
for i=1:n
 cTcgff=cTcgff+Ycgff(i); 
 cTfftk=cTfftk+Yfftk(i);
end

cTcgff=cTcgff/n;
cTfftk=cTfftk/n;

for i=1:n
 Ycgff(i)=Ycgff(i)-cTcgff;
 Yfftk(i)=Yfftk(i)-cTfftk;
end


%plot(x,y,'+');
%hold on
%plot(x,Ycgff,'*');

%for q=1:total
%  subplot(total/2,2,q);
% plot(x,y,'+')
% hold on 
% plot(x,Y(:,q))
%end

%for q=1:total

Bprime=Ak*c;
B=y';

RMSE=sqrt(mean((Bprime-B).^2));

for q=1:1

	figure(q);
	plot(x,y,'d','MarkerFaceColor',[0 0 1])
	hold on
	plot(x,Y(:,q),'LineWidth',[2.0])
end

saveas(gcf,'0_14_LS3-fit_plot.png')

fileID=fopen('0_14_matlab_output_LS3.txt','w');
fprintf(fileID,'%s\n','force constants LS3:');
fprintf(fileID,'%f\n',forceconst);
fprintf(fileID,'%s\n','delta:');
fprintf(fileID,'%f\n',delta);
fprintf(fileID,'%s\n','RMSE:');
fprintf(fileID,'%f\n',RMSE);
fclose(fileID);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clf;
clear all;

x=importdata('0_10_matlab_sorted_angles_data.txt',',',0);

y=importdata('0_11_matlab_diff_pot_data.txt',',',0);

[m,n]=size(x);

multiplicity = 6;

multiplicity2 = multiplicity*2;

total=1;%2^multiplicity;

r=zeros(total,1);

rows=n;

sum=0;

sign=1;

Da=zeros(1,multiplicity);

for b=0:total-1
for a=0:multiplicity-1
	
	if sign==1
		
		sum=sum+(2^(multiplicity-a)/2);

	else	

		sum=sum-(2^(multiplicity-a)/2);
	
	end

	if sum<=b
		Da(1,multiplicity-1-a+1)=0;
		sign=1;
	
	else
		Da(1,multiplicity-1-a+1)=pi;
		sign=-1;
	end		
	
end
	sum=0;
	sign=1;
	D(:,:,b+1)=Da;
	Da=zeros(1,multiplicity);
end

cT=0;
for i=1:n
 cT=cT+y(i); 
end

cT=cT/n;

for i=1:n
 y(i)=y(i)-cT;
end

r=zeros(total,1);

for k=1:total
 Dk=D(:,:,k);
% for i=1:n
 multcount=0;
 for j=1:2:multiplicity2
  cRodd=0;
  cReven=0;
%  j
%  multcount
%  j-multcount
  for i=1:n
	%if mod(j,2)==1
	    Ak(i,j)=cos((j-multcount)*pi/180.0.*x(i)); %THE j's ARE WRONG!!!!
            cRodd=cRodd+Ak(i,j);
	%else
	    Ak(i,j+1)=sin((j-multcount)*pi/180.0.*x(i));	
	    cReven=cReven+Ak(i,j+1);
	%end
    %Ak(i,j)=x(i);
  end
  cRodd=cRodd/n;
  cReven=cReven/n;
  for i=1:n
    %if mod(j,2)==1
	Ak(i,j)=Ak(i,j)-cRodd;
    %else
	Ak(i,j+1)=Ak(i,j+1)-cReven;
    %end    
  end
  multcount=multcount+1;   
 end
 
 A(:,:,k)=Ak;

 Bk=Ak'*Ak;

 B(:,:,k)=Bk;

% ck=inv(Bk)*Ak'*y';

 [Q1,R1]=qr(Ak,0);

 ck=inv(R1)*Q1'*y';

 c(:,k)=ck;

 for l1=1:n
  Yk(l1)=0;
  for l2=1:multiplicity2
   Yk(l1)=Yk(l1)+ck(l2).*Ak(l1,l2);
  end
 end 

 Y(:,k)=Yk;

 for p=1:n
  r(k)=r(k)+(y(p)-Yk(p)).*(y(p)-Yk(p));
 end

end

indexcount=1;
for b=1:2:multiplicity2
 forceconst(indexcount)=sqrt(c(b)*c(b)+c(b+1)*c(b+1));
 delta(indexcount)=(180.0/pi).*atan2(c(b+1),c(b));
 indexcount=indexcount+1;
end


for a=1:n
	Ycgff(a)=2.5*(1+cos(1*pi/180.0.*x(a)-pi))+1.5*(1+cos(2*pi/180.0.*x(a)-0))+0.5*(1+cos(3*pi/180.0.*x(a)-0));
    Yfftk(a)=0.483*(1+cos(1*pi/180.0.*x(a)-pi))+1.5020*(1+cos(2*pi/180.0.*x(a)-pi))+1.2920*(1+cos(3*pi/180.0.*x(a)-pi));
end
cTcgff=0;
cTfftk=0;
for i=1:n
 cTcgff=cTcgff+Ycgff(i); 
 cTfftk=cTfftk+Yfftk(i);
end

cTcgff=cTcgff/n;
cTfftk=cTfftk/n;

for i=1:n
 Ycgff(i)=Ycgff(i)-cTcgff;
 Yfftk(i)=Yfftk(i)-cTfftk;
end


%plot(x,y,'+');
%hold on
%plot(x,Ycgff,'*');

%for q=1:total
%  subplot(total/2,2,q);
% plot(x,y,'+')
% hold on 
% plot(x,Y(:,q))
%end

%for q=1:total

Bprime=Ak*c;
B=y';

RMSE=sqrt(mean((Bprime-B).^2));

for q=1:1

	figure(q);
	plot(x,y,'d','MarkerFaceColor',[0 0 1])
	hold on
	plot(x,Y(:,q),'LineWidth',[2.0])
end

saveas(gcf,'0_15_LS6-fit_plot.png')

fileID=fopen('0_15_matlab_output_LS6.txt','w');
fprintf(fileID,'%s\n','force constants LS6:');
fprintf(fileID,'%f\n',forceconst);
fprintf(fileID,'%s\n','delta:');
fprintf(fileID,'%f\n',delta);
fprintf(fileID,'%s\n','RMSE:');
fprintf(fileID,'%f\n',RMSE);
fclose(fileID);

exit;



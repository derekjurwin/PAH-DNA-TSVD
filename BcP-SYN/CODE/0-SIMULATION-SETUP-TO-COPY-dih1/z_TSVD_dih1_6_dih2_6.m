clear all;

x=importdata('0_10_matlab_sorted_angles_data_ALT.txt',',',0);
x1=importdata('0_10_matlab_sorted_angles_data_ALT2.txt',',',0);

y=importdata('0_11_matlab_diff_pot_data_ALT.txt',',',0);

[m,n]=size(x);

multiplicity = 6;

multiplicity_a = 6;

multiplicity2 = multiplicity*2;

total=1;%2^multiplicity;

r=zeros(total,1);

rows=n;

for i=1:rows
    x2(i)=x(i);
    %x2(i)=7*(x(i)+180.0);
    %x2(i)=7*(x1(i));
end

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
 multcount=0;
 multcount1=multiplicity2;
 multcount2=multiplicity;
 %for j=1:2:multiplicity2*2
 %for j=1:2:18
 cols=multiplicity*2+multiplicity_a*2;
 for j=1:2:cols
  cRodd=0;
  cReven=0;
  cRodd1=0;
  cReven1=0;
  cRodd2=0;
  cReven2=0;
  cRodd3=0;
  cReven3=0;
  
  for i=1:n
	 if j<=multiplicity2
	    Ak(i,j)=cos((j-multcount)*pi/180.0.*x(i));
            cRodd=cRodd+Ak(i,j);
	    Ak(i,j+1)=sin((j-multcount)*pi/180.0.*x(i));	
	        cReven=cReven+Ak(i,j+1);
            
        Ak2(i,j)=cos((j-multcount)*pi/180.0.*x(i));
            cRodd2=cRodd2+Ak2(i,j);
	    Ak2(i,j+1)=sin((j-multcount)*pi/180.0.*x(i));	
	        cReven2=cReven2+Ak2(i,j+1);
     else
	    Ak(i,j)=cos((j-multcount1)*pi/180.0.*x1(i));
            cRodd1=cRodd1+Ak(i,j);
	    Ak(i,j+1)=sin((j-multcount1)*pi/180.0.*x1(i));	
	        cReven1=cReven1+Ak(i,j+1);
            
        Ak2(i,j)=cos((j-multcount2)*pi/180.0.*x2(i));
            cRodd3=cRodd3+Ak2(i,j);
	    Ak2(i,j+1)=sin((j-multcount2)*pi/180.0.*x2(i));	
	        cReven3=cReven3+Ak2(i,j+1);
        %multcount1
        %j-multcount1
	 end
  end
  cRodd=cRodd/n;
  cReven=cReven/n;
  cRodd1=cRodd1/n;
  cReven1=cReven1/n;
  
  cRodd2=cRodd2/n;
  cReven2=cReven2/n;
  cRodd3=cRodd3/n;
  cReven3=cReven3/n;

  for i=1:n
	  if j<=multiplicity2
	     Ak(i,j)=Ak(i,j)-cRodd;
         Ak(i,j+1)=Ak(i,j+1)-cReven;
         
         Ak2(i,j)=Ak2(i,j)-cRodd2;
         Ak2(i,j+1)=Ak2(i,j+1)-cReven2;
      else
       	 Ak(i,j)=Ak(i,j)-cRodd1;
         Ak(i,j+1)=Ak(i,j+1)-cReven1;
         
         Ak2(i,j)=Ak2(i,j)-cRodd3;
         Ak2(i,j+1)=Ak2(i,j+1)-cReven3;
      end	       
  end
     if j<=multiplicity2
         multcount=multcount+1;
     else
         multcount1=multcount1+1;
     end
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
  %for l2=1:multiplicity2*2
  %for l2=1:18
  for l2=1:cols
   Yk(l1)=Yk(l1)+ck(l2).*Ak(l1,l2);
  end
 end 

 Y(:,k)=Yk;

 for p=1:n
  r(k)=r(k)+(y(p)-Yk(p)).*(y(p)-Yk(p));
 end

end

indexcount=1;
%for b=1:2:multiplicity2*2
%for b=1:2:18
for b=1:2:cols
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

Bprime=Ak*c;
B=y';

RMSE=sqrt(mean((Bprime-B).^2));

[U,S,V]=svd(Ak);

ST=S;

[ms,ns]=size(ST);

trunc_k=0.7; %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

for i=1:ms
	for j=1:ns
	     if ST(i,j)<trunc_k 
	        ST(i,j)=0;
             end
	end
end

rsvd=length(find(diag(S)));
rsvdT=length(find(diag(ST)));

Uhat=U(:,1:rsvd);
UhatT=U(:,1:rsvdT);

Shat=S(1:rsvd,1:rsvd);
ShatT=ST(1:rsvdT,1:rsvdT);

Vhat=V(:,1:rsvd);
VhatT=V(:,1:rsvdT);

zsvd=Shat\Uhat'*y';
zsvdT=ShatT\UhatT'*y';

csvd=V*zsvd;
csvdT=VhatT*zsvdT;


for j=1:16000
    
    lambda_step=0.0005;
    
    %BcP not orthog scan
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %GOOD DON'T CHANGE j=1:1000
    %lambda=0.0170+0.01*j;
    
    %lambda=2.0772;
    
    %GOOD j=1:1000 or 2000
    %lambda=0.0+.01*j;
    
    %BEST j 1:10000
    %lambda=0.0+.002*j;
    
    %PHE parameterization scan
    %BEST w/j=1:12000 & trunc <1.35
    %lambda=0.0+.0015*j;
    
    lambda=0.0+lambda_step*j;
    
    rsvdREG=length(find(diag(S)));

    UhatREG=U(:,1:rsvdREG);

    ShatREG=S(1:rsvd,1:rsvdREG);
        
    %for i=1:18
    for i=1:cols
        ShatREG(i,i)=(ShatREG(i,i)*ShatREG(i,i)+lambda*lambda)/ShatREG(i,i);
    end

    VhatREG=V(:,1:rsvdREG);

    zsvdREG=ShatREG\UhatREG'*y';

    csvdREG=VhatREG*zsvdREG;
    
    soln_norm_matrixREG(j)=norm(csvdREG);
    
    BprimeREG=Ak*csvdREG;
    B1REG=y';
    
    B1_0=Ak*csvd;
    
    %res_norm_matrixREG(j)=norm(B1REG-BprimeREG);
    res_norm_matrixREG(j)=norm(B1_0-BprimeREG);
    
    indexcount=1;
    %for b=1:2:multiplicity2*2
    %for b=1:2:18    
    for b=1:2:cols
        forceconstREG(indexcount)=sqrt(csvdREG(b)*csvdREG(b)+csvdREG(b+1)*csvdREG(b+1));
        deltaREG(indexcount)=(180.0/pi).*atan2(csvdREG(b+1),csvdREG(b));
        indexcount=indexcount+1;
    end
    
    forceconstREG;    
    
    reg_iterations=j;
end



%for i=18:-1:1
for i=cols:-1:1
    S_trunc=S;
    
    %for j=18:-1:i
    for j=cols:-1:i
        S_trunc(j,j)=0;        
    end
    
    S_trunc;
    
    rsvdT1=length(find(diag(S_trunc)));

    UhatT1=U(:,1:rsvdT1);

    ShatT1=S_trunc(1:rsvdT1,1:rsvdT1);

    VhatT1=V(:,1:rsvdT1);

    zsvdT1=ShatT1\UhatT1'*y';

    csvdT1=VhatT1*zsvdT1;
    
    soln_norm_matrix(cols+1-i)=norm(csvdT1);
    %soln_norm_matrix(19-i)=norm(csvdT1);
    
    BprimeSVDT1=Ak*csvdT1;
    B1=y';
    
    B1_0=Ak*csvd;
    
    %res_norm_matrix(19-i)=norm(B1-BprimeSVDT1);
    %res_norm_matrix(19-i)=norm(B1_0-BprimeSVDT1);
    res_norm_matrix(cols+1-i)=norm(B1_0-BprimeSVDT1);
    
    indexcount=1;
    %for b=1:2:multiplicity2*2
    %for b=1:2:18    
    for b=1:2:cols
        forceconstsvdT1(indexcount)=sqrt(csvdT1(b)*csvdT1(b)+csvdT1(b+1)*csvdT1(b+1));
        deltasvdT1(indexcount)=(180.0/pi).*atan2(csvdT1(b+1),csvdT1(b));
        indexcount=indexcount+1;
    end
    
    forceconstsvdT1;
end

indexcount=1;
%for b=1:2:multiplicity2*2
%for b=1:2:18    
for b=1:2:cols
 forceconstsvd(indexcount)=sqrt(csvd(b)*csvd(b)+csvd(b+1)*csvd(b+1));
 deltasvd(indexcount)=(180.0/pi).*atan2(csvd(b+1),csvd(b));
 indexcount=indexcount+1;
end

indexcount=1;
%for b=1:2:multiplicity2*2
%for b=1:2:18    
for b=1:2:cols
 forceconstsvdT(indexcount)=sqrt(csvdT(b)*csvdT(b)+csvdT(b+1)*csvdT(b+1));
 deltasvdT(indexcount)=(180.0/pi).*atan2(csvdT(b+1),csvdT(b));
 indexcount=indexcount+1;
end

BprimeSVD=Ak*csvd;
B=y';

RMSEsvd=sqrt(mean((BprimeSVD-B).^2));

BprimeSVDT=Ak*csvdT;
B=y';

RMSEsvdT=sqrt(mean((BprimeSVDT-B).^2));


%for q=1:1
%
%	figure(q);
%	plot(x,y,'d','MarkerFaceColor',[0 0 1]);
%	hold on
%	plot(x,Y(:,q),'LineWidth',[2.0]);
%end
%saveas(gcf,'0_16_ill-conditioned-fit_plot-2.png')

fileID=fopen('0_14_matlab_output_SVD-T.txt','w');
fprintf(fileID,'%s\n','force constants SVD-T:');
fprintf(fileID,'%f\n',forceconstsvdT);
fprintf(fileID,'%s\n','delta:');
fprintf(fileID,'%f\n',deltasvdT);
fprintf(fileID,'%s\n','RMSE:');
fprintf(fileID,'%f\n',RMSEsvdT);
fclose(fileID);

%for i=1:17
for i=1:cols-1
    gaps(i)=S(i+1,i+1)/S(i,i);
end

%for i=1:18
for i=1:cols
    crit(i)=S(1,1)/S(i,i);
end

beta_decay=abs(Uhat'*y')';

%for i=1:18
for i=1:cols
    sigma_decay(i)=S(i,i);
    DPC(i)=beta_decay(i)/S(i,i);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    lambda1= 3.3194;
    
    rsvdREG1=length(find(diag(S)));

    UhatREG1=U(:,1:rsvdREG1);

    ShatREG1=S(1:rsvd,1:rsvdREG1);
        
    %for i=1:18
    for i=1:cols
        ShatREG1(i,i)=(ShatREG1(i,i)*ShatREG1(i,i)+lambda1*lambda1)/ShatREG1(i,i);
    end

    VhatREG1=V(:,1:rsvdREG1);

    zsvdREG1=ShatREG1\UhatREG1'*y';

    csvdREG1=VhatREG1*zsvdREG1;
    
    soln_norm_matrixREG1(j)=norm(csvdREG1);
    
    BprimeREG1=Ak*csvdREG1;
    B1REG1=y';
    
    B1_0=Ak*csvd;
    
    %res_norm_matrixREG(j)=norm(B1REG-BprimeREG);
    res_norm_matrixREG1(j)=norm(B1_0-BprimeREG);
    
    indexcount=1;
    %for b=1:2:multiplicity2*2
    %for b=1:2:18    
    for b=1:2:cols
        forceconstREG1(indexcount)=sqrt(csvdREG1(b)*csvdREG1(b)+csvdREG1(b+1)*csvdREG1(b+1));
        deltaREG1(indexcount)=(180.0/pi).*atan2(csvdREG1(b+1),csvdREG1(b));
        indexcount=indexcount+1;
    end
    
BprimeREG1=Ak*csvdREG1;
B=y';

RMSEREG1=sqrt(mean((BprimeREG1-B).^2));
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    lambda2= 1.8936;
    
    rsvdREG2=length(find(diag(S)));

    UhatREG2=U(:,1:rsvdREG2);

    ShatREG2=S(1:rsvd,1:rsvdREG2);
        
    %for i=1:18
    for i=1:cols
        ShatREG2(i,i)=(ShatREG2(i,i)*ShatREG2(i,i)+lambda2*lambda2)/ShatREG2(i,i);
    end

    VhatREG2=V(:,1:rsvdREG2);

    zsvdREG2=ShatREG2\UhatREG2'*y';

    csvdREG2=VhatREG2*zsvdREG2;
    
    soln_norm_matrixREG2(j)=norm(csvdREG2);
    
    BprimeREG2=Ak*csvdREG2;
    B1REG2=y';
    
    B1_0=Ak*csvd;
    
    %res_norm_matrixREG(j)=norm(B1REG-BprimeREG);
    res_norm_matrixREG2(j)=norm(B1_0-BprimeREG);
    
    indexcount=1;
    %for b=1:2:multiplicity2*2
    %for b=1:2:18    
    for b=1:2:cols
        forceconstREG2(indexcount)=sqrt(csvdREG2(b)*csvdREG2(b)+csvdREG2(b+1)*csvdREG2(b+1));
        deltaREG2(indexcount)=(180.0/pi).*atan2(csvdREG2(b+1),csvdREG2(b));
        indexcount=indexcount+1;
    end
    
BprimeREG2=Ak*csvdREG2;
B=y';

RMSEREG2=sqrt(mean((BprimeREG2-B).^2));
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


figure(1)
%plot(res_norm_matrixREG,soln_norm_matrixREG,'d','MarkerFaceColor',[0 0 1])
plot(log(res_norm_matrixREG),log(soln_norm_matrixREG))
%plot(res_norm_matrixREG,soln_norm_matrixREG)

hold on

plot(log(res_norm_matrix),log(soln_norm_matrix),'d','MarkerFaceColor',[0 0 1])
%plot(res_norm_matrix,soln_norm_matrix,'d','MarkerFaceColor',[0 0 1])

figure(2)
%plot(DPC,'d','MarkerFaceColor',[0 0 1])
%hold on
%plot(sigma_decay)

plot(log(DPC),'d','MarkerFaceColor',[0 0 1])
hold on
plot(log(sigma_decay))

lambda

fileID=fopen('0_20_decay.txt','w');
fprintf(fileID,'%s\n','**truncation k:');
fprintf(fileID,'%f\n',trunc_k);
fprintf(fileID,'%s\n','**sigma decay:');
fprintf(fileID,'%f\n',sigma_decay);
fprintf(fileID,'%s\n','**DPC:');
fprintf(fileID,'%f\n',DPC);
fclose(fileID);

fileID=fopen('0_21_reg_norms.txt','w');
fprintf(fileID,'%s\n','**lambda step:');
fprintf(fileID,'%f\n',lambda_step);
fprintf(fileID,'%s\n','**reg iterations:');
fprintf(fileID,'%f\n',reg_iterations);
fprintf(fileID,'%s\n','**final lambda:');
fprintf(fileID,'%f\n',lambda);
fprintf(fileID,'%s\n','**res norm:');
fprintf(fileID,'%f\n',res_norm_matrixREG);
fprintf(fileID,'%s\n','**soln norm:');
fprintf(fileID,'%f\n',soln_norm_matrixREG);
fclose(fileID);

fileID=fopen('0_22_trunc_norms.txt','w');
fprintf(fileID,'%s\n','**res norm:');
fprintf(fileID,'%f\n',res_norm_matrix);
fprintf(fileID,'%s\n','**soln norm:');
fprintf(fileID,'%f\n',soln_norm_matrix);
fclose(fileID);

fileID=fopen('0_23_matlab_output_SVD-T.txt','w');
fprintf(fileID,'%s\n','**force constants SVD-T:');
fprintf(fileID,'%f\n',forceconstsvdT);
fprintf(fileID,'%s\n','**delta:');
fprintf(fileID,'%f\n',deltasvdT);
fprintf(fileID,'%s\n','**RMSE:');
fprintf(fileID,'%f\n',RMSEsvdT);
fclose(fileID);

fileID=fopen('0_23_matlab_output_REG1.txt','w');
fprintf(fileID,'%s\n','**force constants REG:');
fprintf(fileID,'%f\n',forceconstREG1);
fprintf(fileID,'%s\n','**delta:');
fprintf(fileID,'%f\n',deltaREG1);
fprintf(fileID,'%s\n','**RMSE:');
fprintf(fileID,'%f\n',RMSEREG1);
fprintf(fileID,'%s\n','**lambda:');
fprintf(fileID,'%f\n',lambda1);
fclose(fileID);

fileID=fopen('0_23_matlab_output_REG2.txt','w');
fprintf(fileID,'%s\n','**force constants REG:');
fprintf(fileID,'%f\n',forceconstREG2);
fprintf(fileID,'%s\n','**delta:');
fprintf(fileID,'%f\n',deltaREG2);
fprintf(fileID,'%s\n','**RMSE:');
fprintf(fileID,'%f\n',RMSEREG2);
fprintf(fileID,'%s\n','**lambda:');
fprintf(fileID,'%f\n',lambda2);
fclose(fileID);

fileID=fopen('0_24_gaps_crit.txt','w');
fprintf(fileID,'%s\n','**gaps:');
fprintf(fileID,'%f\n',gaps);
fprintf(fileID,'%s\n','**critical cond:');
fprintf(fileID,'%f\n',crit);
fclose(fileID);


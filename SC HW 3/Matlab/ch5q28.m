function [ output ] = ch5q28()
%Part c/d

x = [1900,1910,1920,1930,1940,1950,1960,1970,1980,1990,2000,2010];
% x = linspace(1900,2010,12);
y = [76.21,92.23,106.0,123.2,132.2,151.3,179.3,203.3,226.5,248.8,281.4,308.7];
[m,n] = size(x);

V = Vandermonde(x);
a = V\y(1:n)';
output = a;


%Calculating pn(xi) using Vandermonde Coefficients
s = ones(n,2);
s(:,1) = s(:,1)*a(1);
for i = 1:n
    for j = 2:n
        s(i,1) = s(i,1) + a(j)*x(i)^(j-1);
    end
end

%Calculating pn(zi) where each z is the corresponding scaled x value
alpha = (x(n)+x(1))/2;
beta = (x(n)-x(1))/2;
z = (x-alpha)/beta;

Vz = Vandermonde(z);
az = Vz\y(1:n)';
s(:,2) = s(:,2)*az(1);
for i = 1:n
    for j = 2:n
        s(i,2) = s(i,2) + az(j)*z(i)^(j-1);
    end
end

%Compute the Lagrange Polynomial (for reference)
p = zeros(n,1);
for i = 1:n
    px = 0;
    lagrangeCoefficient = ell(x(i),x);
    for j = 1:n
        px = px + y(j)*lagrangeCoefficient(j);
    end
    p(i) = px;
end


plot(x,y(1:n)); %Plot (x,y)
hold on;
scatter(x,p); %Scatter Lagrange
plot(x,s(:,1)); %Plot Direct
scatter(x,s(:,2),'+'); %Scatter Scaled Direct
scatter(x,s(:,1),'k.'); %Scatter Direct
legend('Population Curve','Lagrange Interp @ x','Direct Interp @ x','Scaled Interp @ x','Location','Northwest');
hold off;
end


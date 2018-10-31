function [ output ] = ch5q33()
n = 30;

x = linspace(0,1,n);
h = x(2)-x(1);
y = cos(6*pi*x);

nx = 100;
interpPoints = linspace(1e-06,1,nx);
w = zeros(1,nx);
a = y;
b = zeros(1,n);
c = zeros(1,n);

b(1) = -sin(6*pi*x(1))*6*pi;
c(1) = (y(2)-y(1)-(h*b(1)))/(h^2);


for i=2:n-1
    b(i) = -b(i-1) + 2*(y(i)-y(i-1))/h;
    c(i) = (y(i+1) - y(i) - h*b(i))/(h^2);
end
    
for i=1:nx
    j = ceil(interpPoints(i)/h);
    w(i) = a(j) + b(j)*(interpPoints(i)-x(j)) + c(j)*(interpPoints(i)-x(j))^2;
end

plot(x,y);
hold on
plot(interpPoints,w);
legend('cos(6pix)','Interpolated Function','Location','Southwest')
title('n=30')
hold off
end


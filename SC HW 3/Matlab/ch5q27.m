function [output] = ch5q27()

h = pi/20;
nx = 3;
x = linspace(0,40*pi/20,41);
[sinx,y] = cosPiTwenty(41);
% [sinx,y] = cosPiEights(17);

[m,n] = size(x);

s = zeros(1,nx);
%extrapolate points 1.0 outside of range to illustrate behavior at end points
% interpolationPoints = linspace(x(1),x(n),nx);
interpolationPoints = [1,2,5];

n = n-1;
B = zeros(1,n+3);

%%%%Compute the Natural Cubic Spline
% Calculate ai's
A = tridiag(4,1,n-1);
z = zeros(n-1,1);
z(1) = 6*y(2)-y(1);
z(n-1) = 6*y(n)-y(n+1);
for k = 2:n-2
    z(k) = 6*y(k+1);
end

%a is incremented to reflect 1-indexing, not zero
a = zeros(1,n+3);
% a(1) & a(n+1)
a(2) = y(1);
a(n+2) = y(n+1);
%  Solve for middle ai's using Thomas Algorithm

a(3:n+1) = Thomas(A,z);
%  a(0) & a(n+2)
% a(1) = 2*a(2)-a(3);
% a(n+3) = 2*a(n+2)-a(n+1);
a(1) = -sinx(1)*2*h+a(3);
a(n+3) = sinx(n+1)*2*h+a(n+1);

xx = zeros(n+3,1);
xx(2:n+2) = x;
xx(1) = xx(2)-h;
xx(n+3) = xx(n+2)+h;

for i = 1:nx
%     disp(i)
    val = 0;
    for j = 1:n+3
        %Calculate Bi
        cx = (interpolationPoints(i)-xx(j))/h;
        
        if (abs(cx) < 1)
            B(j) = (2/3)-(cx^2)*(1-(.5*abs(cx)));
        elseif (abs(cx) < 2)
            B(j) = ((2-abs(cx))^3)/6;
        else
            B(j) = 0;
        end
%          fprintf('Compare i=%d with j=%d.. cx=%d giving B(%d)=%d \n',interpolationPoints(i),xx(j),abs(cx),j,B(j)) 
        val = val + a(j)*B(j);
    end
%     fprintf('\n')
    s(i) = val;
end

output = s';
% size(x)
% size(y)
% size(interpolationPoints)
% size(s)
% 
plot(x,y);
hold on
scatter(interpolationPoints,s,'k')
% legend('x','interp');
hold off
end


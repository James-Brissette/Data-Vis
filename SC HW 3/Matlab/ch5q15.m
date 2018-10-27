function [ output_args ] = ch5q15()
%ch5q15
%   Detailed explanation goes here
x = linspace(0,24,13);
[m,n] = size(x);
y = [59,56,53,54,60,67,72,74,75,74,70,65,61];

nx = 1000;
%extrapolate points .2 outside of range to illustrate behavior at end points
interpolationPoints = linspace(x(1)-.2,x(n)+.2,nx);

p = zeros(nx,1);

%Compute the Lagrange Polynomial
for i = 1:nx
    px = 0;
    lagrangeCoefficient = ell(interpolationPoints(i),x);
    for j = 1:n
        px = px + y(j)*lagrangeCoefficient(j);
    end
    p(i) = px;
end





scatter(x,y,'ko');
hold on
plot(x,y,'r',interpolationPoints,p,'b');
legend('Temperature Data','Tempature Curve','Langrange Interpolation Function','Location','northwest');
axis([-2,27,50,82]);
hold off

end


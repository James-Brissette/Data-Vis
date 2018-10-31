function [ output ] = ch5q15()
%ch5q15
x = linspace(0,24,13);
[m,n] = size(x);
y = [59,56,53,54,60,67,72,74,75,74,70,65,61];

nx = 25+9; %Adding 9 to evaluate at 9am the next day
interpolationPoints = linspace(x(1),x(n)+9,nx);

%p is the output using the interpolation polynomial
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

hold on

output = zeros(nx,2);
output(:,1) = p;
scatter(x,y,'ko');
plot(x,y,'r',interpolationPoints,p,'b');
%The CubicSpline was handled seperately
output(:,2) = CubicSpline(x,y,nx);
hold off
legend('Temperature Data','Tempature Curve','Langrange Interpolation Function','Cubic Spline','Location','northwest');
axis([-2,27,50,82]);

end


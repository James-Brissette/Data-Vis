function [ output ] = CubicSpline()

x = linspace(0,24,13);
h = x(2)-x(1);
[m,n] = size(x);
y = [59,56,53,54,60,67,72,74,75,74,70,65,61];

A = tridiag(a,b,n-2);
nx = 10;
%extrapolate points .2 outside of range to illustrate behavior at end points
interpolationPoints = linspace(x(1)-.2,x(n)+.2,nx);
B = zeros(n,1);
%Compute the Natural Cubic Spline
for i = 1:nx
    
    for j = 1:n
        %Calculate Bi
        cx = (interpolationPoints(i)-x(j))/h;
        if (abs(cx) <= 1)
            B(j) = (2/3)-(cx^2)*(1-(.5*abs(cx)));
        elseif (abs(cx) > 1 && (abs(cx) < 2))
            B(j) = ((2-abs(cx))^3)/6;
        else
            B(j) = 0;
        end
        
        %Calculate ai
    end
end

end


function [output] = ch2q6(x0,alpha)
tol = 1e-16;
error = 1e10;
x = x0;
while abs(error) > tol
    f = x^2 - alpha;
    fp = 2*x;
    x = x - (f / fp);
    error = 0 - (x^2 - alpha)
end
output = x;
end


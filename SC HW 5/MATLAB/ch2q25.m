function [output] = ch2q25(x0)
tol = 1e-16;
error = 1e10;
x = x0;
while abs(error) > tol
    f = (1-exp(-10*x))/(1+exp(-10*x));
    fp = 20*exp(10*x)/(exp(10*x)+1)^2;
    x = x - (f / fp);
    error = 0 - (1-exp(-10*x))/(1+exp(-10*x))
end
output = x;
end
function [output] = ch6q8()
% Solves for h using the trapezoidal rule
x = 2;
IT = 0;

erf2 = 0.995322265;

error = 1;
n = 200000;
while abs(error) > 10e-7
% while n < 10
    h = x/n;
%     fprintf('N = %d; Step size is %d; ',n, h);
    IT = (.5*exp(0) + .5*(1/exp((2)^2)));
%     fprintf('Intermediate eval at ');
    for i = 1:n-1
        IT = IT + (1/ exp((i*h)^2));
%         fprintf('x = %d; ',(i)*h);
    end
    IT = IT * h;
    error = erf2 - IT
    n = n+1;
end
end


function [error] = ch6q8b(n)
% Solves for h using the trapezoidal rule
a = 0;
b = 2;
x = linspace(a,b,n+1);
h = x(3)-x(2);

trueError = 0.995322265;

IT = f(x);
IT(1) = .5*IT(1);
IT(n+1) = .5*IT(n+1);
IT = IT*h;

error = abs(trueError - sum(IT));

end

function y=f(x)
    y = 2/sqrt(pi).*exp(-x.*x);
end

function [error] = ch6q8d(n)
% Solves for h using Simpson's rule
a = 0;
b = 2;
x = linspace(a,b,n+1);
h = x(3)-x(2);

trueError = 0.995322265;
c = ones(1,n+1);

for i=2:n
    if mod(i,2)==0 
        c(i) = 4;
    else
        c(i) = 2;
    end
end

IT = f(x);
IT = c.*IT;
IT = IT*h/3;

error = abs(trueError - sum(IT));

end

function y=f(x)
    y = 2/sqrt(pi).*exp(-x.*x);
end

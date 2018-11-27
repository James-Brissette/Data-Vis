function [output] = ch2q21()
a = -1;
b = 0;
c = (a+b)/2;

tol = 1e-16;
error = 1e10;

while abs(error) > tol
    if (a^3 + 3*a + 1)*(c^3 + 3*c + 1) < 0
        b = c;
    else
        a = c;
    end
    c = (a + b)/2;
    error = 0 - (c^3 + 3*c + 1);
end
output = c;
end

function [s,c] = cosPiEights(nx)
%Calculate the exact value of cos from 0 to nx*pi/8 in pi/8 steps

c = ones(1,nx);
s = zeros(1,nx);
%start indexing at 2 so output = [0,pi/8,2pi/8,...]
s(2) = sqrt(2-sqrt(2))/2;
c(2) = sqrt(2+sqrt(2))/2;

for i=2:nx-1
    c(i+1) = c(2)*c(i)-s(2)*s(i);
    s(i+1) = s(2)*c(i)+c(2)*s(i);
end

end


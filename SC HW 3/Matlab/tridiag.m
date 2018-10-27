function [ output ] = tridiag(a,b,n)
%UNTITLED5 Summary of this function goes here
%   Detailed explanation goes here

output = zeros(n);
output(1,1) = a;
for i = 2:n
    output(i,i) = a;
    output(i-1,i) = b;
    output(i,i-1) = b;
end          

end


function [out] = Vandermonde(x)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
[m,n] = size(x);
out = zeros(n);
out(:,1) = 1;
for i=2:n
    out(:,i) = x.^(i-1);
end

end


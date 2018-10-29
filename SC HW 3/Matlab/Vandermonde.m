function [out] = Vandermonde(x)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
[m,n] = size(x);
out = zeros(n+1);
out(:,1) = 1;
for i=2:n+1
    out(:,i) = x.^(i-1);
end

end


function [out] = Vandermonde(x)

[m,n] = size(x);
out = zeros(n);
out(:,1) = 1;
for i=2:n
    out(:,i) = x.^(i-1);
end

end


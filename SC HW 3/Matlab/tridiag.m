function [ output ] = tridiag(a,b,n)
%Creates an nxn tridiagonal matrix with 'a' along the main diagonal

output = zeros(n);
output(1,1) = a;
for i = 2:n
    output(i,i) = a;
    output(i-1,i) = b;
    output(i,i-1) = b;
end          

end


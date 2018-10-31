function [x] = Thomas(A,z)
%Thomas Algorithm
%   For solving tridiagonal matrices as given in Table 3.6
[m,n] = size(A);
x = zeros(n,1);
v = zeros(n,1);
w = A(1,1);
x(1) = z(1)/w;

for i = 2:n
    v(i) = A(i-1,i)/w;
    w = A(i,i)-A(i,i-1)*v(i);
    x(i) = (z(i)-A(i,i-1)*x(i-1))/w;
end

for j = (n-1):-1:1
    x(j) = x(j)-v(j+1)*x(j+1);
end

end


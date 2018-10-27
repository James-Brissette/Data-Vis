function [out,out2] = ch4q22(n)

%Value used to shift
omega = 4;
%Setup matrix A based on input n
A =  zeros(n);
for k=2:n
    A(k-1,k) = (k-1) / sqrt((2*(k-1) - 1)*(2*(k-1) + 1));
    A(k,k-1) = A(k-1,k);
end
disp(A)
As = A - omega*eye(n);

%Randomly select B and calculate preliminary eigenvalues
B = rand(n,n);
Q = GS(B);
eigenvals = zeros(n,1);

eigenvec = Q(:,1);
eigenval = dot(eigenvec, A*eigenvec) / dot(eigenvec, eigenvec);

%Run orthogonal iteration until condition satisfied
iterativeErr = 10000;
while abs(iterativeErr) > 1e-12
    B = As*Q;
    Q = GS(B);
    
    e = eigenval;
    eigenvec = Q(:,1);
    eigenval = dot(eigenvec, As*eigenvec) / dot(eigenvec, eigenvec);
    
    iterativeErr = e - eigenval;
end

%Compute eigenvalues
for k=1:n
    eigenvec = Q(:,k);
    eigenval = dot(eigenvec, As*eigenvec) / dot(eigenvec, eigenvec);
    eigenvals(k) = eigenval + omega;
end

w = zeros(n,1);
for k=1:n
    eigenvec = Q(:,k);
    w(k) = 2*eigenvec(k,1)^2
end

out = eigenvals;
out2 = w
end


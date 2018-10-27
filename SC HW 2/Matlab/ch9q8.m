function [out] = ch9q8()

len1 = 2000;
len2 = 20000;
len3 = 200000;

x1 = rand(2,len1);
x2 = rand(2,len2);
x3 = rand(2,len3);

%n=2000
x1a = @() summation(x1,len1);
time_x1a = timeit(x1a);

x1b = @() centersum(x1,len1);
time_x1b = timeit(x1b);

x1c = @() cstars(x1,len1);
time_x1c = timeit(x1c);

x1d = @() callCov(x1,len1);
time_x1d = timeit(x1d);


%n=20000
x2a = @() summation(x2,len2);
time_x2a = timeit(x2a);

x2b = @() centersum(x2,len2);
time_x2b = timeit(x2b);

x2c = @() cstars(x2,len2);
time_x2c = timeit(x2c);

x2d = @() callCov(x2,len2);
time_x2d = timeit(x2d);


%n=200000
x3a = @() summation(x3,len3);
time_x3a = timeit(x3a);

x3b = @() centersum(x3,len3);
time_x3b = timeit(x3b);

x3c = @() cstars(x3,len3);
time_x3c = timeit(x3c);

x3d = @() callCov(x3,len3);
time_x3d = timeit(x3d);

disp('Times:')
disp('Part A, n=2000')
disp(time_x1a)
disp('Part B, n=2000')
disp(time_x1b)
disp('Part C, n=2000')
disp(time_x1c)
disp('Part D, n=2000')
disp(time_x1d)
disp('%%%%%%%%%%%%%%%%%%%%%%%')
disp('Part A, n=20000')
disp(time_x2a)
disp('Part B, n=20000')
disp(time_x2b)
disp('Part C, n=20000')
disp(time_x2c)
disp('Part D, n=20000')
disp(time_x2d)
disp('%%%%%%%%%%%%%%%%%%%%%%%')
disp('Part A, n=200000')
disp(time_x3a)
disp('Part B, n=200000')
disp(time_x3b)
disp('Part C, n=200000')
disp(time_x3c)
disp('Part D, n=200000')
disp(time_x3d)
end

function [out] = calculateCenter(in)
    [m,n] = size(in);
    out = in;
    avg = mean(out);
    for k=1:n
        out(:,k) = out(:,k) - avg(k);
    end
end

function summation(x,n)

xc = calculateCenter(x);
B = zeros(2,2);
for k=1:n
    vec = xc(:,k);
    B = B + (vec*vec');
end
B = B / n;
end

function centersum(x,n)

xc = calculateCenter(x);
B = (xc*xc')/n;

end

function cstars(x,n)

xc = calculateCenter(x);
cstar1 = xc(1,:)';
cstar2 = xc(2,:)';

B = dot(cstar1,cstar2)/n;

end

function callCov(x,n)

xc = calculateCenter(x);
B = cov(xc');

end
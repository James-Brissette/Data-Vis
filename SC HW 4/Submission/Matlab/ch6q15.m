function [ output ] = ch6q15(n)

x = linspace(0,3,n);
v = zeros(n,1);
y = zeros(n,1);
a = sin(x.^4);
h = 3/n;

for i=1:n-1
    v(i+1) = v(i)+.5*h*(a(i)+a(i+1));
    y(i+1) = y(i)+.5*h*(v(i)+v(i+1));
end

trueVal = 0.72732289075 - y(n)
% plot(x,a);
hold on;
% plot(x,v);
plot(x,y);
% legend('a(r)','v(r)','y(r)','Location','Southwest')
hold off;
end


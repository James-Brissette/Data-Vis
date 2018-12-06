function [ output ] = ch6q15c()

n = 10;
x = linspace(0,3,n);
v = zeros(2,1);
y = zeros(2,1);
a = zeros(2,1);

trueVal = 0.72732289075;

while abs(trueVal - y(2)) > 10e-9
    
    h = 3/n;
    a(1) = sin(0);
    a(2) = sin((h)^4);
    for i=1:n-1
        v(2) = v(1)+.5*h*(a(1)+a(2));
        y(2) = y(1)+.5*h*(v(1)+v(2));
        
        t = (i)/h;
        a(1) = a(2);
        a(2) = sin(t^4);
        
        v(1) = v(2);
        y(1) = y(2);
    end
    
    error = abs(trueVal - y(2))
    
end

% % plot(x,a);
% hold on;
% % plot(x,v);
% plot(x,y);
% % legend('a(r)','v(r)','y(r)','Location','Southwest')
% hold off;
% end
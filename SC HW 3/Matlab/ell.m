function [coefficients] = ell(interp, xs)
[m,n] = size(xs);
coefficients = zeros(n,1);

for i=1:n
    val = 1;
    for j=1:n;
        if (i == j)
            continue
        end
        val = val * (interp - xs(j)) / (xs(i)-xs(j));
    end
    coefficients(i) = val;
end
end
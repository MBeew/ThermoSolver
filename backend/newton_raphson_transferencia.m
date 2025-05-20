function [x_critico, iteraciones, contador] = newton_raphson_transferencia(T0, Tamb, Tcrit, k, x0, tol, max_iter)
% Define la función f(x): diferencia entre T(x) y Tcrit
f = @(x) Tamb + (T0 - Tamb) * exp(-k * x) - Tcrit;
% Derivada de f(x)
df = @(x) -k * (T0 - Tamb) * exp(-k * x);

iter = 0;
iteraciones = [];

while iter < max_iter
    fx = f(x0);
    dfx = df(x0);

    if abs(dfx) < 1e-10
        warning('Derivada cercana a cero. El método puede fallar.');
        break;
    end

    x1 = x0 - fx / dfx;
    iteraciones = [iteraciones; iter, x0, fx];

    if abs(x1 - x0) < tol
        x_critico = x1;
        contador = iter + 1;
        return;
    end

    x0 = x1;
    iter = iter + 1;
end

x_critico = NaN;
contador = iter;

function [root, iteraciones, contador] = newton_raphson(f_expr, x0, tol, max_iter)
  f = str2func(['@(x) ' f_expr]);
  df = @(x) (f(x + 1e-6) - f(x)) / 1e-6;

  iter = 0;
  iteraciones = [];
  
  while iter < max_iter
    fx = f(x0);
    dfx = df(x0);
    if dfx == 0
      break;
    end
    
    x1 = x0 - fx/dfx;
    
    iteraciones = [iteraciones; iter, x0, fx];
    
    if abs(x1 - x0) < tol
      root = x1;
      contador = iter + 1; % total iteraciones realizadas
      return
    end
    
    x0 = x1;
    iter = iter + 1;
  end
  
  root = NaN;
  contador = iter;
end

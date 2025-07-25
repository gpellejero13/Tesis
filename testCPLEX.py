from docplex.mp.model import Model
from docplex.mp.model import Model
from docplex.mp.context import Context

context = Context.make_default_context()
context.solver.log_output = True  # Muestra logs del solver

mdl = Model(name="forzar_cplex", context=context)

# Variables
x = mdl.continuous_var(name='x')
y = mdl.continuous_var(name='y')

# Restricciones
mdl.add_constraint(x + 2 * y <= 20)
mdl.add_constraint(3 * x - y >= 0)
mdl.add_constraint(x - y <= 5)

# Función objetivo
mdl.maximize(5 * x + 3 * y)

# Resolver
solucion = mdl.solve()

# Mostrar resultados
if solucion:
    print(f"x = {x.solution_value}")
    print(f"y = {y.solution_value}")
    print(f"Valor óptimo = {mdl.objective_value}")
else:
    print("No se encontró solución")



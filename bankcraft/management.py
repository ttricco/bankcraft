from model import Model
from utils import visualization as vis
model = Model()


df = model.run(10)
model.run(10)
vis.draw_graph(model)
vis.draw_interactive_grid()

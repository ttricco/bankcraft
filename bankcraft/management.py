from model import Model
import visualization as vis

model = Model()


df = model.run(10)
vis.draw_graph(model)


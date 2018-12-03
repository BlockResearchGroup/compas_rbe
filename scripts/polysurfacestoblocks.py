import compas
import compas_rhino
import compas_rbe

from compas_rbe.datastructures import Assembly

guids = compas_rhino.select_surfaces()
assembly = Assembly.from_polysurfaces(guids)

assembly.to_json(compas_rbe.get('curve_components.json'))

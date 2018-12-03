import compas
import compas_rhino
import compas_rbe

from compas_rbe.datastructures import Assembly

guids = compas_rhino.select_meshes()
assembly = Assembly.from_meshes(guids)

assembly.to_json(compas_rbe.get('gene_vault_blocks.json'))

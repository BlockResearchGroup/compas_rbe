from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import i_to_blue
from compas.utilities import i_to_red

from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import length_vector
from compas.geometry import sum_vectors

import compas_rhino

from compas_assembly.rhino import BlockArtist
from compas_assembly.rhino import AssemblyArtist


__all__ = ['AssemblyArtist', 'BlockArtist']


class AssemblyArtist(AssemblyArtist):
    """An artist for visualisation of assemblies inn Rhino.

    Parameters
    ----------
    assembly : compas_rbe.datastructures.Assembly
        The assembly data structure.
    layer : str, optional
        The base layer for drawing.
        Default is ``None``, which means drawing in the current layer.

    Examples
    --------
    .. code-block:: python

        pass

    """

    def __init__(self, assembly, layer=None):
        super(AssemblyArtist, self).__init__(assembly, layer=layer)
        self.defaults.update({
            'color.vertex': (0, 0, 0),
            'color.vertex:is_support': (255, 0, 0),
            'color.edge': (0, 0, 0),
            'color.interface': (255, 255, 255),
            'color.force:compression': (0, 0, 255),
            'color.force:tension': (255, 0, 0),
            'color.force:friction': (255, 165, 0),
            'color.selfweight': (0, 255, 0),
            'scale.force': 0.1,
            'scale.selfweight': 0.1,
            'scale.friction': 0.1,
            'eps.selfweight': 1e-3,
            'eps.force': 1e-3,
            'eps.friction': 1e-3,
            'range.friction': 5,
        })

    def clear_frictions(self):
        self.clear_('friction')

    def clear_forces(self):
        self.clear_('force')

    def draw_frictions(self, scale=None, eps=None, mode=0):
        """Draw the contact frictions at the interfaces.

        Parameters
        ----------
        scale : float, optional
            The scale at which the forces should be drawn.
            Default is `0.1`.
        eps : float, optional
            A tolerance for drawing small force vectors.
            Force vectors with a scaled length smaller than this tolerance are not drawn.
            Default is `1e-3`.
        mode : int, optional
            Display mode: 0 normal, 1 resultant forces
            Default is 0

        Notes
        -----
        * Forces are drawn as lines with arrow heads.
        * Forces are drawn on a sub-layer *Frictions* of the base layer, if a base layer was specified.
        * Forces are named according to the following pattern:
          ``"{assembly_name}.friction.{from block}-{to block}.{interface point}"``

        """
        layer = "{}::Frictions".format(self.layer) if self.layer else None
        scale = scale or self.defaults['scale.friction']
        eps = eps or self.defaults['eps.friction']
        color_friction = self.defaults['color.force:friction']

        lines = []
        resultant_lines = []

        for a, b, attr in self.assembly.edges(True):
            if attr['interface_forces'] is None:
                continue

            u, v = attr['interface_uvw'][0], attr['interface_uvw'][1]

            forces = []

            for i in range(len(attr['interface_points'])):
                sp = attr['interface_points'][i]
                fr_u_unit = attr['interface_forces'][i]['c_u']
                fr_v_unit = attr['interface_forces'][i]['c_v']

                fr_u = scale_vector(u, fr_u_unit)
                fr_v = scale_vector(v, fr_v_unit)
                f = add_vectors(fr_u, fr_v)
                f_l = length_vector(f)

                if f_l > 0.0:
                    if scale * f_l < eps:
                        continue
                    color = color_friction
                else:
                    continue

                f = scale_vector(f, scale)

                lines.append({
                    'start' : sp,
                    'end'   : [sp[axis] + f[axis] for axis in range(3)],
                    'color' : color,
                    'name'  : "{0}.friction.{1}-{2}.{3}".format(self.assembly.name, a, b, i),
                    'arrow' : 'end'
                })

                if mode == 1:
                    forces.append(f)

            if mode == 0:
                continue

            resultant_force = sum_vectors(forces)

            if len(forces) == 0:
                continue

            resultant_pt = sum_vectors([
                scale_vector(attr['interface_points'][i], (
                    length_vector(forces[i]) / length_vector(resultant_force)))
                for i in range(len(attr['interface_points']))
            ])

            resultant_lines.append({
                'start' : resultant_pt,
                'end'   : [resultant_pt[axis] + resultant_force[axis] for axis in range(3)],
                'color' : color,
                'name'  : "{0}.resultant-friction.{1}-{2}.{3}".format(self.assembly.name, a, b, i),
                'arrow' : 'end'
            })

        if mode == 0:
            compas_rhino.xdraw_lines(
                lines, layer=layer, clear=False, redraw=False)
        else:
            compas_rhino.xdraw_lines(
                resultant_lines, layer=layer, clear=False, redraw=False)

    def draw_forces(self, scale=None, eps=None, mode=0):
        """Draw the contact forces at the interfaces.

        Parameters
        ----------
        scale : float, optional
            The scale at which the forces should be drawn.
            Default is `0.1`.
        eps : float, optional
            A tolerance for drawing small force vectors.
            Force vectors with a scaled length smaller than this tolerance are not drawn.
            Default is `1e-3`.
        mode : int, optional
            Display mode: 0 normal, 1 resultant forces
            Default is 0

        Notes
        -----
        * Forces are drawn as lines with arrow heads.
        * Forces are drawn on a sub-layer *Forces* of the base layer, if a base layer was specified.
        * At every interface point there can be a *compression* force (blue) and a *tension* force (red).
        * Forces are named according to the following pattern:
          ``"{assembly_name}.force.{from block}-{to block}.{interface point}"``

        """
        layer = "{}::Forces".format(self.layer) if self.layer else None
        scale = scale or self.defaults['scale.force']
        eps = eps or self.defaults['eps.force']
        color_compression = self.defaults['color.force:compression']
        color_tension = self.defaults['color.force:tension']

        lines = []
        resultant_lines = []

        for a, b, attr in self.assembly.edges(True):
            if attr['interface_forces'] is None:
                continue

            w = attr['interface_uvw'][2]

            forces = []

            for i in range(len(attr['interface_points'])):
                sp = attr['interface_points'][i]
                c = attr['interface_forces'][i]['c_np']
                t = attr['interface_forces'][i]['c_nn']

                f = c - t

                if f > 0.0:
                    if scale * f < eps:
                        continue
                    color = color_compression
                elif f < 0.0:
                    if -scale * f < eps:
                        continue
                    color = color_tension
                else:
                    continue

                lines.append({
                    'start' : sp,
                    'end'   : [sp[axis] + scale * f * w[axis] for axis in range(3)],
                    'color' : color,
                    'name'  : "{0}.force.{1}-{2}.{3}".format(self.assembly.name, a, b, i),
                    'arrow' : 'end'
                })

                if mode == 1:
                    forces.append([scale * f * w[axis] for axis in range(3)])

            if mode == 0:
                continue

            resultant_force = sum_vectors(forces)

            if len(forces) == 0:
                continue

            resultant_pt = sum_vectors([
                scale_vector(attr['interface_points'][i], (
                    length_vector(forces[i]) / length_vector(resultant_force)))
                for i in range(len(attr['interface_points']))
            ])

            resultant_lines.append({
                'start' : resultant_pt,
                'end'   : [resultant_pt[axis] + resultant_force[axis] for axis in range(3)],
                'color' : color,
                'name'  : "{0}.resultant-friction.{1}-{2}.{3}".format(self.assembly.name, a, b, i),
                'arrow' : 'end'
            })

        if mode == 0:
            compas_rhino.xdraw_lines(
                lines, layer=layer, clear=False, redraw=False)
        else:
            compas_rhino.xdraw_lines(
                resultant_lines, layer=layer, clear=False, redraw=False)

    def color_interfaces(self, mode=0):
        """Color the interfaces with shades of blue and red according to the forces at the corners.

        Parameters
        ----------
        mode : int, optional
            Mode to switch between normal forces(0) and frictions(1)
            Default is 0.

        Notes
        -----
        * Currently only normal forces are taken into account.
        * Gradients should go from blue to red over white.
        * White marks the neutral line (the axis of rotational equilibrium).
        * ...

        Examples
        --------
        .. code-block:: python

            pass

        """
        if mode == 0:
            # redraw the faces with a discretisation that makes sense for the neutral axis
            # color the drawn meshes
            for u, v, attr in self.assembly.edges(True):
                if attr['interface_forces'] is None:
                    continue

                name = "{}.interface.{}-{}".format(self.assembly.name, u, v)
                guids = compas_rhino.get_objects(name=name)
                if not guids:
                    continue

                guid = guids[0]

                forces = [f['c_np'] - f['c_nn'] for f in attr['interface_forces']]

                fmin = min(forces)
                fmax = max(forces)
                fmax = max(abs(fmin), fmax)

                colors = []

                p = len(attr['interface_points'])

                for i in range(p):
                    f = forces[i]

                    if f > 0.0:
                        color = i_to_blue(f / fmax)
                    elif f < 0.0:
                        color = i_to_red(-f / fmax)
                    else:
                        color = (255, 255, 255)

                    colors.append(color)

                # this is obviously not correct
                # just a visual reminder
                if p > 4:
                    colors.append((255, 255, 255))

                compas_rhino.set_mesh_vertex_colors(guid, colors)

        elif mode == 1:
            for u, v, attr in self.assembly.edges(True):
                if attr['interface_forces'] is None:
                    continue

                name = "{}.interface.{}-{}".format(self.assembly.name, u, v)
                guids = compas_rhino.get_objects(name=name)
                if not guids:
                    continue

                guid = guids[0]

                iu, iv = attr['interface_uvw'][0], attr['interface_uvw'][1]

                forces = [length_vector(add_vectors(scale_vector(iu, f['c_u']), scale_vector(iv, f['c_v'])))
                          for f in attr['interface_forces']]

                fmin = min(forces)
                fmax = max(forces)
                fmax = max(abs(fmin), fmax)
                fmax = max(fmax, self.defaults['range.friction'])

                colors = []

                p = len(attr['interface_points'])

                for i in range(p):
                    f = forces[i]

                    if f > 0.0:
                        color = i_to_red(f / fmax)
                    else:
                        color = (255, 255, 255)

                    colors.append(color)

                # this is obviously not correct
                # just a visual reminder
                if p > 4:
                    colors.append((255, 255, 255))

                compas_rhino.set_mesh_vertex_colors(guid, colors)

        else:
            print("please choose mode 0 or 1")


class BlockArtist(BlockArtist):
    """An artist for painting RBE blocks."""

    def __init__(self, *args, **kwargs):
        super(BlockArtist, self).__init__(*args, **kwargs)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass

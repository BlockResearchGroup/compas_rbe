from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import sys
import os
import json

import compas
from rui import *

HERE = os.path.abspath(os.path.dirname(__file__))


__all__ = []


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from frontcontroller import RBEFrontController as RBE

    with open(os.path.join(HERE, 'rui_config.json'), 'r') as fo:
        config = json.load(fo)

    macros  = get_macros(RBE, RBE.instancename)

    init_script = [
        '-_RunPythonScript ResetEngine (',
        'import rhinoscriptsyntax as rs;',
        'import sys;',
        'import os;',
        'path = rs.ToolbarCollectionPath(\'{}\');'.format(RBE.instancename),
        'path = os.path.dirname(path);',
        'sys.path.insert(0, path);',
        'from {} import {};'.format('frontcontroller', RBE.__name__),
        '{} = {}();'.format(RBE.instancename, RBE.__name__),
        '{}.init();'.format(RBE.instancename),
        ')'
    ]

    for macro in macros:
        if macro['name'] == '{}.init'.format(RBE.instancename):
            macro['script'] = ' '.join(init_script)

    rui = Rui('./{}.rui'.format(RBE.instancename))

    rui.init()
    rui.add_macros(macros)

    for toolbar in config['toolbars']:
        for item in toolbar['items']:
            itype = item.get('type')
            if itype == 'separator':
                continue
            if 'text' in item:
                name = item['left']
                element = rui.macros[name]
                element.find('button_text/locale_1033').text = item['text']

    rui.add_menus(config['menus'])
    rui.add_toolbars(config['toolbars'])
    rui.add_toolbargroups(config['toolbargroups'])

    rui.write()

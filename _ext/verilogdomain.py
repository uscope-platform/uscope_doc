import re
import copy

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.roles import XRefRole
from sphinx.locale import l_, _
from sphinx.domains import Domain, ObjType, Index
from sphinx.directives import ObjectDescription
from sphinx.util.nodes import make_refnode
from sphinx.util.docfields import Field, GroupedField, TypedField


re_dir = re.compile(r'..\s?vlog:(.*?)\:\s*(.*)')

class VerilogObject(ObjectDescription):
    """
    Description of a general Ruby object.
    """
    has_content = True
    option_spec = {
        'noindex': directives.flag
    }

    doc_field_types = [
        TypedField('parameter', label=l_('Parameters'),
                   names=('param', 'parameter'),
                   typerolename='param', typenames=('param')),
        TypedField('port', label=l_('Ports'), rolename='obj',
                   names=('port'),
                   typerolename='port', typenames=('port',)),
        TypedField('interface', label=l_('Interfaces'), rolename='obj',
                   names=('interface'),
                   typerolename='interface', typenames=('interface',))
    ]

    def get_signature_prefix(self, sig):
        """
        May return a prefix to put before the object name in the signature.
        """
        return ''

    def get_signature_postfix(self, sig):
        return ''

    def handle_signature(self, sig, signode):
        self.clearTmpData  = False
        if self.objtype == 'endmodule':
            '''
            mod_content = self.env.temp_data.get('vlog:top_level_module').children[1]
            
            sections = []
            for idx, val in enumerate(mod_content.children):
                if val.attributes.get('objtype') == 'sect':
                    sections.append((idx, copy.deepcopy(val)))
            for i in sections:
                title_text = i[1].children[0].rawsource
                sect = addnodes.nodes.section()
                inner_sect = addnodes.nodes.section()
                title = addnodes.nodes.title(title_text,title_text)
                inner_sect += title
                inner_sect += i[1].children[1].children
                inner_sect['ids'] = title_text + '-inner_sect'
                sect += inner_sect
                mod_content.children[i[0]] = sect
            self.clearTmpData  = True
            raise ValueError
            '''
        else:
            self.current_module = self.env.temp_data.get('vlog:current_module')
            node = signode
            signode['objtype'] = self.objtype

            prefix = self.get_signature_prefix(sig) + ' '
            if prefix is not ' ':
                node += addnodes.desc_type(prefix,prefix)

            if self.current_module is None:
                self.env.temp_data['vlog:top_level_module'] = signode.parent
            else:
                signode['module'] = self.current_module
            if self.objtype != ('sect'):
                node += addnodes.desc_name(sig, sig)

            postfix = ' ' + self.get_signature_postfix(sig)
            if postfix is not ' ':
                node += addnodes.desc_type(postfix,postfix)  


        return {'type': self.objtype, 'index':sig}


    def add_target_and_index(self, name_cls, sig, signode):
        signode['ids'].append(sig)
        if name_cls['type'] == 'module':
            signode['names'] = [name_cls]
        if name_cls['type'] != 'endmodule':          
            self.env.domaindata['vlog'][name_cls['type']+'_store'][name_cls['index']] = name_cls['type']
        
            

    def before_content(self):
        # needed for automatic qualification of members (reset in subclasses)
        pass

    def after_content(self):
        pass
            


class VerilogModule(VerilogObject):
    """
    Description of an object on module level (functions, data).
    """

    def get_signature_prefix(self, sig):
        return f'{self.objtype} '

    def before_content(self):
        VerilogObject.before_content(self)
        if self.names:
            self.env.temp_data['vlog:current_module'] = self.names[0]['index']

class VerilogPort(VerilogObject):
    option_spec = {
        'direction': directives.unchanged,
        'width': directives.unchanged
    }

    def get_signature_prefix(self, sig):
        direction = self.options.get("direction")
        if direction:
            return direction
        else:
            return ''

    def get_signature_postfix(self, sig):
        width = self.options.get("width")
        if width:
            return f'[ {width} ]'
        else:
            return ''

class VerilogInterface(VerilogObject):
    option_spec = {
        'modport': directives.unchanged,
        'type': directives.unchanged
    }

    def get_signature_prefix(self, sig):
        modport = self.options.get("modport")
        if_type = self.options.get("type")
        if modport and if_type:
            return modport.replace(' ', '') + '.' + if_type
        elif modport:
            return modport
        else:
            return ''

class VerilogParam(VerilogObject): pass

class VerilogStructuralElement(VerilogObject):
    def after_content(self):
        if(self.clearTmpData):
            self.env.temp_data['vlog:current_module'] = None
            self.env.temp_data['vlog:top_level_module'] = None
            self.env.temp_data['vlog:sect'] = None
            self.current_module = None
            self.clearTmpData  = False




class VerilogDomain(Domain):
    """Ruby language domain."""
    name = 'vlog'
    label = 'Verilog'

    object_types = {
        'module': ObjType('module', 'mod', 'obj'),
        'port': ObjType('port', 'mod', 'obj'),
        'param': ObjType('param', 'mod', 'obj'),
        'interface':ObjType('interface', 'mod', 'obj'),
    }

    directives = {
        'module':  VerilogModule,
        'port':    VerilogPort,
        'param': VerilogParam,
        'interface': VerilogInterface,
        'sect': VerilogStructuralElement,
        'endmodule': VerilogStructuralElement
    }

    initial_data = {
        'module_store': {},
        'port_store': {},
        'param_store': {},
        'sect_store': {},
        'interface_store':{}
    }

    def clear_doc(self, docname):
        pass

    def get_objects(self):
        return[]

    def process_doc(self, env, docname,document):
        """Add section titles."""
        sections = set(self._find_sections(document.children))
        if sections:
            for i in sections:
                content = i.children[1]
                title_text = i.children[0].rawsource
                sect = addnodes.nodes.section()
                inner_sect = addnodes.nodes.section()
                title = addnodes.nodes.title(title_text,title_text)
                inner_sect += title
                inner_sect += content
                inner_sect['ids'] = title_text + '-inner_sect'
                sect += inner_sect
                i.children = []
                i += sect



    def _find_sections(self, nodes):
        sections_parents = []
        for i in nodes:
            if i.children:
                for j in i.children:
                    try:
                        if j.attributes.get('objtype') == 'sect' and j.parent.tagname == 'desc':
                            sections_parents.append(j.parent)
                        elif j.children:
                            sections_parents.extend(self._find_sections(i))
                    except AttributeError:
                        pass
        return sections_parents
                    


def setup(app):
    app.add_domain(VerilogDomain)


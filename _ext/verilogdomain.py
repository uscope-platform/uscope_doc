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

def _iteritems(d):
    for k in d:
        yield k, d[k]

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

    def needs_arglist(self):
        """
        May return true if an empty argument list is to be generated even if
        the document contains none.
        """
        return False

    def handle_signature(self, sig, signode):
        self.clearTmpData  = False
        content = None
        if self.objtype == 'endmodule':
            mod_content = self.env.temp_data.get('vlog:top_level_module').children[1]
            
            sections = []
            for idx, val in enumerate(mod_content.children):
                if val.attributes.get('objtype') == 'sectbegin':
                    sections.append((idx, copy.deepcopy(val)))
            for i in sections:
                title_text = i[1].children[0].rawsource
                sect = addnodes.nodes.section()
                inner_sect = addnodes.nodes.section()
                title = addnodes.nodes.title(title_text,title_text)
                inner_sect += title
                inner_sect += i[1]
                inner_sect['ids'] = title_text + '-inner_sect'
                sect += inner_sect
                mod_content.children[i[0]] = sect
            self.clearTmpData  = True

        else:
            self.current_module = self.env.temp_data.get('vlog:current_module')
            node = signode
            signode['objtype'] = self.objtype

            prefix = self.get_signature_prefix(sig)
            if prefix is not '':
                node += addnodes.desc_annotation(prefix,prefix)
                
            if self.current_module is None:
                self.env.temp_data['vlog:top_level_module'] = signode.parent
            else:
                signode['module'] = self.current_module
            if self.objtype != ('sectbegin'):
                node += addnodes.desc_name(sig, sig)

       

    def get_index_text(self, modname, name):
        """
        Return the text for the index entry of the object.
        """
        raise NotImplementedError('must be implemented in subclasses')

    def _is_class_member(self):
        return self.objtype.endswith('method') or self.objtype.startswith('attr')

    def add_target_and_index(self, name_cls, sig, signode):
        if sig not in self.state.document.ids:
            signode['names'].append(sig)
            signode['ids'].append(sig)

        if self.objtype == 'module':
            signode['names'] = [sig]
            self.state.document.note_explicit_target(signode)
            objects = self.env.domaindata['vlog']['modules']
            objects['last_module'] = sig


    def before_content(self):
        # needed for automatic qualification of members (reset in subclasses)
        pass

    def after_content(self):
        if self.clearTmpData:

            self.env.temp_data['vlog:current_module'] = None
            self.env.temp_data['vlog:top_level_module'] = None
            self.env.temp_data['vlog:sect'] = None
            self.current_module = None
            self.clearTmpData  = False


class VerilogModule(VerilogObject):
    """
    Description of an object on module level (functions, data).
    """

    def get_signature_prefix(self, sig):
        return f'{self.objtype} '

    def needs_arglist(self):
        return self.objtype == 'function'

    def get_index_text(self, modname, name_cls):
        if self.objtype == 'function':
            if not modname:
                return _('%s() (global function)') % name_cls[0]
            return _('%s() (module function in %s)') % (name_cls[0], modname)
        else:
            return ''

    def before_content(self):
        VerilogObject.before_content(self)
        if self.names:
            self.env.temp_data['vlog:current_module'] = self.env.domaindata['vlog']['modules']['last_module']

class VerilogPort(VerilogObject):
    """
    Description of an object on module level (functions, data).
    """

    def needs_arglist(self):
        return self.objtype == 'port'

    def get_index_text(self, modname, name_cls):
        if self.objtype == 'port':
            if not modname:
                return _('%s() (global function)') % name_cls[0]
            return _('%s() (module function in %s)') % (name_cls[0], modname)
        else:
            return ''


class VerilogXRefRole(XRefRole):
    def process_link(self, env, refnode, has_explicit_title, title, target):
        if not has_explicit_title:
            title = title.lstrip('.')   # only has a meaning for the target
            title = title.lstrip('#')
            if title.startswith("::"):
                title = title[2:]
            target = target.lstrip('~') # only has a meaning for the title
            # if the first character is a tilde, don't display the module/class
            # parts of the contents
            if title[0:1] == '~':
                m = re.search(r"(?:\.)?(?:#)?(?:::)?(.*)\Z", title)
                if m:
                    title = m.group(1)
        if not title.startswith("$"):
            refnode['rb:module'] = env.temp_data.get('rb:module')
            refnode['rb:class'] = env.temp_data.get('rb:class')
        # if the first character is a dot, search more specific namespaces first
        # else search builtins first
        if target[0:1] == '.':
            target = target[1:]
            refnode['refspecific'] = True
        return title, target


class VerilogModuleIndex(Index):
    """
    Index subclass to provide the Ruby module index.
    """

    name = 'modindex'
    localname = l_('Ruby Module Index')
    shortname = l_('modules')

    def generate(self, docnames=None):
        content = {}
        # list of prefixes to ignore
        ignores = self.domain.env.config['modindex_common_prefix']
        ignores = sorted(ignores, key=len, reverse=True)
        # list of all modules, sorted by module name
        modules = sorted(_iteritems(self.domain.data['modules']),
                         key=lambda x: x[0].lower())
        # sort out collapsable modules
        prev_modname = ''
        num_toplevels = 0
        for modname, (docname, synopsis, platforms, deprecated) in modules:
            if docnames and docname not in docnames:
                continue

            for ignore in ignores:
                if modname.startswith(ignore):
                    modname = modname[len(ignore):]
                    stripped = ignore
                    break
            else:
                stripped = ''

            # we stripped the whole module name?
            if not modname:
                modname, stripped = stripped, ''

            entries = content.setdefault(modname[0].lower(), [])

            package = modname.split('::')[0]
            if package != modname:
                # it's a submodule
                if prev_modname == package:
                    # first submodule - make parent a group head
                    entries[-1][1] = 1
                elif not prev_modname.startswith(package):
                    # submodule without parent in list, add dummy entry
                    entries.append([stripped + package, 1, '', '', '', '', ''])
                subtype = 2
            else:
                num_toplevels += 1
                subtype = 0

            qualifier = deprecated and _('Deprecated') or ''
            entries.append([stripped + modname, subtype, docname,
                            'module-' + stripped + modname, platforms,
                            qualifier, synopsis])
            prev_modname = modname

        # apply heuristics when to collapse modindex at page load:
        # only collapse if number of toplevel modules is larger than
        # number of submodules
        collapse = len(modules) - num_toplevels < num_toplevels

        # sort by first letter
        content = sorted(_iteritems(content))

        return content, collapse


class VerilogDomain(Domain):
    """Ruby language domain."""
    name = 'vlog'
    label = 'Verilog'

    object_types = {
        'module': ObjType('module', 'mod', 'obj'),
        'port': ObjType('Port', 'mod', 'obj')
    }

    directives = {
        'module':  VerilogModule,
        'port':    VerilogPort,
        'sectbegin': VerilogPort,
        'sectend': VerilogPort,
        'endmodule': VerilogPort
    }

    roles = {
        'mod':  VerilogXRefRole(),
        'port': VerilogXRefRole()

    }
    initial_data = {
        'modules': {},  # modname -> docname, synopsis, platform, deprecated
        'ports': {},
    }

    def clear_doc(self, docname):
        a = 0
        pass
        #for modname, (fn, _, _, _) in list(self.data['modules'].items()):
        #    if fn == docname:
        #        del self.data['modules'][modname]

    def resolve_xref(self, env, fromdocname, builder,
                     typ, target, node, contnode):
        return None

    def get_objects(self):
        for modname, info in _iteritems(self.data['modules']):
            yield (modname, modname, 'module', info[0], 'module-' + modname, 0)


def setup(app):
    app.add_domain(VerilogDomain)


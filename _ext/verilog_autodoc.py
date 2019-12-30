
from sphinx.ext.autodoc import Documenter
from sphinx.ext.autodoc.directive import AutodocDirective, DummyOptionSpec, parse_generated_content
from sphinx.ext.autodoc.directive import process_documenter_options, DocumenterBridge
from sphinx import version_info


class VerilogDocumenter(Documenter):

    domain = 'vlog'
    
    def parse_name(self): 
        a = 0

    
    def import_object(self): 
        a = 0


    def add_content(self, more_content, no_docstring = False): 
        a = 0


    def get_object_members(self, want_all): 
        a = 0


    def filter_members(self, members, want_all): 
        a = 0

    def document_members(self, all_members = False):
        a = 0


    def generate(self, more_content=None, real_modname=None, check_module=False, all_members=False): 
        if not self.parse_name():
            # need a module to import
            self.directive.warn(
                'don\'t know which module to import for autodocumenting '
                '%r (try placing a "module" or "currentmodule" directive '
                'in the document, or giving an explicit module name)'
                % self.name)
            return

        # now, import the module and get object to document
        if not self.import_object():
            return


class VerilogModuleDocumenter(VerilogDocumenter): pass


class VerilogAutodocDirective(AutodocDirective):

    option_spec = DummyOptionSpec()
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        a=0

        reporter = self.state.document.reporter

        try:
            source, lineno = reporter.get_source_and_line(self.lineno)  # type: ignore
        except AttributeError:
            source, lineno = (None, None)
        
        objtype = self.name.replace('auto', '')  # Removes auto
        doccls = self.env.app.registry.documenters[objtype]

        # process the options with the selected documenter's option_spec
        try:
            documenter_options = process_documenter_options(doccls, self.config, self.options)
        except (KeyError, ValueError, TypeError) as exc:
            return []

        if version_info[0] >= 2:
            params = DocumenterBridge(self.env, reporter, documenter_options, lineno, self.state)
        else:
            params = DocumenterBridge(self.env, reporter, documenter_options, lineno)
        documenter = doccls(params, self.arguments[0])
        documenter.generate(more_content=self.content)
        if not params.result:
            return []


        # record all filenames as dependencies -- this will at least
        # partially make automatic invalidation possible
        for fn in params.filename_set:
            self.state.document.settings.record_dependencies.add(fn)

        result = parse_generated_content(self.state, params.result, documenter)
        return result



        #    CALL ORDER:
        #
        #    1 run (autodocdirective)   grabs all the relevant bits and bobs, instantiate the documenter and then calls generate, once the docstring is extracted the source is then fed to the directives (somehow) to get translated into nodes
        #      2 generate (Documenter) immediately calls parse name, then 
        #        3 parse_name
        #          3.5 resolve_name   this function goes from the directive argument to absolute paths and shit (deals with default paths and stuff like that)
        #        4 import_object
        #        5 add_content
        #        6 document_member
        #          7 filter member
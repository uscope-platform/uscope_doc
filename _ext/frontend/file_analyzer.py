from hdlConvertor.language import Language
from hdlConvertor import HdlConvertor
from hdlConvertor import hdlAst

from frontend.modules_extractor import ModulesExtractor


class FileAnalyzer:
    def __init__(self, sources, include_sources):
        c = HdlConvertor()
        self._content = c.parse(sources, Language.SYSTEM_VERILOG_2017, include_sources, hierarchyOnly=False, debug=True)

        self._extractor = ModulesExtractor()


    def get_modules_definitions(self):
        modules = {}

        for i in self._content.objs:
            if type(i) is hdlAst.HdlModuleDec:
                modules = {**self._extractor.extract(i), **modules}

        return modules

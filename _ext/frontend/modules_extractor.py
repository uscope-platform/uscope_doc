from hdlConvertor import hdlAst
import math


class ModulesExtractor:

    def __init__(self):
        self.operations = ['ADD', 'SUB', 'MUL', 'DIV', '$clog2']

    def hdlInt2int(self, integer):
        return int(integer.val, integer.base)

    def extract(self, module):
        ret_val = {module.name: {}}

        ret_val[module.name]['params'] = []
        for i in module.params:
            ret_val[module.name]['params'].append(self.process_param(i))

        ret_val[module.name]['ports'] = []
        for i in module.ports:
            port = self.process_port(i, ret_val[module.name]['params'])
            ret_val[module.name]['ports'].append(port)

        return ret_val

    def process_port(self, port, params):
        if type(port.type) is hdlAst.HdlName:
            return self.process_single_io(port)
        elif type(port.type) is hdlAst.HdlCall and port.type.fn.name == 'INDEX':
            return self.process_bus(port, params)
        elif type(port.type) is hdlAst.HdlCall and port.type.fn.name == 'DOT':
            return self.process_interface(port)
        else:
            ValueError('Unknown port type', port)

    def process_single_io(self, io):
        ret_val = {'name': io.name,
                   'direction': io.direction.name,
                   'type': io.type}
        return ret_val

    def process_interface(self, interface):
        ret_val = {'name': interface.name,
                   'type': ('interface', interface.type.ops[0]),
                   'modport': interface.type.ops[1]}
        return ret_val

    def extract_signed(self, port_type):
        if type(port_type) is hdlAst.HdlCall:
            if port_type.ops[0] == 'signed':
                return True
            else:
                return False
        else:
            if port_type.val == 0:
                return False
            else:
                return True

    def extract_length(self, first, second, params):

        if type(first) is hdlAst.HdlIntValue:
            fb = self.hdlInt2int(first)
        else:
            bound_stack = self.parse_math_expr(first)
            purged_stack = self.subst_params(bound_stack, params)
            fb = self.execute_expr(purged_stack)

        if type(second) is hdlAst.HdlIntValue:
            sb = self.hdlInt2int(second)
        else:
            bound_stack = self.parse_math_expr(second)
            purged_stack = self.subst_params(bound_stack, params)
            sb = self.execute_expr(purged_stack)

        length = abs(fb-sb)+1
        return length

    # TODO: add support for parentheses
    # parse mathematical expression using a modified shunting yard algorithm,
    # the support for functions (like $clog2) is special cased
    def parse_math_expr(self, expr):

        operator = expr.fn.name
        if operator is 'CALL':
            operands_stack = []
            first_op = expr.ops[1]
            if type(first_op) is hdlAst.HdlName:
                operands_stack.append(first_op)
            elif type(first_op.ops[0]) is hdlAst.HdlCall:
                first_op = self.parse_math_expr(first_op)
                operands_stack.extend(first_op)
            else:
                operands_stack.append(self.hdlInt2int(first_op))

            operands_stack.append(str(expr.ops[0]))
        else:

            operands_stack = []

            first_op = expr.ops[0]
            if type(first_op) is hdlAst.HdlCall:
                first_op = self.parse_math_expr(first_op)
                operands_stack.extend(first_op)
            elif type(first_op) is hdlAst.HdlName:
                operands_stack.append(first_op)
            else:
                operands_stack.append(self.hdlInt2int(first_op))

            second_op = expr.ops[1]
            if type(second_op) is hdlAst.HdlCall:
                second_op = self.parse_math_expr(second_op)
                operands_stack.extend(second_op)
            elif type(second_op) is hdlAst.HdlName:
                operands_stack.append(second_op)
            else:
                operands_stack.append(self.hdlInt2int(second_op))

            operands_stack.append(operator)

        return operands_stack

    # Substitute verilog parameters with default value
    def subst_params(self, operands, params):
        new_operands = []
        for i in operands:
            if type(i) != int and i not in self.operations:
                for j in params:
                    if i == j['name']:
                        new_operands.append(j['value'])
            else:
                new_operands.append(i)
        return new_operands

    def execute_expr(self, expr):
        stack = []
        for token in expr:
            if token in self.operations:
                if token == 'ADD':
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a+b)
                elif token == 'SUB':
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a-b)
                elif token == 'MUL':
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a*b)
                elif token == 'DIV':
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a/b)
                elif token == '$clog2':
                    a = stack.pop()
                    stack.append(math.ceil(math.log2(a)))
            else:
                stack.append(token)
        return stack.pop()

    def process_bus(self, bus, params):
        ret_val = {'name': bus.name, 'direction': bus.direction.name}

        if type(bus.type.ops[0]) is hdlAst.HdlName:
            ret_val['type'] = bus.type.ops[0]
            ret_val['signed'] = False
        else:
            ret_val['type'] = bus.type.ops[0].ops[0]
            ret_val['signed'] = self.extract_signed(bus.type.ops[0].ops[1])

        bounds = bus.type.ops[1].ops
        ret_val['lenght'] = self.extract_length(bounds[0], bounds[1], params)

        return ret_val

    def process_param(self, param):
        ret_val = {}
        if type(param.value) is str:
            ret_val['name'] = param.name
            ret_val['value'] = param.name
        elif type(param.value) is hdlAst.HdlIntValue:
            ret_val['name'] = param.name
            ret_val['value'] = self.hdlInt2int(param.value)
        return ret_val

from lark import Transformer, Tree, lexer, Token, Discard
from lark.visitors import Discard
import os, glob


class TreeProcessor(Transformer):

    def start(self, node):
        ret_val = []
        for i in node:
            if i != 'comp_directive':
                ret_val.append(i)
        return ret_val

    def module_def(self, node):
        ret_val = {}
        ret_val['type'] = 'module'
        ret_val['name'] = node[0]
        ret_val['params'] = []
        ret_val['ports'] = []
        ret_val['interfaces'] = []

        for i in node[1:]:
            if i != 'comment' and i:
                if i['type'] == 'param':
                    ret_val['params'].append(i)
                elif i['type'] == 'port':
                    ret_val['ports'].append(i)
                elif i['type'] == 'interface':
                    ret_val['interfaces'].append(i)

        return ret_val

    def module_content(self, node):
        ret_val = []
        for i in node:
            ret_val.append(i)

    def compiler_directive(self, node): 
        raise Discard

    def module_inst(self, node):
        ret_val = {}
        ret_val['type'] = node[0]
        ret_val['name'] = node[1]
        ret_val['connections'] = []
        for i in node[2:]:
            ret_val['connections'].append(i)
        return ret_val

    def module_port_con(self, node):
        if node and node is not[]:
            if node[0] =='comment':
                raise Discard
            elif node[0] == None:
                raise Discard
            return {'port':node[0],'signal':node[1]}
        
    def module_param_con(self, node):
        return {'param':node[0],'signal':node[1]}

    def bus(self, node):
        return {'type':'port', 'name':node[3], 'range':node[2] , 'signal_type': node[1], 'direction': node[0]}

    def interface(self, node):
        return {'type':'interface', 'signal_type': node[0], 'modport':node[1], 'name':node[2]}

    def port(self, node):
        return {'type':'port', 'name':node[2], 'signal_type': node[1], 'direction': node[0]}

    def port_direction(self, node):
        return node[0].value


    def parameter_def(self, node):
        return {'type': 'param', 'name':node[0], 'value': node[1]}

    def standalone_parameter_def(self, node):
        return node

    def definitions(self, node):
       return node

    def signal_definition(self, node):
        processed_nodes = []
        for i  in node[1]:
            tmp = i
            tmp['type'] = node[0]
            processed_nodes.append(tmp)
        return processed_nodes


    def net_decl_list(self, node):
        in_nodes = node
        if node[0].get('type') == 'dimensions':
            dim = node[0]
            del dim['type']
            in_nodes[1]['dimensions'] = dim
            del in_nodes[0]
        else:
            return node
        return node

    def packed_net_decl(self, node):
        if len(node) == 2:
            return {'packed': True, "name": node[0], "initial_value": node[1]}
        else:
            return {'packed': True, "name": node[0], "initial_value": None}

    def unpacked_net_decl(self, node):
        if len(node) == 2:
            return {'packed': False, "name": node[0], "initial_value": node[1]}
        else:
            return {'packed': False, "name": node[0], "initial_value": None}
        pass

    def unpacked_net_initialization(self, node):
        return node

    def signal_type(self, node):
        return node[0].value

    def simple_cont_assignment(self, node):
        raise Discard

    def defparam(self, node):
        if len(node) == 4:
            return {'module': node[0], 'parameter': node[1],'range':node[2] ,'value':node[3]}    
        return {'module': node[0], 'parameter': node[1], 'value':node[2]}

    def bus_dim_spec(self, node):
        if len(node) == 1:
            return{'type': 'dimensions', 'single_bit':True, 'first_bound': node[0]}
        else:
            return{'type': 'dimensions', 'single_bit':False, 'first_bound': node[0], 'second_bound': node[1]}

    def bus_dim_inst(self, node):
        if len(node) == 1:
            return{'type': 'dimensions', 'single_bit':True, 'first_bound': node[0]}
        else:
            return{'type': 'dimensions', 'single_bit':False, 'first_bound': node[0], 'second_bound': node[1]}

    def integer(self, node):
        
        cur_type = node[0]
        ret_val = []

        for i in node[1:]:
            ret_val.append({'type': cur_type, 'name': i})
        
        return ret_val

    def int_number(self,node):
        return int(node[0].value)

    def integer_decl(self, node):
        return node

    def integer_type(self, node):
        return node[0].value

    def intint_number(self, node):
        return int(node[0].value)

    def vlog_number_hex(self, node):
        if len(node) == 2:
            return int(node[1].value,16)
        else:
            return int(node[1].value,16)

    def vlog_number_dec(self, node):
        if len(node) == 3:
            return int(node[0] + node[2].value,10)
        return int(node[1].value,10)

    def vlog_number_oct(self, node):
        return int(node[1].value,8)

    def vlog_number_bin(self, node):
        return int(node[1].value,2)

    def vlog_auto_hex(self,node):
        return int(node[0].value,16)
    def vlog_auto_dec(self,node):
        return int(node[0].value,10)
    def vlog_auto_oct(self,node):
        return int(node[0].value,8)
    def vlog_auto_bin(self,node):
        return int(node[0].value,2)

    def line_comment(self, node):
        if node:
            comment = node[0].value
            if ":vlog" in comment:
                return comment
            else:
                raise Discard

    def bus_expression(self, node):
        return node[0].value

    def expression(self, node):
        return node[0]

    def simple_identifier(self,node):
        return node[0].value

    def interface_identifier(self,node):
        return {'type':'interface', 'name':node[0], 'signal': node[1], 'string': '.'.join(node)}
    
    def expression_bin(self,node):
        retstring = ''

        for i in node:
            if type(i) == dict:
                return node
            elif type(i) == int:
                retstring +=  str(i)
            else:
                retstring +=  i
        return retstring
    
    def expression_un(self,node):
        for i in node:
            if type(i) == dict:
                return node
        return ''.join(node)

    def binary_operators(self,node):
        return node[0].value
        
    def unary_operator(self,node):
        return node[0].value

    def sys_task(self,node):
        ret_val = {}

        ret_val['task'] = node[0].value
        if len(node) == 3:
            ret_val['argument'] = {'name': node[1], 'range':node[2]}
        else:
            ret_val['argument'] = {'name': node[1]}
        return ret_val


    def bus_bit(self, node):
        return{'type': 'dimensions', 'single_bit':True, 'first_bound': node[0]}
            
    
    def bus_slice(self,node):
        return{'type': 'dimensions', 'single_bit':False, 'first_bound': node[0], 'second_bound': node[1]}


    def repetition(self,node):
        return {'type':'repetition', 'pattern':node[1], 'size':node[0]}

    def concatenation(self,node):
        return {'type':'concat', 'elements': node}

    def genvar(self, node):
        raise Discard
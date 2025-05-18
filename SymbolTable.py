from StaticError import *
from Symbol import *
from functools import *


def simulate(list_of_commands):
    def split_parts(command):
        if '  ' in command:
            raise InvalidInstruction(command)
        return command.split()

    def find_variable(symbol, name):
        def find_in_scope(scopes):
            if not scopes:
                return None
            head_scope, *rest_scopes = scopes
            found = find_in_list(head_scope, name)
            if found:
                return found
            return find_in_scope(rest_scopes)

        def find_in_list(lst, name):
            if not lst:
                return None
            head_var, *rest_vars = lst
            if head_var.name == name:
                return head_var
            return find_in_list(rest_vars, name)

        reversed_symbol = list(reversed(symbol))
        return find_in_scope(reversed_symbol)

    def is_valid_string_constant(value):
        return (
            len(value) >= 2 and value[0] == "'" and value[-1] == "'" and
            all(c.isalnum() or c == ' ' for c in value[1:-1])
        )
    
    def handle_insert(parts, symbol):
        if len(parts) != 3:
            raise InvalidInstruction(' '.join(parts))
        typ = parts[2]
        if not (parts[1][0].islower() and all(c.isalnum() or c == '_' for c in parts[1])):
            raise InvalidInstruction(' '.join(parts))
        if not parts[1][0].isalpha():
            raise InvalidInstruction(' '.join(parts))
        if typ not in ("string", "number"):
            raise InvalidInstruction(' '.join(parts))
        if find_variable([symbol[-1]], parts[1]) is not None:
            raise Redeclared(' '.join(parts))
        
        new_scope = symbol[-1] + [Symbol(parts[1], typ)]
        return "success", symbol[:-1] + [new_scope]

    def handle_assign(parts, symbol):
        if len(parts) != 3:
            raise InvalidInstruction(' '.join(parts))
        value = parts[2]
        
        if not (parts[1][0].islower() and all(c.isalnum() or c == '_' for c in parts[1])):
            raise InvalidInstruction(' '.join(parts))
        if not parts[1][0].isalpha():
            raise InvalidInstruction(' '.join(parts))
        if find_variable(symbol, parts[1]) is None:
            raise Undeclared(' '.join(parts))
        
        var_obj = find_variable(symbol, parts[1])
        if var_obj is None:
            raise Undeclared(' '.join(parts))

        def infer_type(value):
            if value.isdigit():
                return "number"
            if is_valid_string_constant(value):
                return "string"
            ref_var = find_variable(symbol, value)
            if ref_var is None:
                return None
            return ref_var.typ

        inferred_typ = infer_type(value)
        if inferred_typ is None:
            if len(value) >= 2 and (value[0] == "'" or value[-1] == "'") or not value[0].isalpha() or not value[0].islower():
                raise InvalidInstruction(' '.join(parts))
            elif not all(c.isalnum() or c == '_' for c in value):
                raise InvalidInstruction(' '.join(parts))
            raise Undeclared(' '.join(parts))

        if var_obj.typ != inferred_typ:
            raise TypeMismatch(' '.join(parts))

        return "success", symbol

    def handle_begin(parts, symbol):
        if len(parts) != 1:
            raise InvalidInstruction(' '.join(parts))
        return None, symbol + [[]]

    def handle_end(parts, symbol):
        if len(parts) != 1:
            raise InvalidInstruction(' '.join(parts))
        if len(symbol) == 1:
            raise UnknownBlock()
        return None, symbol[:-1]

    def handle_lookup(parts, symbol):
        if len(parts) != 2:
            raise InvalidInstruction(' '.join(parts))
        if parts[1][0].isdigit():
            raise InvalidInstruction(' '.join(parts))
        if parts[1] in handlers:
            raise InvalidInstruction(' '.join(parts))
        def lookup(scopes, level):
            if not scopes:
                return None
            if find_variable([scopes[-1]], parts[1]) is not None:
                return level
            return lookup(scopes[:-1], level - 1)

        found_level = lookup(symbol, len(symbol) - 1)
        if found_level is None:
            if not (parts[1][0].islower() and all(c.isalnum() or c == '_' for c in parts[1]) ) :
                raise InvalidInstruction(' '.join(parts))
            raise Undeclared(' '.join(parts))
        return str(found_level), symbol

    def collect_vars(scopes, seen=frozenset()):
        if not scopes:
            return []
        current_scope = scopes[-1]
        rest_scopes = scopes[:-1]
        def collect_from_scope(vars_in_scope, seen):
            if not vars_in_scope:
                return [], seen
            var, *rest = vars_in_scope
            if var.name in seen:
                return collect_from_scope(rest, seen)
            collected_rest, updated_seen = collect_from_scope(rest, seen.union({var.name}))
            return [f"{var.name}//{len(rest_scopes)}"] + collected_rest, updated_seen

        collected_now, updated_seen = collect_from_scope(current_scope, seen)
        collected_rest = collect_vars(rest_scopes, updated_seen)
        return collected_rest + collected_now

    def handle_print(parts, symbol):
        if len(parts) != 1:
            raise InvalidInstruction(' '.join(parts))
        return " ".join(collect_vars(symbol)), symbol

    def handle_rprint(parts, symbol):
        if len(parts) != 1:
            raise InvalidInstruction(' '.join(parts))
        return " ".join(reversed(collect_vars(symbol))), symbol

    handlers = {
        "INSERT": handle_insert,
        "ASSIGN": handle_assign,
        "BEGIN": handle_begin,
        "END": handle_end,
        "LOOKUP": handle_lookup,
        "PRINT": handle_print,
        "RPRINT": handle_rprint
    }

    def process(commands, symbol, outputs):
        if not commands:
            return outputs, symbol
        if commands[0].startswith(' '):
            raise InvalidInstruction("Invalid command")
        parts = split_parts(commands[0])
        if len(parts) > 3:
            raise InvalidInstruction(' '.join(parts))
        if len(parts) == 0:
            raise InvalidInstruction("Invalid command")
        command_typ = parts[0]
        if command_typ not in handlers:
            raise InvalidInstruction("Invalid command")
        if commands[0].endswith(' '):
            raise InvalidInstruction(commands[0])

        if command_typ in handlers:
            msg, new_symbol = handlers[command_typ](parts, symbol)
            new_outputs = outputs if msg is None else outputs + [msg]
            return process(commands[1:], new_symbol, new_outputs)
        else:
            raise InvalidInstruction("Invalid command")

    def count_unclosed(commands):
        def helper(cmds, acc):
            if not cmds:
                return acc
            head, *rest = cmds
            acc_next = acc + (1 if head.strip() == "BEGIN" else -1 if head.strip() == "END" else 0)
            return helper(rest, acc_next)
        return helper(commands, 0)

    try:
        outputs, final_symbol = process(list_of_commands, [[]], [])
        if count_unclosed(list_of_commands) > 0:
            raise UnclosedBlock(count_unclosed(list_of_commands))
        return outputs
    except StaticError as e:
        return [str(e)]

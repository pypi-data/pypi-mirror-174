import os
import re

class CodeOwnersPreprocessor:
    def __init__(self, get_members, preamble='', preamble_separator_length=100):
        self.get_members = get_members
        self.preamble = preamble
        self.preamble_separator_length = preamble_separator_length

    def __call__(self, template):
        def replacement(match):
            group_name = match.group(1)
            members = self.get_members(group_name)
            if members is None:
                return match.group(0)  # leave as-is
            return " ".join(members)

        result = re.sub(r'(?<=\s)@(\S+)', replacement, template)
        if self.preamble:
            if self.preamble_separator_length:
                result = '# ' + '-' * (self.preamble_separator_length - 2) + os.linesep + result
            result = self.preamble + os.linesep + result
        return result



#!/usr/bin/env python
"""Module for converting raw knights and knaves puzzles into a standard format."""

from __future__ import print_function
import re


def symbolize(claim, template):
    """Validate a given template."""
    def symbolize_generalized(start_name_i, start_k_i, offset, bool_func):
        """Symbolize a generalized conjunction or disjunction."""
        words = claim.split(" ")
        name_i, k_i, offset = start_name_i, start_k_i, offset

        ret_str = ""
        while k_i < len(words):
            ret_str += words[k_i] + "(" + words[name_i] + ") " + bool_func + " "
            name_i, k_i = name_i + offset, k_i + offset

        ret_str = ret_str[:-(len(bool_func) + 2)]
        return ret_str

    # Handle 2AND
    if template == "both name and name are k_ids":
        words = claim.split(" ")
        return words[-1][:-1] + "(" + words[1] + ") AND " + words[-1][:-1] + "(" + words[3] + ")"
    if template == "both name is a k_id and name is a k_id":
        words = claim.split(" ")
        return words[-1] + "(" + words[1] + ") AND " + words[-1] + "(" + words[6] + ")"
    if template == "name and name are both k_ids":
        words = claim.split(" ")
        return words[-1][:-1] + "(" + words[0] + ") AND " + words[-1][:-1] + "(" + words[2] + ")"

    # Handle ALL(N,...,M) = K_ID
    if re.match(r"^name( and name)* are k_ids$", template):
        words = claim.split(" ")
        n_i, k = 0, words[-1][:-1]
        ret_str = ""
        while n_i < len(words) - 2:
            ret_str += k + "(" + words[n_i] + ") AND "
            n_i += 2

        ret_str = ret_str[:-5]
        return ret_str

    # Handle K_id(N1) ... GAND ... K_id(NM)
    if re.match(r"^(name is a k_id)( and name is a k_id)*$", template):
        return symbolize_generalized(0, 3, 5, "AND")
    if re.match(r"^name know that (name is a k_id)( and that name is a k_id)*$", template):
        return symbolize_generalized(3, 6, 6, "AND")
    if re.match(r"^all of the following is true: (that name is a k_id)( and that name is a k_id)*$", template):
        return symbolize_generalized(7, 10, 6, "AND")

    # Handle K_id(N1) ... GOR ... K_id(NM)
    if re.match(r"^(name is a k_id)( or name is a k_id)*$", template):
        return symbolize_generalized(0, 3, 5, "OR")
    if re.match(r"^at least one of the following is true: (that anme is a k_id)( or that name is a k_id)*$", template):
        return symbolize_generalized(9, 12, 6, "OR")

    # Handle K_id(N1) XOR K_id(N2)
    if template == "either name is a k_id or name is a k_id":
        words = claim.split(" ")
        return words[4] + "(" + words[1] + ") XOR " + words[-1] + "(" + words[6] + ")"
    if template == "name and name are different":
        words = claim.split(" ")
        name1, name2 = words[0], words[2]
        return "(knight(" + name1 + ") AND knave(" + name2 + ")) OR (knave(" + name1 + ") AND knight(" + name2 + "))"
    if template == "name and name are not the same":
        words = claim.split(" ")
        name1, name2 = words[0], words[2]
        return "(knight(" + name1 + ") AND knave(" + name2 + ")) OR (knave(" + name1 + ") AND knight(" + name2 + "))"
    if template == "of name and name, exactly one is a k_id":
        words = claim.split(" ")
        name1, name2 = words[1], words[3][:-1]
        return "(knight(" + name1 + ") AND knave(" + name2 + ")) OR (knave(" + name1 + ") AND knight(" + name2 + "))"

    # Handle NOT (K_id(1) ... GAND ... K_id(NM))
    if re.match(r"^it's false that (name is a k_id)( and name is a k_id)*$", template):
        return "NOT (" + symbolize_generalized(3, 6, 5, "AND") + ")"
    if re.match(r"^it's false that name know that (name is a k_id)( and that name is a k_id)*$", template):
        return "NOT (" + symbolize_generalized(6, 9, 6, "AND") + ")"
    if re.match(r"^it's false that all of the following is true: (that name is a k_id)( and that name is a k_id)*$", template):
        return "NOT (" + symbolize_generalized(10, 13, 6, "AND") + ")"
    if re.match(r"^it's not the case that (name is a k_id)( and name is a k_id)*$", template):
        return "NOT (" + symbolize_generalized(5, 8, 5, "AND") + ")"
    if re.match(r"^it's not the case that name know that (name is a k_id)( and that name is a k_id)*$", template):
        return "NOT (" + symbolize_generalized(8, 11, 6, "AND") + ")"
    if re.match(r"^it's not the case that all of the following is true: (that name is a k_id)( and that name is a k_id)*$", template):
        return "NOT (" + symbolize_generalized(12, 15, 6, "AND") + ")"

    # Handle NOT (K_id(1) ... GOR ... K_id(NM))
    if re.match(r"^it's false that (name is a k_id)( or name is a k_id)*$", template):
        return "NOT (" + symbolize_generalized(3, 6, 5, "OR") + ")"
    if re.match(r"^it's false that at least one of the following is true: (that name is a k_id)( or that name is a k_id)*$", template):
        return "NOT (" + symbolize_generalized(12, 15, 6, "OR") + ")"
    if re.match(r"^it's not the case that (name is a k_id)( or name is a k_id)*$", template):
        return "NOT (" + symbolize_generalized(5, 8, 5, "OR") + ")"
    if re.match(r"^it's not the case that at least one of the following is true: (that name is a k_id)( or that name is a k_id)*$", template):
        return "NOT (" + symbolize_generalized(14, 17, 5, "OR") + ")"

    # Handle K_id(N1) <-> K_id(N2)
    if template == "name and name are both k_ids or both k_ids":
        words = claim.split(" ")
        name1, name2 = words[0], words[2]
        return "(knave(" + name1 + ") AND knave(" + name2 + ")) XOR (knight(" + name1 + ") AND knight(" + name2 + "))"
    if template == "name and name are the same":
        words = claim.split(" ")
        name1, name2 = words[0], words[2]
        return "(knave(" + name1 + ") AND knave(" + name2 + ")) XOR (knight(" + name1 + ") AND knight(" + name2 + "))"

    # Handle K_id(N1) -> (K_id(N1) ... GAND ... K_id(NM))
    if re.match(r"^name could claim that (name is a k_id)( and name is a k_id)*$", template):
        return claim.split(" ")[0] + " -> (" + symbolize_generalized(4, 7, 5, "AND") + ")"
    if re.match(r"^name could claim that name know that (name is a k_id)( and that name is a k_id)*$", template):
        return claim.split(" ")[0] + " -> (" + symbolize_generalized(7, 10, 6, "AND") + ")"
    if re.match(r"^name could claim that all of the following is true: (that name is a k_id)( and that name is a k_id)*$", template):
        return claim.split(" ")[0] + " -> (" + symbolize_generalized(11, 14, 6, "AND") + ")"
    if re.match(r"^name could say that (name is a k_id)( and name is a k_id)*$", template):
        return claim.split(" ")[0] + " -> (" + symbolize_generalized(4, 7, 5, "AND") + ")"
    if re.match(r"^name could say that name know that (name is a k_id)( and that name is a k_id)*$", template):
        return claim.split(" ")[0] + " -> (" + symbolize_generalized(7, 10, 6, "AND") + ")"
    if re.match(r"^name could say that all of the following is true: (that name is a k_id)( and that name is a k_id)*$", template):
        return claim.split(" ")[0] + " -> (" + symbolize_generalized(11, 14, 6, "AND") + ")"
    if re.match(r"^name would tell you that (name is a k_id)( and name is a k_id)*$", template):
        return claim.split(" ")[0] + " -> (" + symbolize_generalized(5, 8, 5, "AND") + ")"
    if re.match(r"^name would tell you name know that (name is a k_id)( and that name is a k_id)*$", template):
        return claim.split(" ")[0] + " -> (" + symbolize_generalized(11, 14, 6, "AND") + ")"
    if re.match(r"^name would tell you all of the following is true: (that name is a k_id)( and that name is a k_id)*$", template):
        return claim.split(" ")[0] + " -> (" + symbolize_generalized(11, 14, 6, "AND") + ")"

    # Handle K_id(N1) -> (K_id(N1) ... GOR ... K_id(NM))
    if re.match(r"^name could claim that (name is a k_id)( or name is a k_id)*$", template):
        return claim.split(" ")[0] + " -> (" + symbolize_generalized(4, 7, 5, "OR") + ")"
    if re.match(r"^name could claim that at least one of the following is true: (that name is a k_id)( or that name is a k_id)*$", template):
        return claim.split(" ")[0] + " -> (" + symbolize_generalized(13, 16, 6, "OR") + ")"
    if re.match(r"^name could say that (name is a k_id)( or name is a k_id)*$", template):
        return claim.split(" ")[0] + " -> (" + symbolize_generalized(4, 7, 5, "OR") + ")"
    if re.match(r"^name could say that at least one of the following is true: (that name is a k_id)( or that name is a k_id)*$", template):
        return claim.split(" ")[0] + " -> (" + symbolize_generalized(13, 16, 6, "OR") + ")"
    if re.match(r"^name would tell you that (name is a k_id)( or name is a k_id)*$", template):
        return claim.split(" ")[0] + " -> (" + symbolize_generalized(5, 8, 5, "OR") + ")"
    if re.match(r"^name would tell you at least one of the following is true: (that name is a k_id)( or that name is a k_id)*$", template):
        return claim.split(" ")[0] + " -> (" + symbolize_generalized(13, 16, 6, "OR") + ")"

    # Handle K_id(N1) NOR K_id(N2)
    if template == "neither name nor name are k_ids":
        words = claim.split(" ")
        return "NOT (" + words[-1][:-1] + "(" + words[1] + ") AND " + words[-1][:-1] + "(" + words[3] + "))"


def main():
    """."""
    pass

if __name__ == "__main__":
    main()

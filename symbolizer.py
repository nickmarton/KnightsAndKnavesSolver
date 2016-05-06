#!/usr/bin/env python
"""Module for converting raw knights and knaves puzzles into a standard format."""


def to_cnf(claim, template, speaker, name_map):
    """."""

    negate_knaves = lambda x, k: -x if k == "knave" else x
    id_0_val = name_map[speaker]

    #  Handle P
    if template == "name is a k_id":
        id_1, kid_1 = claim.split()[0], claim.split()[-1]
        id_1_val = negate_knaves(name_map[id_1], kid_1)

        cnf = [[-id_0_val, id_1_val], [id_0_val, -id_1_val]]
        return cnf

    #  Handle NOT P
    if template == "it's false that name is a k_id":
        id_1, kid_1 = claim.split()[3], claim.split()[-1]
        id_1_val = negate_knaves(name_map[id_1], kid_1)

        cnf = [[-id_0_val, -id_1_val], [id_0_val, id_1_val]]
        return cnf
    elif template == "it's not the case that name is a k_id":
        id_1, kid_1 = claim.split()[5], claim.split()[-1]
        id_1_val = negate_knaves(name_map[id_1], kid_1)

        cnf = [[-id_0_val, -id_1_val], [id_0_val, id_1_val]]
        return cnf

    #  Handle P OR Q
    if template == "at least one of the following is true: that name is a k_id or that name is a k_id":
        id_1, kid_1 = claim.split()[9], claim.split()[12]
        id_2, kid_2 = claim.split()[15], claim.split()[18]
        id_1_val = negate_knaves(name_map[id_1], kid_1)
        id_2_val = negate_knaves(name_map[id_2], kid_2)

        cnf = [[-id_0_val, id_1_val, id_2_val], [id_0_val, -id_1_val], [id_0_val, -id_2_val]]
        return cnf
    elif template == "name is a k_id or name is a k_id":
        id_1, kid_1 = claim.split()[0], claim.split()[3]
        id_2, kid_2 = claim.split()[5], claim.split()[8]
        id_1_val = negate_knaves(name_map[id_1], kid_1)
        id_2_val = negate_knaves(name_map[id_2], kid_2)

        cnf = [[-id_0_val, id_1_val, id_2_val], [id_0_val, -id_1_val], [id_0_val, -id_2_val]]
        return cnf

    #  Handle P AND Q
    if template == "name and name are k_ids":
        id_1, kid_1 = claim.split()[0], claim.split()[-1][:-1]
        id_2, kid_2 = claim.split()[2], claim.split()[-1][:-1]
        id_1_val = negate_knaves(name_map[id_1], kid_1)
        id_2_val = negate_knaves(name_map[id_2], kid_2)

        cnf = [[-id_0_val, id_1_val], [-id_0_val, id_2_val], [id_0_val, -id_1_val, -id_2_val]]
        return cnf
    elif template == "name and name are both k_ids":
        id_1, kid_1 = claim.split()[0], claim.split()[-1][:-1]
        id_2, kid_2 = claim.split()[2], claim.split()[-1][:-1]
        id_1_val = negate_knaves(name_map[id_1], kid_1)
        id_2_val = negate_knaves(name_map[id_2], kid_2)

        cnf = [[-id_0_val, id_1_val], [-id_0_val, id_2_val], [id_0_val, -id_1_val, -id_2_val]]
        return cnf
    elif template == "name is a k_id and name is a k_id":
        id_1, kid_1 = claim.split()[0], claim.split()[3]
        id_2, kid_2 = claim.split()[5], claim.split()[8]
        id_1_val = negate_knaves(name_map[id_1], kid_1)
        id_2_val = negate_knaves(name_map[id_2], kid_2)

        cnf = [[-id_0_val, id_1_val], [-id_0_val, id_2_val], [id_0_val, -id_1_val, -id_2_val]]
        return cnf
    elif template == "both name is a k_id and name is a k_id":
        id_1, kid_1 = claim.split()[1], claim.split()[4]
        id_2, kid_2 = claim.split()[6], claim.split()[9]
        id_1_val = negate_knaves(name_map[id_1], kid_1)
        id_2_val = negate_knaves(name_map[id_2], kid_2)

        cnf = [[-id_0_val, id_1_val], [-id_0_val, id_2_val], [id_0_val, -id_1_val, -id_2_val]]
        return cnf
    elif template == "name know that name is a k_id and that name is a k_id":
        id_1, kid_1 = claim.split()[3], claim.split()[6]
        id_2, kid_2 = claim.split()[9], claim.split()[12]
        id_1_val = negate_knaves(name_map[id_1], kid_1)
        id_2_val = negate_knaves(name_map[id_2], kid_2)

        cnf = [[-id_0_val, id_1_val], [-id_0_val, id_2_val], [id_0_val, -id_1_val, -id_2_val]]
        return cnf
    elif template == "both name and name are k_ids":
        id_1, kid_1 = claim.split()[1], claim.split()[-1][:-1]
        id_2, kid_2 = claim.split()[3], claim.split()[-1][:-1]
        id_1_val = negate_knaves(name_map[id_1], kid_1)
        id_2_val = negate_knaves(name_map[id_2], kid_2)

        cnf = [[-id_0_val, id_1_val], [-id_0_val, id_2_val], [id_0_val, -id_1_val, -id_2_val]]
        return cnf

    #  Handle P XOR Q
    if template == "either name is a k_id or name is a k_id":
        id_1, kid_1 = claim.split()[1], claim.split()[4]
        id_2, kid_2 = claim.split()[6], claim.split()[9]
        id_1_val = negate_knaves(name_map[id_1], kid_1)
        id_2_val = negate_knaves(name_map[id_2], kid_2)

        cnf = [[-id_0_val, -id_1_val, -id_2_val], [-id_0_val, id_1_val, id_2_val],
               [id_0_val, -id_1_val, id_2_val], [id_0_val, id_1_val, -id_2_val]]
        return cnf

    #  Handle (P & ~Q) XOR (~P & Q)
    if template == "name and name are not the same":
        id_1, id_2 = claim.split()[0], claim.split()[2]
        id_1_val, id_2_val = name_map[id_1], name_map[id_2]

        cnf = [[-id_0_val, -id_1_val, -id_2_val], [-id_0_val, id_1_val, id_2_val],
               [id_0_val, -id_1_val, id_2_val], [id_0_val, id_1_val, -id_2_val]]
        return cnf
    elif template == "name and name are different":
        id_1, id_2 = claim.split()[0], claim.split()[2]
        id_1_val, id_2_val = name_map[id_1], name_map[id_2]

        cnf = [[-id_0_val, -id_1_val, -id_2_val], [-id_0_val, id_1_val, id_2_val],
               [id_0_val, -id_1_val, id_2_val], [id_0_val, id_1_val, -id_2_val]]
        return cnf
    elif template == "of name and name, exactly one is a k_id":
        id_1, id_2 = claim.split()[1], claim.split()[3][:-1]
        id_1_val, id_2_val = name_map[id_1], name_map[id_2]

        cnf = [[-id_0_val, -id_1_val, -id_2_val], [-id_0_val, id_1_val, id_2_val],
               [id_0_val, -id_1_val, id_2_val], [id_0_val, id_1_val, -id_2_val]]
        return cnf

    #  Handle P IMPLIES Q
    if template == "name could claim that name is a k_id":
        id_1, kid_1 = claim.split()[0], "knight"
        id_2, kid_2 = claim.split()[4], claim.split()[-1]
        id_1_val = negate_knaves(name_map[id_1], kid_1)
        id_2_val = negate_knaves(name_map[id_2], kid_2)

        cnf = [[-id_0_val, -id_1_val, id_2_val], [id_0_val, id_1_val],
               [id_0_val, -id_2_val]]
        return cnf
    elif template == "name could say that name is a k_id":
        id_1, kid_1 = claim.split()[0], "knight"
        id_2, kid_2 = claim.split()[4], claim.split()[-1]
        id_1_val = negate_knaves(name_map[id_1], kid_1)
        id_2_val = negate_knaves(name_map[id_2], kid_2)

        cnf = [[-id_0_val, -id_1_val, id_2_val], [id_0_val, id_1_val],
               [id_0_val, -id_2_val]]
        return cnf
    elif template == "name would tell you that name is a k_id":
        id_1, kid_1 = claim.split()[0], "knight"
        id_2, kid_2 = claim.split()[5], claim.split()[-1]
        id_1_val = negate_knaves(name_map[id_1], kid_1)
        id_2_val = negate_knaves(name_map[id_2], kid_2)

        cnf = [[-id_0_val, -id_1_val, id_2_val], [id_0_val, id_1_val],
               [id_0_val, -id_2_val]]
        return cnf
    elif template == "only a k_id would say that name is a k_id":
        id_1, kid_1 = speaker, "knave"
        id_2, kid_2 = claim.split()[6], claim.split()[-1]
        id_1_val = negate_knaves(name_map[id_1], kid_1)
        id_2_val = negate_knaves(name_map[id_2], kid_2)

        cnf = [[-id_0_val, -id_1_val, id_2_val], [id_0_val, id_1_val],
               [id_0_val, -id_2_val]]
        return cnf

    #  Handle P <-> Q
    if template == "name and name are both k_ids or both k_ids":
        id_1, kid_1 = claim.split()[0], "knight"
        id_2, kid_2 = claim.split()[2], "knight"
        id_1_val = negate_knaves(name_map[id_1], kid_1)
        id_2_val = negate_knaves(name_map[id_2], kid_2)

        cnf = [[-id_0_val, -id_1_val, id_2_val], [-id_0_val, id_1_val, -id_2_val],
               [id_0_val, -id_1_val, -id_2_val], [id_0_val, id_1_val, id_2_val]]
        return cnf
    elif template == "name and name are the same":
        id_1, kid_1 = claim.split()[0], "knight"
        id_2, kid_2 = claim.split()[2], "knight"
        id_1_val = negate_knaves(name_map[id_1], kid_1)
        id_2_val = negate_knaves(name_map[id_2], kid_2)

        cnf = [[-id_0_val, -id_1_val, id_2_val], [-id_0_val, id_1_val, -id_2_val],
               [id_0_val, -id_1_val, -id_2_val], [id_0_val, id_1_val, id_2_val]]
        return cnf

    #  Handle ~(P OR Q)
    if template == "neither name nor name are k_ids":
        id_1, kid_1 = claim.split()[1], claim.split()[-1][:-1]
        id_2, kid_2 = claim.split()[3], claim.split()[-1][:-1]
        id_1_val = negate_knaves(name_map[id_1], kid_1)
        id_2_val = negate_knaves(name_map[id_2], kid_2)

        cnf = [[-id_0_val, -id_1_val], [-id_0_val, -id_2_val], [id_0_val, id_1_val, id_2_val]]
        return cnf

    raise ValueError("Unsupported template provided.")


def main():
    """."""
    pass

if __name__ == "__main__":
    main()

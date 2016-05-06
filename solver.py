#!/usr/bin/env python
"""Module for solving knights and knaves puzzles."""

from __future__ import print_function

import sys, os
import pycosat
from symbolizer import to_cnf

templates = set([])


def templatize(names, claim):
    """Transform a claim into a regex-capable template."""
    for name in names:
        while name in claim:
            claim = claim.replace(name, "name")

    while "knave" in claim:
        claim = claim.replace("knave", "k_id")

    while "knight" in claim:
        claim = claim.replace("knight", "k_id")

    while " am " in claim:
        claim = claim.replace(" am ", " is ")

    return claim.lower()


def parse(puzzle):
    """Parse puzzles of form {name: claim} into symbolized form."""
    # Replace instances of "I" with name of speaker
    puzzle = {name: claim.replace(" I ", " " + name + " ").replace("I ", name + " ").replace(" I", " " + name)
              for name, claim in puzzle.iteritems()}

    names = puzzle.keys()
    name_map = {names[i]: i + 1 for i in range(len(names))}
    inverse_name_map = {int_id: name for name, int_id in name_map.iteritems()}

    puzzle_cnf = []
    for speaker, claim in puzzle.iteritems():

        # transform given claim into a template
        template = templatize(names, claim)

        cnf_claim = to_cnf(claim, template, speaker, name_map)
        puzzle_cnf.extend(cnf_claim)

        global templates
        templates.add(template)

    return puzzle_cnf, inverse_name_map


def clean(puzzle):
    """Format a given puzzle into the form {name: claim}."""
    def clean_claim(claim):
        """Strip uninformative leading words from a given claim."""
        rm_claims_comma = lambda x: x.split("claims, ")[1] if "claims, " in x else x
        rm_claims_that = lambda x: x.split("claims that ")[1] if "claims that " in x else x
        rm_says_comma = lambda x: x.split("says, ")[1] if "says, " in x else x
        rm_says_that = lambda x: x.split("says that ")[1] if "says that " in x else x
        rm_tells_you_comma = lambda x: x.split("tells you, ")[1] if "tells you, " in x else x
        rm_tells_you_that = lambda x: x.split("tells you that ")[1] if "tells you that " in x else x
        rm_trail_apo = lambda x: x[:-1] if x[-1] == "\'" else x
        rm_lead_backtick = lambda x: x[1:] if x[0] == "`" else x

        func_list = [rm_claims_comma, rm_claims_that, rm_says_comma,
                     rm_says_that, rm_tells_you_comma, rm_tells_you_that,
                     rm_trail_apo, rm_lead_backtick]

        parsed_claim = reduce(lambda c, func: func(c), func_list, claim)

        return parsed_claim

    rm_lead_apo = lambda x: x[1:] if x[0] == '\'' else x
    rm_ws = lambda x: x.strip()

    lines = puzzle.split(".")
    lines, name_line = lines[1:], lines[0]

    sub_comma_for_and = lambda x: x.replace("and", ",")
    make_names = lambda x: map(rm_ws, x.split(":")[1].split(","))

    names = make_names(sub_comma_for_and(name_line))
    claims = {}

    for line in lines:
        if len(line) > 1:
            formatted_line = rm_ws(rm_lead_apo(line))
            name = formatted_line[:formatted_line.find(" ")]
            claim = formatted_line[formatted_line.find(" ") + 1:]

            if name not in names:
                raise ValueError("Badly formatted puzzle")
            else:
                claims[name] = clean_claim(claim)

    return claims


def process(puzzle, do_clean=True):
    """Process an individual knights and knaves problem."""

    if do_clean:
        puzzle = clean(puzzle)

    cnf, inverse_name_map = parse(puzzle)
    # print (cnf)
    add_kid = lambda x, i: "knight(" + x + ")" if i > 0 else "knave(" + x + ")"

    parsed_results = []
    if pycosat.solve(cnf) == "UNSAT":
        pass
    else:
        results = pycosat.itersolve(cnf)
        for result in results:
            result = [add_kid(inverse_name_map[abs(i)], i) for i in result]
            parsed_results.append(result)

    return parsed_results


def main():
    """Entry point."""

    cmds = ["help", "new puzzle", "show", "solve", "clear", "add", "quit()", "list"]

    puzzles = []
    with open("raw.txt", "r") as f:
        for line in f:
            puzzles = line[:-2].split("###")

    # Index all solutions from website
    solutions = {}
    no_solutions = {}
    multi_solutions = {}
    for index, puzzle in enumerate(puzzles):
        parsed_puzzles = process(puzzle)
        solutions[index + 1] = (puzzle, parsed_puzzles)

        if not parsed_puzzles:
            no_solutions[index + 1] = (puzzle, parsed_puzzles)

        if len(parsed_puzzles) > 1:
            multi_solutions[index + 1] = (puzzle, parsed_puzzles)

    # Bring templates into local scope
    global templates

    interactive_claims = {}
    print ("Welcome to Knights and Knaves solver; enter a command or 'help'\n")
    while True:
        cmd = raw_input()

        if cmd == "quit()":
            break

        if cmd == "help":
            print ("Enter one of the following commands or 'help [cmd]' for a more detailed description.")
            print (" | ".join(cmds) + "\n")

        if cmd == "help new puzzle":
            print("Start a new puzzle in interactive mode, clearing the old added entries.\n")
        if cmd == "help show":
            print ("Enter 'show solution i' to show the solution to puzzle i or to all puzzles.")
            print ("Enter 'show solution all' to show the solution to all puzzles in order.")
            print ("Enter 'show templates' to show the available templates supported.\n")
        if cmd == "help solve":
            print ("Solve the interactive mode puzzle; try to find a solution for all added claims.\n")
        if cmd == "help clear":
            print ("Clear the terminal screen.\n")
        if cmd == "help add":
            print ("Add a name and claim to the interactive mode puzzle (where the claim has a supported template).\n")
        if cmd == "help quit()":
            print ("Exit the Knights and Knaves session.\n")
        if cmd == "help list":
            print ("Enter 'list no solutions' to list all puzzles with no solutions")
            print ("Enter 'list multiple solutions' to list all puzzles with multiple solutions")

        if cmd == "clear":
            os.system("clear")

        if cmd == "solve":
            int_names = interactive_claims.keys()

            bad_templates = False

            interactive_claims = {name: claim.replace(" I ", " " + name + " ").replace("I ", name + " ").replace(" I", " " + name)
                                  for name, claim in interactive_claims.iteritems()}

            for int_claim in interactive_claims.values():
                int_template = templatize(int_names, int_claim)
                if int_template not in templates:
                    print (int_template)
                    print ("Invalid templates provided; starting new puzzle")
                    interactive_claims = {}
                    bad_templates = True
                    break

            if bad_templates:
                continue

            parsed_puzzles = process(interactive_claims, do_clean=False)
            print (interactive_claims)
            print ()
            print (parsed_puzzles)

        if cmd == "add":
            print ("Who is making the claim?")
            name = raw_input()
            print ("What is the claim?")
            claim = raw_input()
            interactive_claims[name] = claim
            print ()

        if cmd == "list no solutions":
            print ("The following puzzles have no solutions:")
            print (", ".join([str(puzzle_id) for puzzle_id in sorted(no_solutions.keys())]) + '\n')

        if cmd == "list multiple solutions":
            print ("The following puzzles have multiple solutions:")
            print (", ".join([str(puzzle_id) for puzzle_id in sorted(multi_solutions.keys())]) + '\n')

        args = cmd.split()

        if len(args) >= 2:
            if args[0] == "new" and args[1] == "puzzle":
                print ("Beginning new puzzle")
                interactive_claims = {}

            if args[0] == "show":
                if args[1] == "templates":
                    temp_copy = templates
                    templates = sorted(list(templates))
                    templates = temp_copy

                    for template in templates:
                        print (template)
                    print ()

                elif args[1] == "solution":
                    if len(args) == 3:
                        try:
                            sol_id = int(args[2])
                            if 1 <= sol_id <= 382:
                                puzzle, solution_set = solutions[sol_id]
                                print (puzzle)
                                print ()
                                if solution_set:
                                    for sol in solution_set:
                                        print (sol)
                                else:
                                    print ("No solutions")
                                print()
                            else:
                                print ("Invalid command provided")
                        except ValueError:
                            if args[2] == "all":
                                for puzzle, solution_set in solutions.values():
                                    print ("PUZZLE: " + str(sol_id))
                                    print (puzzle)
                                    print ()
                                    if solution_set:
                                        for sol in solution_set:
                                            print (sol)
                                    else:
                                        print ("No solutions")
                                    print ('\n' * 3)
                            else:
                                print ("Invalid command provided")
                else:
                    print ("Invalid command provided")

if __name__ == "__main__":
    main()

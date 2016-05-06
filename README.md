# Knights and Knaves Solver
---

### How To Use
---
First, the pycosat dependency found [here](https://pypi.python.org/pypi/pycosat) must be installed.

This program uses the examples found [here](http://philosophy.hku.hk/think/logic/knights.php) as templates for input. To that end, a puzzle is captured entirely in a string (e.g. "You meet two inhabitants: Zoey and Mel.  Zoey tells you that Mel is a knave.  Mel says, `Neither Zoey nor I are knaves.'").
For each sentence following the first, the form is name-claim. The uninformative leading words after the name and before the claim (e.g. "claims ", "says that ", etc.) will try to be stripped away. The following templates are supported (where each template is a single claim made by an inhabitant of the island, i.e., the claim part of the name-claim form):

* To express "P" as a claim use the template:
	* "name is a k_id"

* To express "NOT P" as a claim use the template:
	* "it's false that name is a k_id"
	* "it's not the case that name is a k_id"

* To express "P OR Q" as a claim use the template:
	* "at least one of the following is true that name is a k_id or that name is a k_id"
	* "name is a k_id or name is a k_id"

* To express "P AND Q" as a claim use the template:
	* "name and name are k_ids"
	* "name and name are both k_ids"
	* "name is a k_id and name is a k_id"
	* "both name is a k_id and name is a k_id"
	* "name know that name is a k_id and that name is a k_id"
	* "both name and name are k_ids"

* To express "P XOR Q" as a claim use the template:
	* "either name is a k_id or name is a k_id"

* To express "(P & ~Q) XOR (~P & Q)" as a claim use the template:
	* "name and name are not the same"
	* "name and name are different"
	* "of name and name, exactly one is a k_id"

* To express "P IMPLIES Q" as a claim use the template:
	* "name could claim that name is a k_id"
	* "name could say that name is a k_id"
	* "name would tell you that name is a k_id"
	* "only a k_id would say that name is a k_id"

* To express "P <-> Q" as a claim use the template:
	* "name and name are both k_ids or both k_ids"
	* "name and name are the same"


* To express "~(P OR Q)" as a claim use the template:
	* "neither name nor name are k_ids"

where name is substituted by a name of the inhabitant and k_id(s) is substituted by knight(s)/knave(s) respectively.

### Interactive Mode
---
In interactive mode, users can generate and subsequently solve their own knights and knaves puzzles. Additionally, the user can show the solution to any puzzle from the examples.

Interactive mode supports the following commands:

* "help": Show all commands supported in interactive mode or show more detail for a given command by following "help" with the string for another command (e.g. "help solve"). 
* "new puzzle": Begin a new interactive Knights and Knaves puzzle, clearing any added claims beforehand.
* "show": Show either templates (i.e., "show templates"), a specfic solution for a puzzle from the examples (e.g. "show solution 8" for the solution to puzzle 8), or show all solutions to the examples (i.e., "show solution all").
* "solve": Attempt to solve the current interactive puzzle, using the claims made through the "add" command.
* "clear": Clear the terminal.
* "add":  Add a claim to the interactive puzzle by listing who said it (name) and what they said (claim) where claim must have the form of a supported template.
* "quit()": Quit the Knights and Knaves session.
* "list": List all puzzles with either no solutions (i.e., "list no solutions") or all puzzles with multiple solutions (i.e., "list all solutions").
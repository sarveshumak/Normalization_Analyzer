from itertools import combinations


# --------------------------------------------------
# 1. ATTRIBUTE CLOSURE
# --------------------------------------------------

def attribute_closure(attributes, fds):

    closure = set(attributes)

    changed = True

    while changed:

        changed = False

        for lhs, rhs in fds:

            if set(lhs).issubset(closure):

                new_attributes = set(rhs) - closure

                if new_attributes:

                    closure.update(new_attributes)
                    changed = True

    return closure


# --------------------------------------------------
# 2. CANDIDATE KEY FINDER
# --------------------------------------------------

def find_candidate_keys(attributes, fds):

    attributes = set(attributes)

    candidate_keys = []

    attribute_list = list(attributes)

    for size in range(1, len(attribute_list) + 1):

        for combination in combinations(attribute_list, size):

            test_set = set(combination)

            closure = attribute_closure(test_set, fds)

            # If closure contains all attributes
            if closure == attributes:

                # Check minimality
                is_minimal = True

                for key in candidate_keys:

                    if key.issubset(test_set):

                        is_minimal = False
                        break

                if is_minimal:

                    candidate_keys.append(test_set)

    return candidate_keys


# --------------------------------------------------
# 3. PARTIAL DEPENDENCY DETECTOR
# --------------------------------------------------

def find_partial_dependencies(attributes, fds, candidate_keys):

    partial_dependencies = []

    attributes = set(attributes)

    # Find prime attributes
    prime_attributes = set()

    for key in candidate_keys:

        prime_attributes.update(key)

    # Non-prime attributes
    non_prime_attributes = attributes - prime_attributes

    for lhs, rhs in fds:

        lhs = set(lhs)
        rhs = set(rhs)

        for key in candidate_keys:

            # LHS is proper subset of candidate key
            if lhs.issubset(key) and lhs != key:

                violating_attributes = rhs & non_prime_attributes

                if violating_attributes:

                    partial_dependencies.append(
                        (lhs, violating_attributes, key)
                    )

    return partial_dependencies


# --------------------------------------------------
# 4. TRANSITIVE DEPENDENCY DETECTOR
# --------------------------------------------------

def find_transitive_dependencies(attributes, fds, candidate_keys):

    transitive_dependencies = []

    attributes = set(attributes)

    # Prime attributes
    prime_attributes = set()

    for key in candidate_keys:

        prime_attributes.update(key)

    # Non-prime attributes
    non_prime_attributes = attributes - prime_attributes

    for lhs, rhs in fds:

        lhs = set(lhs)
        rhs = set(rhs)

        # LHS should not itself be a candidate key
        if not any(lhs == key for key in candidate_keys):

            violating_attributes = rhs & non_prime_attributes

            # Non-prime → non-prime
            if violating_attributes and lhs.issubset(non_prime_attributes):

                transitive_dependencies.append(
                    (lhs, violating_attributes)
                )

    return transitive_dependencies


# --------------------------------------------------
# 5. COMPLETE NORMALIZATION ANALYZER
# --------------------------------------------------

def analyze_normalization(attributes, fds):

    attributes = set(attributes)

    # Candidate keys
    candidate_keys = find_candidate_keys(
        attributes,
        fds
    )

    # Partial dependencies
    partial_dependencies = find_partial_dependencies(
        attributes,
        fds,
        candidate_keys
    )

    # Transitive dependencies
    transitive_dependencies = find_transitive_dependencies(
        attributes,
        fds,
        candidate_keys
    )

    # Determine highest normal form

    if partial_dependencies:

        highest_normal_form = "1NF"

    elif transitive_dependencies:

        highest_normal_form = "2NF"

    else:

        highest_normal_form = "3NF"

    return {

        "candidate_keys": candidate_keys,

        "partial_dependencies":
            partial_dependencies,

        "transitive_dependencies":
            transitive_dependencies,

        "1NF": True,

        "2NF":
            len(partial_dependencies) == 0,

        "3NF":
            len(partial_dependencies) == 0
            and len(transitive_dependencies) == 0,

        "highest_normal_form":
            highest_normal_form
    }


def suggest_decomposition(attributes, fds, candidate_keys):

    decomposition = []

    attributes = set(attributes)

    # Find prime attributes
    prime_attributes = set()

    for key in candidate_keys:
        prime_attributes.update(key)

    # Find non-prime attributes
    non_prime_attributes = attributes - prime_attributes

    # --------------------------------------------
    # Handle transitive dependencies
    # --------------------------------------------

    for lhs, rhs in fds:

        lhs = set(lhs)
        rhs = set(rhs)

        # Look for non-key -> non-key dependency
        if lhs.issubset(non_prime_attributes):

            dependent_attributes = rhs & non_prime_attributes

            if dependent_attributes:

                # Table containing determinant and its attributes
                table1 = lhs | dependent_attributes

                decomposition.append({
                    "reason": "Transitive Dependency",
                    "attributes": table1
                })

                # Remove dependent attributes from original relation
                remaining_attributes = attributes - dependent_attributes

                decomposition.append({
                    "reason": "Remaining Relation",
                    "attributes": remaining_attributes
                })

                break

    return decomposition


def suggest_2nf_decomposition(attributes, fds, candidate_keys):

    attributes = set(attributes)

    decomposition = []

    # We mainly handle composite candidate keys
    for key in candidate_keys:

        if len(key) <= 1:
            continue

        for lhs, rhs in fds:

            lhs = set(lhs)
            rhs = set(rhs)

            # Check if LHS is a proper subset of the candidate key
            if lhs.issubset(key) and lhs != key:

                # Create a new table containing:
                # partial determinant + dependent attributes
                new_table = lhs | rhs

                decomposition.append({
                    "type": "Partial Dependency",
                    "attributes": new_table
                })

    # Remove duplicate tables
    unique_tables = []

    for table in decomposition:

        if table["attributes"] not in [
            x["attributes"] for x in unique_tables
        ]:

            unique_tables.append(table)

    decomposition = unique_tables

    # Original key relation
    if decomposition:

        decomposition.append({
            "type": "Key Relation",
            "attributes": set().union(*[
                set(key) for key in candidate_keys
            ])
        })

    return decomposition



def get_suggested_decomposition(attributes, fds, analysis):

    # -----------------------------------
    # CASE 1: 2NF VIOLATION
    # -----------------------------------

    if not analysis["2NF"]:

        candidate_keys = analysis["candidate_keys"]

        tables = suggest_2nf_decomposition(
            attributes,
            fds,
            candidate_keys
        )

        return {
            "required": True,
            "normalization_level": "2NF",
            "reason": "Partial dependencies detected.",
            "tables": tables
        }

    # -----------------------------------
    # CASE 2: 3NF VIOLATION
    # -----------------------------------

    if not analysis["3NF"]:

        candidate_keys = analysis["candidate_keys"]

        old_tables = suggest_decomposition(
            attributes,
            fds,
            candidate_keys
        )

        # Convert 3NF decomposition format
        # into the same format used by 2NF

        tables = []

        for table in old_tables:

            tables.append({
                "type": table["reason"],
                "attributes": table["attributes"]
            })

        return {
            "required": True,
            "normalization_level": "3NF",
            "reason": "Transitive dependencies detected.",
            "tables": tables
        }

    # -----------------------------------
    # CASE 3: ALREADY IN 3NF
    # -----------------------------------

    return {
        "required": False,
        "normalization_level": "3NF",
        "reason": "Relation is already in 3NF.",
        "tables": []
    }   






# ============================================
# TESTING
# ============================================

if __name__ == "__main__":

    print("=" * 50)
    print("           NORMALIZATION ANALYZER")
    print("=" * 50)

    # ----------------------------------------
    # TEST CASE
    # ----------------------------------------

    attributes = {
        "StudentID",
        "StudentName",
        "DepartmentID",
        "DepartmentName"
    }

    fds = [
        ({"StudentID"}, {"StudentName", "DepartmentID"}),
        ({"DepartmentID"}, {"DepartmentName"})
    ]

    # ----------------------------------------
    # NORMALIZATION ANALYSIS
    # ----------------------------------------

    result = analyze_normalization(
        attributes,
        fds
    )

    # ----------------------------------------
    # CANDIDATE KEYS
    # ----------------------------------------

    print("\nCandidate Keys:")

    for key in result["candidate_keys"]:
        print(key)

    # ----------------------------------------
    # NORMAL FORMS
    # ----------------------------------------

    print("\nNormal Forms:")

    print(
        "1NF:",
        "PASS" if result["1NF"] else "FAIL"
    )

    print(
        "2NF:",
        "PASS" if result["2NF"] else "FAIL"
    )

    print(
        "3NF:",
        "PASS" if result["3NF"] else "FAIL"
    )

    print(
        "\nHighest Normal Form:",
        result["highest_normal_form"]
    )

    # ----------------------------------------
    # PARTIAL DEPENDENCIES
    # ----------------------------------------

    print("\nPartial Dependencies:")

    if result["partial_dependencies"]:

        for dependency in result["partial_dependencies"]:
            print(dependency)

    else:
        print("None")

    # ----------------------------------------
    # TRANSITIVE DEPENDENCIES
    # ----------------------------------------

    print("\nTransitive Dependencies:")

    if result["transitive_dependencies"]:

        for dependency in result["transitive_dependencies"]:
            print(dependency)

    else:
        print("None")

    # ----------------------------------------
    # SUGGESTED DECOMPOSITION
    # ----------------------------------------

    decomposition = get_suggested_decomposition(
        attributes,
        fds,
        result
    )

    print("\nSuggested Decomposition:")

    if not decomposition["required"]:

        print("No decomposition required.")

    else:

        print("Decomposition Required: YES")

        print(
            "Target Normal Form:",
            decomposition["normalization_level"]
        )

        print(
            "Reason:",
            decomposition["reason"]
        )

        for i, table in enumerate(
            decomposition["tables"],
            start=1
        ):

            print(
                f"\nTable {i} "
                f"({table['type']}):"
            )

            print(table["attributes"])

    # ----------------------------------------
    # END
    # ----------------------------------------

    print("\n" + "=" * 50)
    print("          ANALYSIS COMPLETE")
    print("=" * 50)
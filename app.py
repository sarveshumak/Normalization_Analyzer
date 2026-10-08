import streamlit as st

from normalizer import (
    analyze_normalization,
    get_suggested_decomposition
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Normalization Analyzer",
    page_icon="🗄️",
    layout="wide"
)


# ============================================================
# SAMPLE CASES
# ============================================================

SAMPLE_CASES = {
    "Custom Input": {
        "attributes": "",
        "fds": "",
        "atomic": False
    },

    "Example 1 - 2NF Violation": {
        "attributes": (
            "StudentID, CourseID, StudentName, CourseName"
        ),
        "fds": (
            "StudentID -> StudentName\n"
            "CourseID -> CourseName"
        ),
        "atomic": True
    },

    "Example 2 - 3NF Violation": {
        "attributes": (
            "StudentID, StudentName, DepartmentID, DepartmentName"
        ),
        "fds": (
            "StudentID -> StudentName, DepartmentID\n"
            "DepartmentID -> DepartmentName"
        ),
        "atomic": True
    },

    "Example 3 - Already 3NF": {
        "attributes": (
            "StudentID, StudentName"
        ),
        "fds": (
            "StudentID -> StudentName"
        ),
        "atomic": True
    },

    "Example 4 - Composite Key": {
        "attributes": (
            "OrderID, ProductID, ProductName, Quantity"
        ),
        "fds": (
            "OrderID, ProductID -> Quantity\n"
            "ProductID -> ProductName"
        ),
        "atomic": True
    }
}


# ============================================================
# SESSION STATE
# ============================================================

if "selected_case" not in st.session_state:
    st.session_state.selected_case = "Custom Input"

if "attributes_input" not in st.session_state:
    st.session_state.attributes_input = ""

if "fds_input" not in st.session_state:
    st.session_state.fds_input = ""

if "atomic_input" not in st.session_state:
    st.session_state.atomic_input = False


def load_sample_case():

    case = SAMPLE_CASES[
        st.session_state.selected_case
    ]

    st.session_state.attributes_input = case["attributes"]
    st.session_state.fds_input = case["fds"]
    st.session_state.atomic_input = case["atomic"]


# ============================================================
# DEPENDENCY GRAPH
# ============================================================

def create_dependency_graph(fds):

    graph = """
    digraph G {

        rankdir=LR;

        graph [
            bgcolor="transparent",
            pad="0.5"
        ];

        node [
            shape=box,
            style="rounded,filled",
            fontname="Arial",
            fontsize=12
        ];

        edge [
            color="#555555",
            penwidth=1.5,
            arrowsize=0.8
        ];
    """

    node_counter = 0

    for lhs, rhs in fds:

        lhs_text = ", ".join(sorted(lhs))

        lhs_id = f"lhs_{node_counter}"

        graph += f'''
            {lhs_id} [
                label="{lhs_text}",
                fillcolor="#DCEBFF"
            ];
        '''

        for attribute in sorted(rhs):

            safe_attribute = (
                attribute
                .replace(" ", "_")
                .replace("-", "_")
            )

            rhs_id = (
                f"rhs_{node_counter}_{safe_attribute}"
            )

            graph += f'''
                {rhs_id} [
                    label="{attribute}",
                    fillcolor="#E8F5E9"
                ];

                {lhs_id} -> {rhs_id};
            '''

        node_counter += 1

    graph += "}"

    return graph


# ============================================================
# FORMAT ATTRIBUTE SET
# ============================================================

def format_attributes(attributes):

    return ", ".join(
        sorted(attributes)
    )


# ============================================================
# PAGE CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666666;
        margin-bottom: 20px;
    }

    .schema-box {
        border: 1px solid #d0d0d0;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 10px;
        background-color: #fafafa;
    }

    .schema-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .attribute {
        padding: 5px 0;
        font-size: 16px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '🗄️ Database Normalization Analyzer'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze functional dependencies, candidate keys, '
    'normal forms and automatic decomposition.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🧪 Sample Cases")

    selected = st.selectbox(
        "Choose an example",
        list(SAMPLE_CASES.keys()),
        index=list(
            SAMPLE_CASES.keys()
        ).index(
            st.session_state.selected_case
        )
    )

    if selected != st.session_state.selected_case:

        st.session_state.selected_case = selected

        load_sample_case()

        st.rerun()


    if selected != "Custom Input":

        st.success(
            "Sample case loaded."
        )


    st.divider()


    st.header("📚 What this tool does")

    st.write(
        """
        This analyzer performs:

        🔑 Candidate Key Detection

        ⚠️ Partial Dependency Detection

        ⚠️ Transitive Dependency Detection

        1️⃣ 1NF Analysis

        2️⃣ 2NF Analysis

        3️⃣ 3NF Analysis

        🔗 Dependency Graph

        🔨 Automatic Decomposition
        """
    )


    st.divider()

    st.caption(
        "Interactive Database Normalization "
        "Analyzer & Decomposition Simulator"
    )


# ============================================================
# INPUT SECTION
# ============================================================

st.header("1️⃣ Define Relation")

attribute_input = st.text_input(
    "Enter relation attributes",
    key="attributes_input",
    placeholder=(
        "Example: StudentID, StudentName, "
        "DepartmentID, DepartmentName"
    )
)


st.header("2️⃣ Define Functional Dependencies")

st.caption(
    "Enter one functional dependency per line."
)

st.code(
    "StudentID -> StudentName, DepartmentID\n"
    "DepartmentID -> DepartmentName"
)

fd_input = st.text_area(
    "Functional Dependencies",
    key="fds_input",
    height=150,
    placeholder=(
        "StudentID -> StudentName, DepartmentID\n"
        "DepartmentID -> DepartmentName"
    )
)


st.header("3️⃣ First Normal Form")

atomic_values = st.checkbox(
    "All attribute values are atomic (single-valued)",
    key="atomic_input"
)


st.divider()


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze = st.button(
    "🔍 Analyze Normalization",
    type="primary",
    use_container_width=True
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze:

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not attribute_input.strip():

        st.error(
            "❌ Please enter relation attributes."
        )

        st.stop()


    if not fd_input.strip():

        st.error(
            "❌ Please enter functional dependencies."
        )

        st.stop()


    # --------------------------------------------------------
    # PARSE ATTRIBUTES
    # --------------------------------------------------------

    attributes = {
        item.strip()
        for item in attribute_input.split(",")
        if item.strip()
    }


    if not attributes:

        st.error(
            "❌ No valid attributes found."
        )

        st.stop()


    # --------------------------------------------------------
    # PARSE FUNCTIONAL DEPENDENCIES
    # --------------------------------------------------------

    fds = []

    for line in fd_input.splitlines():

        line = line.strip()

        if not line:
            continue


        if "->" not in line:

            st.error(
                f"❌ Invalid dependency: `{line}`"
            )

            st.stop()


        lhs, rhs = line.split(
            "->",
            1
        )


        lhs_attributes = {
            item.strip()
            for item in lhs.split(",")
            if item.strip()
        }


        rhs_attributes = {
            item.strip()
            for item in rhs.split(",")
            if item.strip()
        }


        if not lhs_attributes or not rhs_attributes:

            st.error(
                f"❌ Invalid dependency: `{line}`"
            )

            st.stop()


        # ----------------------------------------------------
        # UNKNOWN ATTRIBUTE CHECK
        # ----------------------------------------------------

        unknown = (
            lhs_attributes |
            rhs_attributes
        ) - attributes


        if unknown:

            st.error(
                "❌ These attributes are not part "
                "of the relation: "
                + ", ".join(sorted(unknown))
            )

            st.stop()


        fds.append(
            (
                lhs_attributes,
                rhs_attributes
            )
        )


    # ========================================================
    # RUN ANALYZER
    # ========================================================

    result = analyze_normalization(
        attributes,
        fds
    )


    # ========================================================
    # 1NF
    # ========================================================

    result["1NF"] = atomic_values


    if not result["1NF"]:

        result["2NF"] = False
        result["3NF"] = False

        result["highest_normal_form"] = (
            "Not in 1NF"
        )

    elif not result["2NF"]:

        result["highest_normal_form"] = "1NF"

    elif not result["3NF"]:

        result["highest_normal_form"] = "2NF"

    else:

        result["highest_normal_form"] = "3NF"


    # ========================================================
    # RESULTS
    # ========================================================

    st.divider()

    st.header("📊 Analysis Result")


    # ========================================================
    # CANDIDATE KEYS
    # ========================================================

    st.subheader("🔑 Candidate Keys")

    if result["candidate_keys"]:

        key_columns = st.columns(
            min(
                len(result["candidate_keys"]),
                4
            )
        )

        for index, key in enumerate(
            result["candidate_keys"]
        ):

            with key_columns[
                index % len(key_columns)
            ]:

                st.success(
                    "{ "
                    + format_attributes(key)
                    + " }"
                )

    else:

        st.error(
            "No candidate key found."
        )


    # ========================================================
    # NORMAL FORM STATUS
    # ========================================================

    st.subheader("📋 Normal Form Status")

    col1, col2, col3 = st.columns(3)


    with col1:

        if result["1NF"]:
            st.success("1NF  ✅")
        else:
            st.error("1NF  ❌")


    with col2:

        if result["2NF"]:
            st.success("2NF  ✅")
        else:
            st.error("2NF  ❌")


    with col3:

        if result["3NF"]:
            st.success("3NF  ✅")
        else:
            st.error("3NF  ❌")


    st.info(
        "🏆 Highest Normal Form: "
        f"**{result['highest_normal_form']}**"
    )


    # ========================================================
    # EXPLANATION
    # ========================================================

    st.subheader("💡 Analysis Explanation")

    if not result["1NF"]:

        st.error(
            "The relation is not in 1NF because "
            "one or more attributes may contain "
            "non-atomic values."
        )

    elif not result["2NF"]:

        st.warning(
            "2NF fails because partial dependencies "
            "exist. A non-prime attribute depends "
            "on only part of a composite candidate key."
        )

    elif not result["3NF"]:

        st.warning(
            "3NF fails because a transitive dependency "
            "exists. A non-key attribute determines "
            "another non-key attribute."
        )

    else:

        st.success(
            "The relation satisfies 3NF. "
            "No partial or transitive dependency "
            "was detected."
        )


    # ========================================================
    # PARTIAL DEPENDENCIES
    # ========================================================

    st.subheader("⚠️ Partial Dependencies")

    if result["partial_dependencies"]:

        for lhs, rhs, key in result[
            "partial_dependencies"
        ]:

            st.warning(
                f"**{{{format_attributes(lhs)}}} "
                f"→ {{{format_attributes(rhs)}}}**  "
                f"(Key: "
                f"{{{format_attributes(key)}}})"
            )

    else:

        st.success(
            "No partial dependencies found."
        )


    # ========================================================
    # TRANSITIVE DEPENDENCIES
    # ========================================================

    st.subheader("⚠️ Transitive Dependencies")

    if result["transitive_dependencies"]:

        for lhs, rhs in result[
            "transitive_dependencies"
        ]:

            st.warning(
                f"**{{{format_attributes(lhs)}}} "
                f"→ {{{format_attributes(rhs)}}}**"
            )

    else:

        st.success(
            "No transitive dependencies found."
        )


    # ========================================================
    # DEPENDENCY GRAPH
    # ========================================================

    st.divider()

    st.header("🔗 Functional Dependency Graph")

    st.caption(
        "Blue nodes represent determinants. "
        "Green nodes represent dependent attributes."
    )

    graph = create_dependency_graph(fds)

    st.graphviz_chart(
        graph,
        use_container_width=True
    )


    # ========================================================
    # DECOMPOSITION
    # ========================================================

    st.divider()

    st.header("🔨 Suggested Decomposition")


    decomposition = get_suggested_decomposition(
        attributes,
        fds,
        result
    )


    if not decomposition["required"]:

        st.success(
            "✅ No decomposition required. "
            "The relation is already in 3NF."
        )

    else:

        st.warning(
            "Decomposition Required: "
            f"**YES**"
        )

        st.write(
            "**Target Normal Form:** "
            f"{decomposition['normalization_level']}"
        )

        st.write(
            "**Reason:** "
            f"{decomposition['reason']}"
        )


        tables = decomposition["tables"]


        # ====================================================
        # BEFORE / AFTER
        # ====================================================

        st.subheader("📐 Before vs After")


        before_col, after_col = st.columns(2)


        # ----------------------------------------------------
        # BEFORE
        # ----------------------------------------------------

        with before_col:

            st.markdown(
                "### 🔴 Original Relation"
            )

            st.markdown(
                '<div class="schema-box">',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="schema-title">'
                'RELATION'
                '</div>',
                unsafe_allow_html=True
            )

            for attribute in sorted(attributes):

                st.markdown(
                    f'<div class="attribute">'
                    f'🔹 {attribute}'
                    f'</div>',
                    unsafe_allow_html=True
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


        # ----------------------------------------------------
        # AFTER
        # ----------------------------------------------------

        with after_col:

            st.markdown(
                "### 🟢 Decomposed Relations"
            )


            for index, table in enumerate(tables):

                st.markdown(
                    '<div class="schema-box">',
                    unsafe_allow_html=True
                )

                table_type = table.get(
                    "type",
                    "Normalized Relation"
                )

                st.markdown(
                    f'<div class="schema-title">'
                    f'TABLE {index + 1}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                st.caption(
                    table_type
                )


                for attribute in sorted(
                    table["attributes"]
                ):

                    st.markdown(
                        f'<div class="attribute">'
                        f'🔹 {attribute}'
                        f'</div>',
                        unsafe_allow_html=True
                    )


                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )


        # ====================================================
        # NORMALIZED TABLES
        # ====================================================

        st.subheader(
            "🗃️ Normalized Schema"
        )

        table_columns = st.columns(
            min(len(tables), 3)
        )


        for index, table in enumerate(tables):

            with table_columns[
                index % len(table_columns)
            ]:

                st.markdown(
                    f"### Table {index + 1}"
                )

                st.caption(
                    table.get(
                        "type",
                        "Normalized Relation"
                    )
                )

                for attribute in sorted(
                    table["attributes"]
                ):

                    st.write(
                        f"🔹 {attribute}"
                    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Interactive Database Normalization Analyzer "
    "& Decomposition Simulator"
)
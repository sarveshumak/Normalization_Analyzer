# Interactive Database Normalization Analyzer & Decomposition Simulator

An interactive web-based tool that analyzes a relational schema for normalization from **1NF to 3NF** and provides decomposition suggestions based on functional dependencies.

## 🚀 Live Demo

https://normalizationanalyzer-3mk3phhtcte29jpwyxtulf.streamlit.app/

## 📌 Project Overview

Database normalization is an important process in relational database design. It helps reduce data redundancy, avoid update anomalies, and improve the overall structure of a database.

This project provides an interactive **Database Normalization Analyzer** where users can enter relation attributes and functional dependencies. The system automatically analyzes the relation and determines its normalization level up to **3NF**.

## 🎯 Objectives

- Analyze relational schemas for normalization.
- Identify candidate keys automatically.
- Check whether a relation satisfies 1NF, 2NF, and 3NF.
- Detect partial dependencies.
- Detect transitive dependencies.
- Suggest suitable decompositions.
- Visualize functional dependencies using a dependency graph.
- Provide a before-and-after view of normalization.
- Make normalization concepts easier to understand through an interactive interface.

## ✨ Key Features

### 1. Relation Input

Users can enter the attributes of a relation.

Example:

```text
StudentID, StudentName, DepartmentID, DepartmentName
```

### 2. Functional Dependency Input

Users can enter functional dependencies such as:

```text
StudentID -> StudentName, DepartmentID
DepartmentID -> DepartmentName
```

### 3. Candidate Key Detection

The system automatically calculates candidate keys using **attribute closure**.

### 4. 1NF Analysis

The application checks whether the relation contains atomic values.

### 5. 2NF Analysis

The system identifies partial dependencies involving proper subsets of composite candidate keys.

### 6. 3NF Analysis

The system analyzes transitive dependencies and identifies possible 3NF violations.

### 7. Dependency Graph

Functional dependencies are displayed visually using a dependency graph.

### 8. Decomposition Suggestions

When a normalization violation is detected, the application suggests decomposed relations.

### 9. Before vs After View

The application displays the original relation and the suggested normalized relations for comparison.

### 10. Sample Cases

The application provides predefined examples for:

- 2NF violation
- 3NF violation
- Already normalized relation
- Composite key scenario

## 🧠 Normalization Concepts

### First Normal Form (1NF)

A relation is in 1NF when all attributes contain atomic values and there are no repeating groups.

### Second Normal Form (2NF)

A relation must:

- Be in 1NF.
- Have no partial dependency of a non-prime attribute on a proper subset of a candidate key.

### Third Normal Form (3NF)

A relation must:

- Be in 2NF.
- Avoid inappropriate transitive dependencies between non-key attributes.

The analyzer uses functional dependencies and candidate-key information to identify potential 3NF violations.

## ⚙️ How the Analyzer Works

```text
User Input
    ↓
Relation Attributes
    ↓
Functional Dependencies
    ↓
Attribute Closure
    ↓
Candidate Key Detection
    ↓
1NF Analysis
    ↓
Partial Dependency Analysis
    ↓
2NF Analysis
    ↓
Transitive Dependency Analysis
    ↓
3NF Analysis
    ↓
Decomposition Suggestion
    ↓
Visualization & Report
```

## 🔑 Candidate Key Detection

The application uses the concept of **attribute closure**.

For a set of attributes X:

```text
X+
```

represents all attributes that can be functionally determined from X.

If:

```text
X+ = All attributes of the relation
```

then X is a superkey.

The application further checks minimality to determine whether the superkey is a **candidate key**.

## 🧩 Example

Consider the relation:

```text
Student(StudentID, StudentName, DepartmentID, DepartmentName)
```

Functional dependencies:

```text
StudentID -> StudentName, DepartmentID
DepartmentID -> DepartmentName
```

The system identifies:

```text
Candidate Key:
StudentID
```

The dependency:

```text
DepartmentID -> DepartmentName
```

creates a transitive dependency:

```text
StudentID -> DepartmentID -> DepartmentName
```

Therefore, the relation is identified as having a **3NF violation**.

A possible decomposition is:

```text
Student(StudentID, StudentName, DepartmentID)

Department(DepartmentID, DepartmentName)
```

## 🏗️ Project Structure

```text
Normalization_Analyzer/
│
├── app.py
│       └── Streamlit user interface
│
├── normalizer.py
│       └── Normalization and functional dependency logic
│
├── requirements.txt
│       └── Required Python packages
│
├── .gitignore
│       └── Ignored files and folders
│
└── README.md
        └── Project documentation
```

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| Streamlit | Interactive web interface |
| Graphviz | Dependency graph visualization |
| Git | Version control |
| GitHub | Source code hosting |
| Streamlit Community Cloud | Web deployment |

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/sarveshumak/Normalization_Analyzer.git
```

### 2. Open the project folder

```bash
cd Normalization_Analyzer
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Streamlit application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## 📊 Sample Test Cases

### Example 1 — 2NF Violation

Attributes:

```text
StudentID, CourseID, StudentName, CourseName
```

Functional Dependencies:

```text
StudentID -> StudentName
CourseID -> CourseName
```

Candidate Key:

```text
(StudentID, CourseID)
```

The application detects partial dependencies and suggests decomposition.

### Example 2 — 3NF Violation

Attributes:

```text
StudentID, StudentName, DepartmentID, DepartmentName
```

Functional Dependencies:

```text
StudentID -> StudentName, DepartmentID
DepartmentID -> DepartmentName
```

The application detects a transitive dependency and suggests decomposition.

### Example 3 — Already in 3NF

Attributes:

```text
StudentID, StudentName
```

Functional Dependency:

```text
StudentID -> StudentName
```

The relation satisfies 1NF, 2NF, and 3NF.

## 🔮 Future Enhancements

Possible future improvements include:

- BCNF analysis
- 4NF and 5NF support
- Lossless-join decomposition verification
- Dependency-preservation verification
- More advanced functional dependency inference
- Interactive table data entry
- Database integration using SQLite
- Exportable normalization reports
- More visualization options
- Improved formal 3NF checking

## 👥 Project Team

This project was developed as part of an academic database project.

**Team Size:** 4 Members

## 📄 License

This project is developed for academic and educational purposes.
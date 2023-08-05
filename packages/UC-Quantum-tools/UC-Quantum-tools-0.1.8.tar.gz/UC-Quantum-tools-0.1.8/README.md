# UCQ_tools
## Resources
- PyPi: See the project on pypi for the download at: https://pypi.org/project/UC-Quantum-tools/
- GitHub: See the project repo at: https://github.com/UC-Advanced-Research-Computing/UC-Quantum-tools

## Bugs
If you encounter a bug please make an issue in the "issues" tab above. This is a maintained repo and we will respond.

## Contributing
Anyone who wants to contribute to the code, please do. Download the code, modify it, and create a pull request.

## Available Functions
- Functions from `UC_Quantum_Lab.commands`
    - `state`
        - **Description**: Displays a vector in vscode if using the UC_Quantum_Lab vscode extension. And no matter where you are using this function it will return the state vector as a list.
        - **inputs**:
            - `circuit:QuantumCircuit`: a qiskit quantum circuit **with no measurements in it**.
            - `show:boolean` (optional): a boolean indicating if you want to display the statevector in the UC_Quantum_Lab vscode extension (default is yes if using the extension).
        - **returns**:
            - `statevector:list`: the statevector of the circuit in little endian format (this is how qiskit orders bits) in list form. You do not have to use this return (just do not assign it to a variable).
        - **NOTE**: this function can be multiple times (whenever you can this function the statevector of the circuit up to the call will be created).
        - **Example Useage**
            ```python
            from UC_Quantum_Lab.commands import state
            import qiskit
            quantumcircuit = qiskit.QuantumCircuit(2, 2)

            statevector = state(quantumciruit, show=True)
            # or 
            statevector = state(quantumciruit)
            # or 
            state(quantumciruit)
            ```
    - `display`
        - **Description**: Displays a circuit diagram in vscode if using the UC_Quantum_Lab vscode extension. If you are not using the vscode extension, then:
            - if you provide input *path* then the circuit diagram will be saved to that path.
            - if you do *not* input *path* then a matplotlib figure will pop up.
        - **inputs**:
            - `circuit:QuantumCircuit`: a qiskit quantum circuit.
            - `path:string` (optional): a string path that you want to save the figure to.
            - **NOTE**: if you are not using this function with the UC_Quantum_Lab vscode extension and you do not provide the path then a matplotlib figure will pop up.
        - **returns**: (nothing)
        - **NOTE**: this function can be multiple times and it will just generate more images (whenever you can this function a diagram of the circuit up to the call will be created).
        - **Example Useage**
            ```python
            from UC_Quantum_Lab.commands import display
            import qiskit
            quantumcircuit = qiskit.QuantumCircuit(2, 2)

            display(quantumciruit, path="local.png")
            # or 
            display(quantumciruit)
            ```
    - `counts`
        - **Description**: Displays a histogram in vscode if using the UC_Quantum_Lab vscode extension. If you are not using the vscode extension, then:
            - if you provide input *path* then the histogram will be saved to that path.
            - if you do *not* input *path* then a matplotlib figure will pop up.
        - **inputs**:
            - `circuit:QuantumCircuit`: a qiskit quantum circuit **that must have measurements in it**.
            - `backend:simulator` (optional): the simulator to execute the circuit on, default is IBM's qasm simulator. 
            - `path:string` (optional): a string path that you want to save the figure to.
            - `show:boolean` (optional): whether or not display the circuit, default is true. If false, then only the dictionary will be returned and nothing else will happen.
            - **NOTE**: if you are not using this function with the UC_Quantum_Lab vscode extension and you do not provide the path then a matplotlib figure will pop up.
        - **returns**:
            - `counts:dictionary`: the results of the simulation of the circuit as a dictionay where the keys are the binary strings and the values of the keys are the number of the times the binary string is the output of the circuit out of 1024. You do not have to use this return (just do not assign it to a variable).
        - **NOTE**: this function can be multiple times and it will just generate more images (and simulate the circuit at every call).
        - **Example Useage**
            ```python
            from UC_Quantum_Lab.commands import counts
            import qiskit
            quantumcircuit = qiskit.QuantumCircuit(2, 2)

            result = counts(
                quantumciruit, 
                backend=Aer.get_backend("statevector_simulator"),
                path="local.png"
            )
            # or 
            counts(quantumciruit, path="local.png")
            # or
            result = counts(quantumcircuit)
            # or
            counts(quantumcircuit)
            ```
- Functions from `UC_Quantum_Lab.layout`
    - `invert`
        - **Description**: This only works with the vscode extension UC_Quantum_Lab. Inverts the tiling of the extension's UI vertically and horizontally from default.
        - **inputs** (nothing)
        - **returns** (nothing)
        - **Example Useage**
            ```python
            from UC_Quantum_Lab.layout import invert
            invert()
            ```
    - `horizontal_invert`
        - **Description**: This only works with the vscode extension UC_Quantum_Lab. Inverts the tiling of the extension's UI horizontally from default.
        - **inputs** (nothing)
        - **returns** (nothing)
        - **Example Useage**
            ```python
            from UC_Quantum_Lab.layout import horizontal_invert
            horizontal_invert()
            ```
    - `vertical_invert`
        - **Description**: This only works with the vscode extension UC_Quantum_Lab. Inverts the tiling of the extension's UI vertically from default.
        - **inputs** (nothing)
        - **returns** (nothing)
        - **Example Useage**
            ```python
            from UC_Quantum_Lab.layout import vertical_invert
            vertical_invert()
            ```
    - `custom`
        - **Description**: This only works with the vscode extension UC_Quantum_Lab. Creates a custom webview from the inputted json using the format specified in https://github.com/brodkemd/UC_Quantum_Lab in the "*About json to html converter*" section.
        - **inputs**:
            - `layout_json:JSON`: json style object to set to the webviewer html.
        - **returns** (nothing)
        - **Example Useage**
            ```python
            from UC_Quantum_Lab.layout import custom
            custom({"left": "<h1>hello</h1>", "right" : "<h1>hello</h1>"})
            ```
        - **NOTE**: if you call this function before you call the inverts above the inverts will apply.



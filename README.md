```markdown
# Interactive Automate Script

## Purpose

The `interactive_automate.sh` script allows users to interactively input and execute code snippets in various programming languages. It supports Python, C, Rust, Go, Java, Kotlin, and Swift. The script captures code snippets, runs them, and handles errors by copying them to the clipboard. Each run of the script archives the previous code file for future reference.

## Features

- Supports multiple programming languages.
- Interactively accepts code snippets.
- Runs the code and displays the output.
- Copies errors to the clipboard.
- Archives old code files.

## Requirements

- Bash
- Appropriate compilers/interpreters for the supported languages:
  - Python: `python3`
  - C: `gcc`
  - Rust: `rustc`
  - Go: `go`
  - Java: `javac`, `java`
  - Kotlin: `kotlinc`, `java`
  - Swift: `swift`
- Clipboard tool:
  - Linux: `xclip`
  - macOS: `pbcopy`
  - Windows: `clip`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/interactive-automate.git
   cd interactive-automate
   ```

2. Make the script executable:

   ```bash
   chmod +x interactive_automate.sh
   ```

## Usage

To run the script, use the following command format:

```bash
./interactive_automate.sh <code_type> [clipboard_tool]
```

- `<code_type>`: The programming language of the code snippet (e.g., `python`, `c`, `rust`, `go`, `java`, `kotlin`, `swift`).
- `[clipboard_tool]`: Optional. Specify the clipboard tool if the default detection does not work.

### Example Usage

To run a Python snippet:

```bash
./interactive_automate.sh python
```

To run a C snippet with a custom clipboard tool:

```bash
./interactive_automate.sh c xclip
```
Also feel free to use the simple gui as a result of my typo in naming the file for initial commit.
```bash
python ./interactive_automate.py c xclip
```


### Interactive Code Input

1. The script will prompt you to enter your code snippet.
2. Enter the code line by line.
3. End the input with `#end of code` to execute the code.

### Sample Test Prompt

Here is a sample test prompt you can use to generate a Python code snippet:

```python
# This is a test Python script to demonstrate the interactive tool

def greet(name):
    print(f"Hello, {name}!")

def add(a, b):
    return a + b

if __name__ == "__main__":
    greet("World")
    result = add(5, 3)
    print(f"The result of adding 5 and 3 is {result}")
#end of code
```

### Example Output

When you run the script with the above Python snippet, you should see an output similar to the following:

```plaintext
Enter the python code snippet (end with '#end of code'):
You entered the following code:
# This is a test Python script to demonstrate the interactive tool

def greet(name):
    print(f"Hello, {name}!")

def add(a, b):
    return a + b

if __name__ == "__main__":
    greet("World")
    result = add(5, 3)
    print(f"The result of adding 5 and 3 is {result}")

Executing command: python3 code_snippet.py
Script output:
Hello, World!
The result of adding 5 and 3 is 8
No errors detected.
The current python file has been archived as code_snippet.bak1.py.
Enter the python code snippet (end with '#end of code'):
```

## Contributing

If you have any suggestions or improvements, feel free to create an issue or submit a pull request. Contributions are welcome!

## License

This project is licensed under the GPLv3 License. See the [LICENSE](LICENSE) file for details.
```

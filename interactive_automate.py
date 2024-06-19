#!/bin/bash

# Define variables
ERRORS_FILE="errors.log"
OUTPUT_FILE="output.log"

# Function to get the next backup number
get_next_bak_number() {
  local prefix=$1
  local max=0
  for file in ${prefix}*; do
    [[ $file =~ ${prefix}([0-9]+) ]] && ((max < ${BASH_REMATCH[1]})) && max=${BASH_REMATCH[1]}
  done
  echo $((max + 1))
}

# Function to detect OS and set clipboard tool
detect_os_and_set_clipboard_tool() {
  case "$(uname -s)" in
    Linux*)     CLIPBOARD_TOOL="xclip";;
    Darwin*)    CLIPBOARD_TOOL="pbcopy";;
    CYGWIN*|MINGW32*|MSYS*|MINGW*) CLIPBOARD_TOOL="clip";;
    *)          echo "Unknown OS. Please provide a clipboard tool as a parameter."; exit 1;;
  esac
}

# Check if a clipboard tool is provided as a parameter
if [ -n "$2" ]; then
  CLIPBOARD_TOOL="$2"
else
  detect_os_and_set_clipboard_tool
fi

# Check if code type is provided
if [ -z "$1" ]; then
  echo "Please provide the code type as the first parameter (python, c, rust, go, java, kotlin, swift)."
  exit 1
fi

# Set file extensions and commands based on code type
case "$1" in
  python)
    FILE_EXT="py"
    RUN_CMD="python3"
    ;;
  c)
    FILE_EXT="c"
    RUN_CMD="gcc -o code_snippet code_snippet.c && ./code_snippet"
    ;;
  rust)
    FILE_EXT="rs"
    RUN_CMD="rustc code_snippet.rs && ./code_snippet"
    ;;
  go)
    FILE_EXT="go"
    RUN_CMD="go run code_snippet.go"
    ;;
  java)
    FILE_EXT="java"
    RUN_CMD="javac code_snippet.java && java code_snippet"
    ;;
  kotlin)
    FILE_EXT="kt"
    RUN_CMD="kotlinc code_snippet.kt -include-runtime -d code_snippet.jar && java -jar code_snippet.jar"
    ;;
  swift)
    FILE_EXT="swift"
    RUN_CMD="swift code_snippet.swift"
    ;;
  *)
    echo "Unsupported code type: $1"
    exit 1
    ;;
esac

CODE_FILE="code_snippet.${FILE_EXT}"
BAK_PREFIX="code_snippet.bak"

# Interactive loop
while true; do
  # Query for code snippet
  echo "Enter the $1 code snippet (end with '#end of code'):"
  CODE_SNIPPET=""
  while IFS= read -r line; do
    [[ "$line" == "#end of code" ]] && break
    CODE_SNIPPET+="$line"$'\n'
  done

  # Exit loop if no input
  if [[ -z "$CODE_SNIPPET" ]]; then
    echo "No input provided. Exiting..."
    break
  fi

  # Echo the input code back to the user
  echo "You entered the following code:"
  echo "$CODE_SNIPPET"

  # Save code snippet to the appropriate file
  echo "$CODE_SNIPPET" > "$CODE_FILE"

  # Display the command to be executed for debugging
  echo "Executing command: $RUN_CMD $CODE_FILE"

  # Run the code file and capture output and errors
  eval "$RUN_CMD $CODE_FILE" > "$OUTPUT_FILE" 2> "$ERRORS_FILE"

  # Echo the output of running the script
  echo "Script output:"
  cat "$OUTPUT_FILE"

  # Check if there are any errors
  if [ -s "$ERRORS_FILE" ]; then
    # Move errors into the clipboard
    if command -v $CLIPBOARD_TOOL &> /dev/null; then
      if [[ "$CLIPBOARD_TOOL" == "xclip" ]]; then
        cat "$ERRORS_FILE" | $CLIPBOARD_TOOL -selection clipboard
      else
        cat "$ERRORS_FILE" | $CLIPBOARD_TOOL
      fi
    else
      echo "Clipboard tool $CLIPBOARD_TOOL not found. Please install it or update the script to use your system's clipboard tool."
      exit 1
    fi
    echo "Errors have been copied to the clipboard."
    echo "Script errors:"
    cat "$ERRORS_FILE"
  else
    echo "No errors detected."
  fi

  # Get the next backup number
  BAK_NUMBER=$(get_next_bak_number "$BAK_PREFIX")

  # Archive the old code file
  mv "$CODE_FILE" "${BAK_PREFIX}${BAK_NUMBER}.${FILE_EXT}"

  echo "The current $1 file has been archived as ${BAK_PREFIX}${BAK_NUMBER}.${FILE_EXT}."
done

echo "Script execution completed."

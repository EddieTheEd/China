

#! /bin/sh

# Example: bash run.sh env Environment

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <path> <name>"
    exit 1
fi

cd scripts
source chinaenv/bin/activate
python3 anki3.py "$2" "${1}.txt"
deactivate
cd ..

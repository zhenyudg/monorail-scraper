from enforce_py_version import enforce_py_version

'''
How to use the manual issue serializer:

Input: a copy and pasted block of text from an OSS-Fuzz Monorail issue.
Output: A JSON serialization of the issue.

What information to copy:
Select everything from the issue header (containing the issue number) to the last comment.

I copy-pasted from Google Chrome 83 on macOS. Different setups may yield different pasted text that might bork the script.
'''



if __name__ == '__main__':
    enforce_py_version()

    raw_text = input("Copy and paste text from an OSS-Fuzz Monorail issue."
                     "Select everything from the Issue number in the header to the last comment,"
                     "copy, then paste into stdin.\n")


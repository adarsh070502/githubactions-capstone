from pathlib import Path
import re

def main(starting_path, identifier_comment, exclude_files, new_tag):
    dir_path = Path(starting_path)

    yaml_files = list(dir_path.rglob("*.yml")) + list(dir_path.rglob("*.yaml"))

    # Regex:
    # - capture indentation
    # - capture "version:"
    # - capture version value
    # - keep comment intact
    version_pattern = re.compile(
        rf'^(\s*version:\s*)([^\s#]+)(\s*#\s*{re.escape(identifier_comment)}.*)$'
    )

    print("No of yaml files found:", len(yaml_files))
    
    for file in yaml_files:
        if file in exclude_files:
            continue
        try:
            lines = file.read_text(encoding="utf-8").splitlines(keepends=True)
        except UnicodeDecodeError:
            continue

        changed = False
        new_lines = []

        for line in lines:
            match = version_pattern.match(line)
            if match:
                prefix, old_version, suffix = match.groups()
                line = f"{prefix}{new_tag}{suffix}\n"
                changed = True
            new_lines.append(line)

        if changed:
            file.write_text("".join(new_lines), encoding="utf-8")
            print(f"Updated: {file}")
        
if __name__ == "__main__":
    print("In python file")
    import argparse
    
    # 1. Create the Argument Parser
    parser = argparse.ArgumentParser(
        description="Inputs for updating manifest files"
    )

    # 2. Add Arguments

    # A. The Single String (e.g., a username)
    parser.add_argument(
        "--starting_path",
        type=str,
        required=True,
        help="Starting path"
    )
    
    parser.add_argument(
        "--new_tag",
        type=str,
        required=True,
        help="New Tag"
    )

    parser.add_argument(
        "--identifier_comment",
        nargs='+',  # Key: '+' means 1 or more arguments are expected, and they are collected into a list.
        type=str,
        required=False,
        help="Identifier Comment"
    )
    
    parser.add_argument(
        "--exclude_files",
        nargs='+',  # Key: '+' means 1 or more arguments are expected, and they are collected into a list.
        type=str,
        required=False,
        help="A list of files to exclude"
    )

    # 3. Parse the Arguments
    args = parser.parse_args()
    
    
    starting_path = args.starting_path
    identifier_comment = args.identifier_comment
    exclude_files = args.exclude_files
    new_tag = args.new_tag
    
    if starting_path is None or starting_path == "":
        raise Exception("Provide starting directory")
    if identifier_comment is None or identifier_comment == "":
        raise Exception("Provide identifier comment")
    if new_tag is None or new_tag == "":
        raise Exception("Provide new tag")
    if exclude_files is None or exclude_files == "":
        exclude_files = []
        
    print(starting_path)
    print(exclude_files)
    print(new_tag)
    identifier_comment = " ".join(identifier_comment) #identifier_comment[0].strip()
    identifier_comment = identifier_comment.lstrip("# ").strip()
    print(f"identifier_comment: ",identifier_comment)
    main(starting_path, identifier_comment, exclude_files, new_tag)

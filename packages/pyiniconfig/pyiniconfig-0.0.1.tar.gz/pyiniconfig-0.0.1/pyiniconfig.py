import os
import ast


def _find_chars_positions(search_string: str, chars: list) -> dict:
    """Find positions of given chars in string"""

    positions_dict = {}
    for char in chars:
        assert len(char) == 1, "Char length can't be greater than 1."

        chars_positions = []
        for index, string_char in enumerate(search_string):

            if string_char == char:
                chars_positions.append(index)

        positions_dict[char] = chars_positions

    return positions_dict


def _get_section(supposed_section: str) -> str:
    """Return section name if string is section else raise error"""

    supposed_section_string = supposed_section

    # Remove comment if it's exist
    supposed_section_chars = _find_chars_positions(supposed_section_string, [";", "#"])

    if supposed_section_chars[";"] or supposed_section_chars["#"]:
        min_comment_index = None

        if supposed_section_chars[";"]:

            if not min_comment_index or min_comment_index > min(supposed_section_chars[";"]):
                min_comment_index = min(supposed_section_chars[";"])

        if supposed_section_chars["#"]:

            if not min_comment_index or min_comment_index > min(supposed_section_chars["#"]):
                min_comment_index = min(supposed_section_chars["#"])

        if min_comment_index:
            supposed_section_string = supposed_section_string[0:min_comment_index]

    # Check if "=" char in section line
    supposed_section_chars = _find_chars_positions(supposed_section_string, ["="])
    assert not len(supposed_section_chars["="]), "Char \"=\" is prohibited to use on section line."

    # Check is section is closed
    supposed_section_chars = _find_chars_positions(supposed_section_string, ["[", "]"])
    assert len(supposed_section_chars["["]) == len(supposed_section_chars["]"]) and len(supposed_section_chars["["]) == 1, "Amount of \"[\" and \"]\" have to be 1."

    return supposed_section_string[supposed_section_chars["["][0] + 1:supposed_section_chars["]"][0]]


class IniConfig:

    def __init__(self, config_path: str) -> None:
        """Class constructor"""

        self.config_path = config_path.strip() if config_path.strip().endswith(".ini") else config_path.strip() + ".ini"

        # Create config if it doesn't exist
        try:

            if not os.path.exists(self.config_path):

                with open(self.config_path, "a") as file:
                    file.close()

        except Exception as error:
            raise Exception(f"Could not create config file in config path.\n{error}")

    # Misc methods
    def remove(self) -> None:
        """Remove config"""

        os.remove(self.config_path)
        del self

    # Sections methods
    def get_sections(self, debug: bool = False) -> list:
        """List all section in config

        Return tuple (name, string_number) if debig arg is True else return names list"""

        with open(self.config_path, "r", encoding="utf-8") as file:
            file_lines = [line.strip(" ") for line in file]

        if file_lines:

            # Remove empty chars in the end of the file
            while file_lines and not file_lines[-1].strip():
                del file_lines[-1]

            # Remove empty chars in the begin of the file
            while file_lines and not file_lines[0].strip():
                del file_lines[0]

        # Append string separator to the end
        if file_lines:

            if not file_lines[-1].endswith("\n"):
                file_lines[-1] = file_lines[-1] + "\n"

        # Rewrite config file
        with open(self.config_path, "w", encoding="utf-8") as file:
            file.write("".join(file_lines))

        sections = []
        for index, line in enumerate(file_lines):

            if line.strip().startswith("["):
                sections.append((_get_section(line.strip()), index + 1))

        # Remove numbers of lines
        sections = [section[0] for section in sections] if not debug else sections

        return sections

    def set_section(self, section_name: str, comment: str = None) -> None:
        """Add section with specified name to config"""

        current_sections = [section[0] for section in self.get_sections(True)]

        if section_name in current_sections:
            raise Exception(f"Section with '{section_name}' name already exists.")

        prohibited_chars = [";", "#", "="]
        for prohibited_char in prohibited_chars:
            assert prohibited_char not in section_name, f"'{prohibited_char}' char is prohibited to use in section name."

        with open(self.config_path, "r", encoding="utf-8") as file:
            file_lines = [line.strip(" ") for line in file]

        if file_lines:

            # Remove empty chars in the end of the file
            while file_lines and not file_lines[-1].strip():
                del file_lines[-1]

            # Remove empty chars in the begin of the file
            while file_lines and not file_lines[0].strip():
                del file_lines[0]

        # Append string separator to the end
        if file_lines:

            if not file_lines[-1].endswith("\n"):
                file_lines[-1] = file_lines[-1] + "\n"

        # Rewrite config file
        with open(self.config_path, "w", encoding="utf-8") as file:
            file.write("".join(file_lines) + f"[{section_name}] ; {comment}" if comment else "".join(file_lines) + f"[{section_name}]")

    def rename_section(self, section_name: str, new_section_name: str) -> None:

        current_sections = [section[0] for section in self.get_sections(True)]

        if section_name not in current_sections:
            raise Exception(f"Section with '{section_name}' name not found.")

        if new_section_name in current_sections:
            raise Exception(f"Section with '{new_section_name}' name already exists.")

        prohibited_chars = [";", "#", "="]
        for prohibited_char in prohibited_chars:
            assert prohibited_char not in new_section_name, f'"{prohibited_char}" char is prohibited to use in section name.'

        with open(self.config_path, "r", encoding="utf-8") as file:
            file_lines = [line.strip(" ") for line in file]

        processed_file_lines = []
        for line in file_lines:

            if section_name in line.strip() and line.strip().startswith("["):
                processed_file_lines.append(line.replace(f"[{section_name}]", f"[{new_section_name}]"))

            else:
                processed_file_lines.append(line)

        if file_lines:

            # Remove empty chars in the end of the file
            while file_lines and not file_lines[-1].strip():
                del file_lines[-1]

            # Remove empty chars in the begin of the file
            while file_lines and not file_lines[0].strip():
                del file_lines[0]

        # Append string separator to the end
        if file_lines:

            if not file_lines[-1].endswith("\n"):
                file_lines[-1] = file_lines[-1] + "\n"

        # Rewrite config file
        with open(self.config_path, "w", encoding="utf-8") as file:
            file.write("".join(processed_file_lines))

    def remove_section(self, section_name: str) -> None:
        """Remove section"""

        current_sections = [section[0] for section in self.get_sections(True)]
        current_enumerated_sections = self.get_sections(True)

        if section_name not in current_sections:
            raise Exception(f"Section with '{section_name}' name not found.")

        with open(self.config_path, "r", encoding="utf-8") as file:
            file_lines = [line.strip(" ") for line in file]

        if current_sections and current_sections[-1] == section_name:

            for _ in range(len(file_lines) - current_enumerated_sections[-1][1] + 1):
                del file_lines[-1]

        else:
            for index, section in enumerate(current_enumerated_sections):

                if section[0] == section_name:
                    del file_lines[section[1] - 1:current_enumerated_sections[index + 1][1] - 1]

        if file_lines:

            # Remove empty chars in the end of the file
            while file_lines and not file_lines[-1].strip():
                del file_lines[-1]

            # Remove empty chars in the begin of the file
            while file_lines and not file_lines[0].strip():
                del file_lines[0]

        # Append string separator to the end
        if file_lines:

            if not file_lines[-1].endswith("\n"):
                file_lines[-1] = file_lines[-1] + "\n"

        # Rewrite config file
        with open(self.config_path, "w", encoding="utf-8") as file:
            file.write("".join(file_lines))

    # Options methods

    def get_options(self, section_name: str, debug: bool = False) -> dict:
        """List all options in selected section

        Return dict {"option": "value"}"""

        current_sections = [section[0] for section in self.get_sections(True)]
        current_enumerated_sections = self.get_sections(True)

        if section_name not in current_sections:
            raise Exception(f"Section with '{section_name}' name not found.")

        with open(self.config_path, "r", encoding="utf-8") as file:
            file_lines = [line.strip(" ") for line in file]

        options = {}
        prohibited_chars = ['&', '.', ')', '-', '?', '[', '!', '_', '\\', ']', '*', '+', "'", '|', '<', '#', '=', ',', '}', '(', '/', '{', '~;', ':', '@', '^', '№', '>']
        if current_sections and current_sections[-1] == section_name:
            options_section = file_lines[current_enumerated_sections[-1][1]:]

            for option in options_section:

                if option.strip() and not option.strip()[0] in prohibited_chars and option.strip().count("=") != 0:

                    if option.split("=")[1].strip():

                        try:
                            options[option.split("=")[0].strip()] = ast.literal_eval(option.split("=")[1].strip())

                        except Exception:
                            options[option.split("=")[0].strip()] = option.split("=")[1].strip()

                    else:
                        options[option.split("=")[0].strip()] = None

        else:

            for index, section in enumerate(current_enumerated_sections):

                if section[0] == section_name:
                    options_section = file_lines[section[1]:current_enumerated_sections[index + 1][1] - 1]

                    for option in options_section:

                        if option.strip() and not option.strip()[0] in prohibited_chars and option.strip().count("=") != 0:

                            if option.split("=")[1].strip():

                                try:
                                    options[option.split("=")[0].strip()] = ast.literal_eval(option.split("=")[1].strip())

                                except Exception:
                                    options[option.split("=")[0].strip()] = option.split("=")[1].strip()

                            else:
                                options[option.split("=")[0].strip()] = None

        return options

    def set_option(self, section_name: str, option_name: str, value: str = None, comment: str = None):

        current_sections = [section[0] for section in self.get_sections(True)]
        current_enumerated_sections = self.get_sections(True)

        if section_name not in current_sections:
            raise Exception(f"Section with '{section_name}' name not found.")

        prohibited_chars = ['&', '.', ')', '-', '?', '[', '!', '_', '\\', ']', '*', '+', "'", '|', '<', '#', '=', ',', '}', '(', '/', '{', '~;', ':', '@', '^', '№', '>']
        for prohibited_char in prohibited_chars:
            assert prohibited_char not in option_name, f"'{prohibited_char}' char is prohibited to use in option."

        with open(self.config_path, "r", encoding="utf-8") as file:
            file_lines = [line.strip(" ") for line in file]

        if current_sections and current_enumerated_sections[-1][0] == section_name:
            section_content = file_lines[current_enumerated_sections[-1][1]:]

            for line_index, option in enumerate(section_content):

                if option.split("=")[0].strip() == option_name.strip():
                    file_lines[current_enumerated_sections[-1][1] + line_index] = option_name + " =\n" if not value else option_name + f" = {value}\n"
                    break

            else:
                file_lines.insert(current_enumerated_sections[-1][1], option_name + " =\n") if not value else file_lines.insert(current_enumerated_sections[-1][1], option_name + f" = {value}\n")

                if comment:
                    file_lines.insert(current_enumerated_sections[-1][1], f"; {comment}\n")

        else:

            for index, section in enumerate(current_enumerated_sections):

                if section[0] == section_name:
                    section_content = file_lines[section[1]:current_enumerated_sections[index + 1][1] - 1]

                for line_index, option in enumerate(section_content):

                    if option.split("=")[0].strip() == option_name.strip():
                        file_lines[current_enumerated_sections[-1][1] + line_index] = option_name + " =\n" if not value else option_name + f" = {value}\n"
                        break

                else:
                    file_lines.insert(current_enumerated_sections[-1][1], option_name + " =\n") if not value else file_lines.insert(current_enumerated_sections[-1][1], option_name + f" = {value}\n")

                    if comment:
                        file_lines.insert(current_enumerated_sections[-1][1], f"; {comment}")

        if file_lines:

            # Remove empty chars in the end of the file
            while file_lines and not file_lines[-1].strip():
                del file_lines[-1]

            # Remove empty chars in the begin of the file
            while file_lines and not file_lines[0].strip():
                del file_lines[0]

        # Append string separator to the end
        if file_lines:

            if not file_lines[-1].endswith("\n"):
                file_lines[-1] = file_lines[-1] + "\n"

        # Rewrite config file
        with open(self.config_path, "w", encoding="utf-8") as file:
            file.write("".join(file_lines))

from crawl4md.utils.frames import print_main_header, print_sub_header, print_test_path


def snake_to_pascal(value: str) -> str:
    return "".join(part.capitalize() for part in value.split("_"))


def print_preprocessing_group_header(test_name: str, test_path: str) -> None:
    print_sub_header(test_name)
    print_test_path(test_path)


def print_heading(title: str, index: int = 1) -> None:
    print_main_header(f"{index}. {title}")

from ..src.duckduckgo_cli.main import (
    convert_argv_to_duckduckgo_link,
    open_duckduckgo_link_in_browser,
)


def test_convert_argv_to_duckduckgo_link() -> None:
    assert convert_argv_to_duckduckgo_link(["test"]) == "https://duckduckgo.com/?q=test"
    assert (
        convert_argv_to_duckduckgo_link(["!py3", "webbrowser"])
        == "https://duckduckgo.com/?q=!py3+webbrowser"
    )

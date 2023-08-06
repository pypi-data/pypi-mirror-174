import deephaven_plugin_plotly_js
from deephaven_plugin_plotly_js.__info__ import (
    __npm_org__,
    __npm_package__,
    __npm_version__,
)


def test_type():
    assert deephaven_plugin_plotly_js.PlotlyJs().type == "js"


def test_name():
    assert (
        deephaven_plugin_plotly_js.PlotlyJs().metadata["name"]
        == f"{__npm_org__}/{__npm_package__}"
    )


def test_version():
    assert (
        deephaven_plugin_plotly_js.PlotlyJs().metadata["version"]
        == f"{__npm_version__}"
    )


def test_main():
    assert deephaven_plugin_plotly_js.PlotlyJs().metadata["main"] == "dist/index.js"


def test_distribution_path():
    with deephaven_plugin_plotly_js.PlotlyJs().distribution_path() as distribution_path:
        assert distribution_path.is_dir()


def test_main_exists():
    with deephaven_plugin_plotly_js.PlotlyJs().distribution_path() as distribution_path:
        path = distribution_path / "dist" / "index.js"
        assert path.is_file()

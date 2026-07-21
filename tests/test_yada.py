import unittest
from unittest import mock

from dash_yada.Yada import YadaAIO, addScripts


def _get_child_by_subcomponent(component, subcomponent):
    for child in component.children:
        child_id = getattr(child, "id", None)
        if isinstance(child_id, dict) and child_id.get("subcomponent") == subcomponent:
            return child
    raise AssertionError(f"Could not find child with subcomponent={subcomponent}")


def _find_nested_child_by_subcomponent(component, subcomponent):
    child_id = getattr(component, "id", None)
    if isinstance(child_id, dict) and child_id.get("subcomponent") == subcomponent:
        return component

    children = getattr(component, "children", None)
    if children is None:
        return None

    if isinstance(children, (list, tuple)):
        child_items = children
    else:
        child_items = [children]

    for child in child_items:
        found = _find_nested_child_by_subcomponent(child, subcomponent)
        if found is not None:
            return found

    return None


class TestYada(unittest.TestCase):
    def test_add_scripts_collects_entries_from_pages(self):
        with mock.patch(
            "dash.page_registry",
            {
                "home": {"addScripts": {"Home": [{"target": "#home"}]}},
                "about": {"title": "About"},
                "docs": {"addScripts": {"Docs": [{"target": "#docs"}]}},
            },
        ):
            self.assertEqual(
                addScripts(),
                {
                    "Home": [{"target": "#home"}],
                    "Docs": [{"target": "#docs"}],
                },
            )

    def test_component_uses_page_registry_scripts_by_default(self):
        page_scripts = {"Tour": [{"target": "#title", "convo": "Hello"}]}
        with mock.patch("dash.page_registry", {"home": {"addScripts": page_scripts}}):
            component = YadaAIO(yada_id="yada-test")

        scripts_store = _get_child_by_subcomponent(component, "scripts")
        self.assertEqual(scripts_store.data, page_scripts)

    def test_component_defaults_and_offcanvas_style_merge(self):
        component = YadaAIO(
            yada_id="yada-test",
            steps_offcanvas_style={"backgroundColor": "black"},
        )

        hover_message = _get_child_by_subcomponent(component, "hover_message")
        self.assertEqual(hover_message.children[0].children, "yada")

        greeting_store = _get_child_by_subcomponent(component, "hover_message_greeting")
        self.assertIn("Your Automated Dashboard Assistant", greeting_store.data)

        offcanvas = _get_child_by_subcomponent(component, "_steps_offcanvas")
        self.assertEqual(offcanvas.style["flexDirection"], "column-reverse")
        self.assertEqual(offcanvas.style["backgroundColor"], "black")


if __name__ == "__main__":
    unittest.main()

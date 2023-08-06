from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Optional, Tuple, Union

from ..widget import Widget, AttributeNames, StateControl
from .panel import PanelWidget, Panel


@dataclass
class TabsLayout(Panel):

    tabs: Optional[Tuple[str, StateControl]] = field(default_factory=lambda: [])
    layout: Optional[Literal["top", "bottom" "left", "right"]] = "top"

    def add_tab(self, tab_title: str, component: StateControl) -> TabsLayout:
        my_list = list(self.tabs)
        my_list.append([tab_title, component])
        self.tabs = tuple(my_list)

        return self

    def remove_tab(self, index: Union[str, int]) -> TabsLayout:
        my_list = list(self.tabs)

        try:
            if isinstance(index, str):
                my_list.remove(index)
            elif isinstance(index, int):
                my_list.pop(index)
            else:
                raise ValueError(f"Error {TabsLayout.__name__}: wrong format for param index")
        except:
            raise ValueError(f"Error {TabsLayout.__name__}: wrong value for param index")

        self.tabs = tuple(my_list)
        return self


class TabsLayoutWidget(PanelWidget):
    """
    Creates a layout that provides a horizontal layout to display tabs.
    """

    def __init__(self,
                 panel_title: Optional[str] = None,
                 panel_id: Optional[str] = None,
                 tabs: Optional[Tuple[str, StateControl]] = field(default_factory=lambda: []),
                 layout: Optional[Literal["top", "bottom" "left", "right"]] = "top",
                 **additional):
        self._parent_class = TabsLayout.__name__
        self.tabs = tabs
        self.layout = layout
        super().__init__(panel_title, panel_id, **additional)
        TabsLayout.__init__(self, tabs, layout)
        self._compatibility: Tuple = (TabsLayout.__name__)
        self.placements = dict()

    def place(self, widget: Widget, tab_title: str = None):
        super()._place(widget)

    def to_dict_widget(self):
        panel_dict = super().to_dict_widget()

        for tab in self.tabs:
            print(tab)

        panel_dict[AttributeNames.PROPERTIES.value].update({
            AttributeNames.TABS.value: [{"title": tab[0], "component": tab[1]} for tab in self.tabs]
        })

        if (self.layout is not None):
            panel_dict[AttributeNames.LAYOUT.value].update({
                AttributeNames.LAYOUT.value: self.layout
            })

        return panel_dict

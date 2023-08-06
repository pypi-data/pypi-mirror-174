from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Optional, Tuple, Union

from ..widget import Widget, AttributeNames, StateControl
from .panel import PanelWidget, Panel


@dataclass
class TabsLayout(StateControl):

    tabs: Optional[Tuple[str, StateControl]] = field(default_factory=lambda: [])
    position: Optional[Literal["top", "bottom" "left", "right"]] = "bottom"

    def add_tab(self, tab_title: str, component: StateControl) -> TabsLayout:
        if (self.tabs is None):
            element = tab_title, component
            self.tabs = [element]
        else:
            my_list = list(self.tabs)
            element = tab_title, component
            my_list.append(element)
            self.tabs = tuple(my_list)

        return self

    def remove_tab(self, index: Union[str, int]) -> TabsLayout:
        my_list = list(self.tabs)

        try:
            if isinstance(index, str):
                index = self.getIndex(index)
                my_list.pop(index)
            elif isinstance(index, int):
                my_list.pop(index)
            else:
                raise ValueError(f"Error {TabsLayout.__name__}: wrong format for param index")
        except:
            raise ValueError(f"Error {TabsLayout.__name__}: wrong value for param index")

        self.tabs = tuple(my_list)
        return self

    def getIndex(self, name:str) -> int:
        my_list = list(self.tabs)

        try:
            enum_list = [(i, x) for i, x in enumerate(my_list, 0)]    
            i_list = [t[0] for t in enum_list if (t[1][0]==name)]
            return i_list[0]
        except:
            raise ValueError(f"Error {TabsLayout.__name__}: wrong value for string index")

class TabsLayoutWidget(PanelWidget,TabsLayout):
    """
    Creates a layout that provides a horizontal layout to display tabs.
    """

    def __init__(self,
                 panel_title: Optional[str] = None,
                 panel_id: Optional[str] = None,
                 tabs: Optional[Tuple[str, StateControl]] = None,
                 position: Optional[Literal["top", "bottom" "left", "right"]] = "bottom",
                 **additional):
        self._parent_class = TabsLayout.__name__
        self.tabs = tabs
        self.position = position
        super().__init__(panel_title, panel_id, **additional)
        TabsLayout.__init__(self, tabs, position)
        self._compatibility: Tuple = (TabsLayout.__name__)
        self.placements = dict()

    def place(self, widget: Widget, tab_title: str = None):
        super()._place(widget)

    def to_dict_widget(self):
        panel_dict = super().to_dict_widget()

        if (self.tabs is not None):
            panel_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.TABS.value: [{"title": tab[0], "component": tab[1]} for tab in self.tabs]
            })

        if (self.position is not None):
            panel_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.POSITION.value: self.position
            })

        return panel_dict

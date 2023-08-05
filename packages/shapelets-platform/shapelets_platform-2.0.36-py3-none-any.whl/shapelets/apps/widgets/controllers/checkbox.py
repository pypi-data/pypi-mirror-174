from dataclasses import dataclass
from typing import Optional

from ..widget import AttributeNames, Widget, StateControl


@dataclass
class Checkbox(StateControl):
    title: Optional[str] = None
    checked: Optional[bool] = None
    defaultChecked: Optional[bool] = None
    toggle: Optional[bool] = None


class CheckboxWidget(Widget, Checkbox):

    def __init__(self,
                 title: Optional[str] = None,
                 checked: Optional[bool] = None,
                 defaultChecked: Optional[bool] = None,
                 toggle: Optional[bool] = None,
                 **additional
                 ):
        Widget.__init__(self, Checkbox.__name__, **additional)
        Checkbox.__init__(self, title, checked, defaultChecked, toggle)

    def to_dict_widget(self):
        checkbox_dict = super().to_dict_widget()
        if self.title is not None:
            checkbox_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.TITLE.value: self.title
            })
        if self.checked:
            checkbox_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.CHECKED.value: self.checked
            })

        if self.defaultChecked:
            checkbox_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.DEFAULT.value: self.defaultChecked
            })

        if self.toggle:
            checkbox_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.TOGGLE.value: self.toggle
            })

        return checkbox_dict
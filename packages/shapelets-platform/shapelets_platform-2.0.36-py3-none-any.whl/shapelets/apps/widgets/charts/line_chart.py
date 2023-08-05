from __future__ import annotations

import numpy as np
import pandas as pd

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Union

from ....model import Sequence, View
from ..widget import AttributeNames, StateControl, Widget
from ..contexts import FilteringContext, TemporalContext
# from ..controllers import CollectionSelector, SequenceSelector

LineChartValueType = Union[
    List[Sequence], Sequence,
    List[int],
    List[float],
    List[str],
    np.ndarray
]


@dataclass
class LineChart(StateControl):
    title: Optional[str] = None
    value: Optional[LineChartValueType] = None
    views: Optional[List[View]] = field(default_factory=lambda: [])
    temporal_context: Optional[TemporalContext] = None
    filtering_context: Optional[FilteringContext] = None
    multi_line_chart: Optional[bool] = True
    _plots: List = field(default_factory=lambda: [])
    _is_type = None

    def __post_init__(self):
        # A subtype to differentiate between sequences or y_axis/x_axis. Requested by UI.
        self.linechart_sub_type = None
        self.sequence = None
        self.y_axis = None
        self.x_axis = None
        if isinstance(self.value, Sequence):
            self.linechart_sub_type = f"{AttributeNames.SEQUENCE.value.capitalize()}"
            self.sequence = self.value
        elif isinstance(self.value, List):
            self.linechart_sub_type = f"{LineChart.__name__}"
        elif isinstance(self.value, (np.ndarray, pd.Series)):
            self.linechart_sub_type = f"{AttributeNames.NUMPY_ARRAY.value.capitalize()}"
            self.y_axis = self.value
        elif isinstance(self.value, pd.DataFrame):
            self.linechart_sub_type = f"{AttributeNames.NUMPY_ARRAY.value.capitalize()}"
            if self.multi_line_chart:
                # Ignore text columns
                value = self.value.select_dtypes(include='number')
                for index, col in enumerate(value):
                    # Remove Nan
                    if value[col].isnull().values.any():
                        adjust_df = value[col].dropna()
                        self.plot(y_axis=adjust_df, x_axis=adjust_df.index.tolist(), lane_index=index, label=col)
                    else:
                        self.plot(y_axis=value[col], x_axis=value[col].index, lane_index=index, label=col)
            else:
                self.y_axis = self.value.iloc[:, 0]
                self.x_axis = self.value.index
        elif self.value is None:
            self.linechart_sub_type = "Empty"

    # TODO Adjust LineChart Type
    def from_sequences(self, sequences: List[Sequence]) -> LineChart:
        self.linechart_sub_type = f"{AttributeNames.SEQUENCE.value.capitalize()}"
        self.value = sequences
        return self

    def from_sequence(self, sequence: Sequence) -> LineChart:
        self.linechart_sub_type = f"{AttributeNames.SEQUENCE.value.capitalize()}"
        self.value = sequence
        return self

    def to_sequence(self) -> Sequence:
        return self.sequence

    def from_views(self, views: List[View]) -> LineChart:
        self.views = views
        return self

    def from_view(self, view: View) -> LineChart:
        self.views.append(view)
        return self

    def to_views(self) -> List[View]:
        return self.views

    def from_dataframe(self, dataframe: pd.DataFrame) -> LineChart:
        # TODO: save dataframe/transform
        self.value = dataframe
        return self

    def to_dataframe(self) -> pd.DataFrame:
        # TODO: transform sequence to dataframe
        return self.sequence

    def from_ndarray(self, ndarray: np.ndarray) -> LineChart:
        # TODO: save ndarray/transform
        self.linechart_sub_type = f"{AttributeNames.NUMPY_ARRAY.value.capitalize()}"
        self.value = ndarray
        return self

    def to_ndarray(self) -> np.ndarray:
        # TODO: transform sequence to ndarray
        return self.sequence

    def from_list(self, lst: list) -> LineChart:
        self.linechart_sub_type = f"{LineChart.__name__}"
        self.value = lst
        return self

    def to_list(self) -> pd.DataFrame:
        return self.y_axis

    def plot(self,
             y_axis: Union[List[int], List[float], np.ndarray, pd.Series] = None,
             x_axis: Union[List[int], List[float], List[str], np.ndarray] = None,
             sequence: Union[List[Sequence], Sequence] = None,
             label: str = None,
             lane_index: int = 0):
        plot_dict = {}

        plot_dict.update({AttributeNames.LANE_INDEX.value: lane_index})

        if sequence is not None:
            # Adjust subtype for UI
            self.linechart_sub_type = f"{AttributeNames.SEQUENCE.value.capitalize()}"
            # list of sequences
            if isinstance(sequence, List) and all([isinstance(seq, Sequence) for seq in sequence]):
                for seq in sequence:
                    if isinstance(seq, Sequence):
                        plot_dict_array = dict()
                        plot_dict_array.update({
                            AttributeNames.LANE_INDEX.value: lane_index,
                            AttributeNames.SEQUENCE_ID.value: seq.sequence_id
                        })
                        self._plots.append(plot_dict_array)
                    else:
                        raise ValueError(f"Unexpected type {type(seq)}")
                    # elif isinstance(seq, SequenceSelector):
                    #     seq_node = dict()
                    #     seq_node.update({
                    #         AttributeNames.LANE_INDEX.value: lane_index,
                    #         AttributeNames.WIDGET_REF.value: seq.widget_id
                    #     })
                    #     self._plots.append(seq_node)

            # if isinstance(sequence, SequenceSelector) or isinstance(sequence, CollectionSelector):
            #     if self.sequence:
            #         self._plots.append({AttributeNames.WIDGET_REF.value: sequence.widget_id})

            # a single sequence
            if isinstance(sequence, Sequence):
                plot_dict.update({
                    AttributeNames.SEQUENCE_ID.value: sequence.sequence_id
                })
                self._plots.append(plot_dict)

        # Handle arrays: y-axis
        # TODO: save array and send ID
        if y_axis is not None:
            self.linechart_sub_type = f"{AttributeNames.NUMPY_ARRAY.value.capitalize()}"
            if isinstance(y_axis, np.ndarray):
                plot_dict.update({AttributeNames.Y_AXIS.value: y_axis.tolist()})
            elif isinstance(y_axis, List):
                plot_dict.update({AttributeNames.Y_AXIS.value: y_axis})
            elif isinstance(y_axis, pd.Series):
                plot_dict.update({AttributeNames.Y_AXIS.value: y_axis.values.tolist()})

        # Handle arrays: x-axis
        # TODO: save array and send ID
        if x_axis is not None:
            if isinstance(x_axis, np.ndarray):
                is_type = ''
                if ('<i' in x_axis.dtype.str) or ('<f' in x_axis.dtype.str):
                    is_type = 'number'
                elif '<U' in x_axis.dtype.str:
                    is_type = 'string'
                if self._is_type is None:
                    self._is_type = is_type
                if self._is_type is not None and self._is_type is not is_type:
                    raise Exception("invalid mix of types in x axis")

                plot_dict.update({AttributeNames.X_AXIS.value: "nd_array_id"})

            elif isinstance(x_axis, List):
                if all([isinstance(item, str) for item in x_axis]):
                    is_type = 'string'
                elif all([(isinstance(item, float) or isinstance(item, int)) for item in x_axis]):
                    is_type = 'number'

                if self._is_type is None:
                    self._is_type = is_type

                if self._is_type is not None and self._is_type is not is_type:
                    raise Exception("invalid mix of types in x axis")

                plot_dict.update({AttributeNames.X_AXIS.value: x_axis})
            elif isinstance(x_axis, pd.RangeIndex):
                plot_dict.update({AttributeNames.X_AXIS.value: x_axis.tolist()})
            elif isinstance(x_axis, pd.DatetimeIndex):
                #     plot_dict.update({AttributeNames.X_AXIS.value: pd.Series(x_axis.format()).tolist()})
                plot_dict.update({AttributeNames.X_AXIS.value: x_axis.astype(np.int64).tolist()})

        if label is not None:
            if sequence:
                plot_dict.update({AttributeNames.LABEL.value: sequence})
            if isinstance(label, str):
                plot_dict.update({
                    AttributeNames.LABEL.value: label
                })
        if self.sequence is None:
            self._plots.append(plot_dict)


class LineChartWidget(Widget, LineChart):
    def __init__(self,
                 title: Optional[str] = None,
                 value: Optional[LineChartValueType] = None,
                 views: Optional[List[View]] = [],
                 temporal_context: Optional[TemporalContext] = None,
                 filtering_context: Optional[FilteringContext] = None,
                 multi_line_chart: Optional[bool] = True,
                 **additional):

        # define TYPE
        widget_type = LineChart.__name__
        Widget.__init__(self, widget_type, **additional)
        LineChart.__init__(self, title, value, views, temporal_context, filtering_context, multi_line_chart)
        self._parent_class = LineChart.__name__
        self._compatibility: Tuple = (str.__name__, int.__name__, float.__name__, LineChart.__name__, Sequence.__name__,
                                      View.__name__, "List[View]", "List[Sequence]", pd.DataFrame.__name__,
                                      list.__name__, np.ndarray.__name__, pd.Series.__name__)

        # if self.sequence and (self.y_axis or self.x_axis):
        #     raise Exception("sequence and axis properties are incompatible")
        #
        # if self.filtering_context and (self.y_axis or self.x_axis):
        #     raise Exception("filtering contexts cannot be used with axis properties")

        temporal_context_id = None
        if self.temporal_context:
            temporal_context_id = self.temporal_context.context_id
            self.temporal_context.widgets.append(self.widget_id)
        filtering_context_id = None
        if self.filtering_context:
            filtering_context_id = filtering_context.context_id
            filtering_context.output_widgets.append(self.widget_id)
        self.temporal_context = temporal_context_id
        self.filtering_context = filtering_context_id

    def to_dict_widget(self):
        line_chart_dict = super().to_dict_widget()
        if self.title is not None:
            if isinstance(self.title, str):
                line_chart_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            else:
                raise ValueError(f"Unexpected type {type(self.title)} in title")
            # elif isinstance(self.title, SequenceSelector):
            #     line_chart_dict[AttributeNames.PROPERTIES.value].update({
            #         AttributeNames.TITLE.value: {
            #             AttributeNames.WIDGET_REF.value: self.title.widget_id
            #         }
            #     })
        if self.sequence is not None:
            self.plot(sequence=self.sequence)
        elif self.x_axis is not None and self.y_axis is not None:
            self.plot(x_axis=self.x_axis, y_axis=self.y_axis)
        elif self.y_axis is not None:
            self.plot(y_axis=self.y_axis)

        if self.views:
            if isinstance(self.views, List) and all(isinstance(view, View) for view in self.views):
                view_list = [view.to_dict() for view in self.views]
                line_chart_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VIEWS.value: view_list
                })

        if len(self._plots) > 0:
            line_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.PLOTS.value: self._plots
            })

        if self.linechart_sub_type:
            line_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.TYPE.value: self.linechart_sub_type
            })

        return line_chart_dict

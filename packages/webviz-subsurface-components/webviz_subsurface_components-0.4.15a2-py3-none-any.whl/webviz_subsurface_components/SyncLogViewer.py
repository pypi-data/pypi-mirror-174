# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SyncLogViewer(Component):
    """A SyncLogViewer component.


Keyword arguments:

- id (string; required):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- axisMnemos (dict; optional):
    Names for axes.

- axisTitles (dict; optional):
    Log mnemonics for axes.

- checkDatafileSchema (boolean; optional):
    Validate JSON datafile against schems.

- colorTables (list; required):
    Prop containing color table data.

- domain (list of numbers; optional):
    Initial visible interval of the log data.

- hideLegend (boolean; optional):
    Hide legends of the track. Default is False.

- hideTitles (boolean; optional):
    Hide titles of the track. Default is False.

- horizontal (boolean; optional):
    Orientation of the track plots on the screen. Default is False.

- maxContentZoom (number; optional):
    The maximum zoom value.

- maxVisibleTrackNum (number; optional):
    The maximum number of visible tracks.

- patterns (list; optional):
    Horizon to pattern index map.

- patternsTable (dict; optional):
    Patterns table.

- primaryAxis (string; optional):
    Primary axis id: \" md\", \"tvd\", \"time\".

- readoutOptions (optional):
    Options for readout panel.

- selection (list of numbers; optional):
    Initial selected interval of the log data.

- spacers (list; optional):
    Set to True or to array of spacer widths if WellLogSpacers should
    be used.

- syncContentDomain (boolean; optional):
    Synchronize the visible area in views.

- syncContentSelection (boolean; optional):
    Synchronize the selection (current mouse hover) in views.

- syncTemplate (boolean; optional):
    Synchronize templates in views.

- syncTrackPos (boolean; optional):
    Synchronize the first visible track number in views.

- templates (list; required):
    Prop containing track template data.

- wellDistances (dict; optional):
    Distanses between wells to show on the spacers.

- welllogs (list; required):
    Array of JSON objects describing well log data.

- wellpicks (list; optional):
    Well Picks data array."""
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, welllogs=Component.REQUIRED, templates=Component.REQUIRED, colorTables=Component.REQUIRED, wellpicks=Component.UNDEFINED, patternsTable=Component.UNDEFINED, patterns=Component.UNDEFINED, spacers=Component.UNDEFINED, wellDistances=Component.UNDEFINED, horizontal=Component.UNDEFINED, primaryAxis=Component.UNDEFINED, hideTitles=Component.UNDEFINED, hideLegend=Component.UNDEFINED, axisTitles=Component.UNDEFINED, axisMnemos=Component.UNDEFINED, maxVisibleTrackNum=Component.UNDEFINED, maxContentZoom=Component.UNDEFINED, domain=Component.UNDEFINED, selection=Component.UNDEFINED, checkDatafileSchema=Component.UNDEFINED, readoutOptions=Component.UNDEFINED, syncTrackPos=Component.UNDEFINED, syncContentDomain=Component.UNDEFINED, syncContentSelection=Component.UNDEFINED, syncTemplate=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'axisMnemos', 'axisTitles', 'checkDatafileSchema', 'colorTables', 'domain', 'hideLegend', 'hideTitles', 'horizontal', 'maxContentZoom', 'maxVisibleTrackNum', 'patterns', 'patternsTable', 'primaryAxis', 'readoutOptions', 'selection', 'spacers', 'syncContentDomain', 'syncContentSelection', 'syncTemplate', 'syncTrackPos', 'templates', 'wellDistances', 'welllogs', 'wellpicks']
        self._type = 'SyncLogViewer'
        self._namespace = 'webviz_subsurface_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'axisMnemos', 'axisTitles', 'checkDatafileSchema', 'colorTables', 'domain', 'hideLegend', 'hideTitles', 'horizontal', 'maxContentZoom', 'maxVisibleTrackNum', 'patterns', 'patternsTable', 'primaryAxis', 'readoutOptions', 'selection', 'spacers', 'syncContentDomain', 'syncContentSelection', 'syncTemplate', 'syncTrackPos', 'templates', 'wellDistances', 'welllogs', 'wellpicks']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['id', 'colorTables', 'templates', 'welllogs']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(SyncLogViewer, self).__init__(**args)

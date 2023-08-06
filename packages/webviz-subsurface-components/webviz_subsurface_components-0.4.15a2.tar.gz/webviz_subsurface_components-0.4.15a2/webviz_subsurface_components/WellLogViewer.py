# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class WellLogViewer(Component):
    """A WellLogViewer component.


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

- primaryAxis (string; optional):
    Primary axis id: \" md\", \"tvd\", \"time\".

- readoutOptions (optional):
    Options for readout panel.

- selection (list of numbers; optional):
    Initial selected interval of the log data.

- template (dict; required):
    Prop containing track template data.

- welllog (dict; required):
    An object from JSON file describing well log data.

- wellpick (dict; optional):
    Well picks data."""
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, welllog=Component.REQUIRED, template=Component.REQUIRED, colorTables=Component.REQUIRED, horizontal=Component.UNDEFINED, hideTitles=Component.UNDEFINED, hideLegend=Component.UNDEFINED, domain=Component.UNDEFINED, selection=Component.UNDEFINED, wellpick=Component.UNDEFINED, primaryAxis=Component.UNDEFINED, axisTitles=Component.UNDEFINED, axisMnemos=Component.UNDEFINED, maxVisibleTrackNum=Component.UNDEFINED, maxContentZoom=Component.UNDEFINED, checkDatafileSchema=Component.UNDEFINED, readoutOptions=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'axisMnemos', 'axisTitles', 'checkDatafileSchema', 'colorTables', 'domain', 'hideLegend', 'hideTitles', 'horizontal', 'maxContentZoom', 'maxVisibleTrackNum', 'primaryAxis', 'readoutOptions', 'selection', 'template', 'welllog', 'wellpick']
        self._type = 'WellLogViewer'
        self._namespace = 'webviz_subsurface_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'axisMnemos', 'axisTitles', 'checkDatafileSchema', 'colorTables', 'domain', 'hideLegend', 'hideTitles', 'horizontal', 'maxContentZoom', 'maxVisibleTrackNum', 'primaryAxis', 'readoutOptions', 'selection', 'template', 'welllog', 'wellpick']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['id', 'colorTables', 'template', 'welllog']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(WellLogViewer, self).__init__(**args)

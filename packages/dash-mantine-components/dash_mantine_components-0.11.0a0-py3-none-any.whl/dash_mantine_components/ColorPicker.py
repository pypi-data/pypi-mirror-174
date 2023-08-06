# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ColorPicker(Component):
    """A ColorPicker component.
Inline color picker. For more information, see: https://mantine.dev/core/color-picker/

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- focusable (boolean; optional):
    Should interactive elements be focusable.

- format (a value equal to: 'hex', 'rgba', 'rgb', 'hsl', 'hsla'; optional):
    Color format.

- fullWidth (boolean; optional):
    Force picker to take 100% width of its container.

- m (number; optional):
    margin props.

- mb (number; optional):
    margin props.

- ml (number; optional):
    margin props.

- mr (number; optional):
    margin props.

- mt (number; optional):
    margin props.

- mx (number; optional):
    margin props.

- my (number; optional):
    margin props.

- p (number; optional):
    padding props.

- pb (number; optional):
    padding props.

- pl (number; optional):
    padding props.

- pr (number; optional):
    padding props.

- pt (number; optional):
    padding props.

- px (number; optional):
    padding props.

- py (number; optional):
    padding props.

- size (a value equal to: 'xs', 'sm', 'md', 'lg', 'xl'; optional):
    Predefined component size.

- style (boolean | number | string | dict | list; optional):
    Inline style.

- styles (dict; optional):
    Mantine styles API.

- swatches (list of strings; optional):
    Predefined colors.

- swatchesPerRow (number; optional):
    Number of swatches displayed in one row.

- sx (boolean | number | string | dict | list; optional):
    With sx you can add styles to component root element. If you need
    to customize styles of other elements within component use styles
    prop.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- value (string; optional):
    Controlled component value.

- withPicker (boolean; optional):
    Set to False to display swatches only."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mantine_components'
    _type = 'ColorPicker'
    @_explicitize_args
    def __init__(self, value=Component.UNDEFINED, format=Component.UNDEFINED, withPicker=Component.UNDEFINED, swatches=Component.UNDEFINED, swatchesPerRow=Component.UNDEFINED, size=Component.UNDEFINED, fullWidth=Component.UNDEFINED, focusable=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'focusable', 'format', 'fullWidth', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'size', 'style', 'styles', 'swatches', 'swatchesPerRow', 'sx', 'unstyled', 'value', 'withPicker']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'focusable', 'format', 'fullWidth', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'size', 'style', 'styles', 'swatches', 'swatchesPerRow', 'sx', 'unstyled', 'value', 'withPicker']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(ColorPicker, self).__init__(**args)

# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TimeInput(Component):
    """A TimeInput component.
Capture time input from user. For more information, see: https://mantine.dev/dates/time-input/

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- amLabel (string; optional):
    Label for 'am'.

- amPmPlaceholder (string; optional):
    Placeholder for am/pm input.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- clearable (boolean; optional):
    Allow to clear item.

- description (a list of or a singular dash component, string or number; optional):
    Input description, displayed after label.

- disabled (boolean; optional):
    Disabled input state.

- error (a list of or a singular dash component, string or number; optional):
    Displays error message after input.

- format (a value equal to: '12', '24'; optional):
    Time format.

- icon (a list of or a singular dash component, string or number; optional):
    Adds icon on the left side of input.

- iconWidth (number; optional):
    Width of icon section in px.

- inputWrapperOrder (list of a value equal to: 'label', 'description', 'error', 'input's; optional):
    Controls order of the Input.Wrapper elements.

- label (a list of or a singular dash component, string or number; optional):
    Input label, displayed before input.

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

- pmLabel (string; optional):
    Label for 'pm'.

- pr (number; optional):
    padding props.

- pt (number; optional):
    padding props.

- px (number; optional):
    padding props.

- py (number; optional):
    padding props.

- radius (number; optional):
    Input border-radius from theme or number to set border-radius in
    px.

- required (boolean; optional):
    Sets required on input element   Adds required attribute to the
    input and red asterisk on the right side of label.

- rightSection (a list of or a singular dash component, string or number; optional):
    Right section of input, similar to icon but on the right.

- rightSectionWidth (number; optional):
    Width of right section, is used to calculate input padding-right.

- size (a value equal to: 'xs', 'sm', 'md', 'lg', 'xl'; optional):
    Input size.

- style (boolean | number | string | dict | list; optional):
    Inline style.

- styles (dict; optional):
    Mantine styles API.

- sx (boolean | number | string | dict | list; optional):
    With sx you can add styles to component root element. If you need
    to customize styles of other elements within component use styles
    prop.

- timePlaceholder (string; optional):
    Placeholder for hours/minutes/seconds inputs.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- value (string; optional):
    Controlled input value.

- variant (a value equal to: 'unstyled', 'default', 'filled'; optional):
    Defines input appearance, defaults to default in light color
    scheme and filled in dark.

- withAsterisk (boolean; optional):
    Determines whether required asterisk should be rendered, overrides
    required prop, does not add required attribute to the input.

- withSeconds (boolean; optional):
    Display seconds input."""
    _children_props = ['icon', 'rightSection', 'label', 'description', 'error']
    _base_nodes = ['icon', 'rightSection', 'label', 'description', 'error', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'TimeInput'
    @_explicitize_args
    def __init__(self, value=Component.UNDEFINED, withSeconds=Component.UNDEFINED, clearable=Component.UNDEFINED, format=Component.UNDEFINED, amLabel=Component.UNDEFINED, pmLabel=Component.UNDEFINED, timePlaceholder=Component.UNDEFINED, amPmPlaceholder=Component.UNDEFINED, size=Component.UNDEFINED, icon=Component.UNDEFINED, iconWidth=Component.UNDEFINED, rightSection=Component.UNDEFINED, rightSectionWidth=Component.UNDEFINED, required=Component.UNDEFINED, radius=Component.UNDEFINED, variant=Component.UNDEFINED, disabled=Component.UNDEFINED, label=Component.UNDEFINED, description=Component.UNDEFINED, error=Component.UNDEFINED, withAsterisk=Component.UNDEFINED, inputWrapperOrder=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'amLabel', 'amPmPlaceholder', 'className', 'clearable', 'description', 'disabled', 'error', 'format', 'icon', 'iconWidth', 'inputWrapperOrder', 'label', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pmLabel', 'pr', 'pt', 'px', 'py', 'radius', 'required', 'rightSection', 'rightSectionWidth', 'size', 'style', 'styles', 'sx', 'timePlaceholder', 'unstyled', 'value', 'variant', 'withAsterisk', 'withSeconds']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'amLabel', 'amPmPlaceholder', 'className', 'clearable', 'description', 'disabled', 'error', 'format', 'icon', 'iconWidth', 'inputWrapperOrder', 'label', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pmLabel', 'pr', 'pt', 'px', 'py', 'radius', 'required', 'rightSection', 'rightSectionWidth', 'size', 'style', 'styles', 'sx', 'timePlaceholder', 'unstyled', 'value', 'variant', 'withAsterisk', 'withSeconds']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(TimeInput, self).__init__(**args)

# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Menu(Component):
    """A Menu component.
Combine a list of secondary actions into single interactive area. For more information, see: https://mantine.dev/core/menu/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Menu content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- arrowOffset (number; optional):
    Arrow offset in px.

- arrowSize (number; optional):
    Arrow size in px.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- clickOutsideEvents (list of strings; optional):
    Events that trigger outside clicks.

- closeDelay (number; optional):
    Close delay in ms, applicable only to trigger=\"hover\" variant.

- closeOnClickOutside (boolean; optional):
    Determines whether dropdown should be closed on outside clicks,
    default to True.

- closeOnEscape (boolean; optional):
    Determines whether dropdown should be closed when Escape key is
    pressed, defaults to True.

- closeOnItemClick (boolean; optional):
    Determines whether Menu should be closed when item is clicked.

- exitTransitionDuration (number; optional):
    Exit transition duration in ms.

- loop (boolean; optional):
    Determines whether arrow key presses should loop though items
    (first to last and last to first).

- offset (number; optional):
    Space between target element and dropdown in px.

- openDelay (number; optional):
    Open delay in ms, applicable only to trigger=\"hover\" variant.

- opened (boolean; optional):
    Controlled menu opened state.

- position (a value equal to: 'top', 'right', 'bottom', 'left', 'top-end', 'top-start', 'right-end', 'right-start', 'bottom-end', 'bottom-start', 'left-end', 'left-start'; optional):
    Dropdown position relative to target.

- radius (number; optional):
    Radius from theme.radius or number to set border-radius in px.

- shadow (boolean | number | string | dict | list; optional):
    Key of theme.shadow or any other valid css box-shadow value.

- style (boolean | number | string | dict | list; optional):
    Inline style.

- styles (dict; optional):
    Mantine styles API.

- sx (boolean | number | string | dict | list; optional):
    With sx you can add styles to component root element. If you need
    to customize styles of other elements within component use styles
    prop.

- transition (a value equal to: 'fade', 'skew-up', 'skew-down', 'rotate-right', 'rotate-left', 'slide-down', 'slide-up', 'slide-right', 'slide-left', 'scale-y', 'scale-x', 'scale', 'pop', 'pop-top-left', 'pop-top-right', 'pop-bottom-left', 'pop-bottom-right'; optional):
    One of premade transitions ot transition object.

- transitionDuration (number; optional):
    Transition duration in ms.

- trigger (a value equal to: 'click', 'hover'; optional):
    Event which should open menu.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- width (string | number; optional):
    Dropdown width, or 'target' to make dropdown width the same as
    target element.

- withArrow (boolean; optional):
    Determines whether component should have an arrow.

- zIndex (number; optional):
    Dropdown z-index."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mantine_components'
    _type = 'Menu'
    @_explicitize_args
    def __init__(self, children=None, opened=Component.UNDEFINED, closeOnItemClick=Component.UNDEFINED, loop=Component.UNDEFINED, closeOnEscape=Component.UNDEFINED, trigger=Component.UNDEFINED, openDelay=Component.UNDEFINED, closeDelay=Component.UNDEFINED, closeOnClickOutside=Component.UNDEFINED, clickOutsideEvents=Component.UNDEFINED, position=Component.UNDEFINED, offset=Component.UNDEFINED, transition=Component.UNDEFINED, transitionDuration=Component.UNDEFINED, exitTransitionDuration=Component.UNDEFINED, width=Component.UNDEFINED, withArrow=Component.UNDEFINED, arrowSize=Component.UNDEFINED, arrowOffset=Component.UNDEFINED, zIndex=Component.UNDEFINED, radius=Component.UNDEFINED, shadow=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'arrowOffset', 'arrowSize', 'className', 'clickOutsideEvents', 'closeDelay', 'closeOnClickOutside', 'closeOnEscape', 'closeOnItemClick', 'exitTransitionDuration', 'loop', 'offset', 'openDelay', 'opened', 'position', 'radius', 'shadow', 'style', 'styles', 'sx', 'transition', 'transitionDuration', 'trigger', 'unstyled', 'width', 'withArrow', 'zIndex']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'arrowOffset', 'arrowSize', 'className', 'clickOutsideEvents', 'closeDelay', 'closeOnClickOutside', 'closeOnEscape', 'closeOnItemClick', 'exitTransitionDuration', 'loop', 'offset', 'openDelay', 'opened', 'position', 'radius', 'shadow', 'style', 'styles', 'sx', 'transition', 'transitionDuration', 'trigger', 'unstyled', 'width', 'withArrow', 'zIndex']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Menu, self).__init__(children=children, **args)

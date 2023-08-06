# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DateRangePicker(Component):
    """A DateRangePicker component.
Capture date input from user. For more information, see: https://mantine.dev/dates/date-picker/

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- allowLevelChange (boolean; optional):
    Allow to change level (date - month - year).

- allowSingleDateInRange (boolean; optional):
    Allow one date to be selected as range.

- amountOfMonths (number; optional):
    Amount of months.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- clearButtonTabIndex (a value equal to: 0, -1; optional):
    Set the clear button tab index to disabled or default after input
    field.

- clearable (boolean; optional):
    Allow to clear value.

- clickOutsideEvents (list of strings; optional):
    Events that should trigger outside clicks.

- closeCalendarOnChange (boolean; optional):
    Set to False to force dropdown to stay open after date was
    selected.

- description (a list of or a singular dash component, string or number; optional):
    Input description, displayed after label.

- disableOutsideEvents (boolean; optional):
    When True dates that are outside of given month cannot be clicked
    or focused.

- disabled (boolean; optional):
    Disabled input state.

- disabledDates (list of strings; optional):
    Specifies additional days between min_date_allowed and
    max_date_allowed that should be disabled.

- dropdownPosition (a value equal to: 'bottom-start', 'top-start', 'flip'; optional):
    Dropdown positioning behavior.

- dropdownType (a value equal to: 'popover', 'modal'; optional):
    Where to show calendar in modal or popover.

- error (a list of or a singular dash component, string or number; optional):
    Displays error message after input.

- firstDayOfWeek (a value equal to: 'sunday', 'monday'; optional):
    Set first day of the week.

- fixOnBlur (boolean; optional):
    call onChange with last valid value onBlur.

- focusable (boolean; optional):
    Should focusable days have tabIndex={0}?.

- fullWidth (boolean; optional):
    Set to True to make calendar take 100% of container width.

- hideOutsideDates (boolean; optional):
    Remove outside dates.

- hideWeekdays (boolean; optional):
    Set to False to remove weekdays row.

- icon (a list of or a singular dash component, string or number; optional):
    Adds icon on the left side of input.

- iconWidth (number; optional):
    Width of icon section in px.

- initialLevel (a value equal to: 'date', 'month', 'year'; optional):
    Initial date selection level.

- initialMonth (string; optional):
    Initial month for uncontrolled calendar.

- initiallyOpened (boolean; optional):
    Control initial dropdown opened state.

- inputFormat (string; optional):
    dayjs input format.

- inputWrapperOrder (list of a value equal to: 'label', 'description', 'error', 'input's; optional):
    Controls order of the Input.Wrapper elements.

- label (a list of or a singular dash component, string or number; optional):
    Input label, displayed before input.

- labelSeparator (string; optional):
    Separator between dates.

- locale (string; optional):
    Locale used for labels formatting, defaults to theme.datesLocale.

- m (number; optional):
    margin props.

- maxDate (string; optional):
    Maximum possible date.

- mb (number; optional):
    margin props.

- minDate (string; optional):
    Minimum possible date.

- ml (number; optional):
    margin props.

- modalZIndex (number; optional):
    Modal z-index.

- mr (number; optional):
    margin props.

- mt (number; optional):
    margin props.

- mx (number; optional):
    margin props.

- my (number; optional):
    margin props.

- openDropdownOnClear (boolean; optional):
    Set to True to open dropdown on clear.

- p (number; optional):
    padding props.

- paginateBy (number; optional):
    Paginate by amount of months.

- pb (number; optional):
    padding props.

- pl (number; optional):
    padding props.

- placeholder (string; optional):
    Placeholder.

- pr (number; optional):
    padding props.

- preventFocus (boolean; optional):
    Prevent focusing upon clicking.

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

- shadow (a value equal to: 'xs', 'sm', 'md', 'lg', 'xl'; optional):
    Dropdown shadow from theme or css value for custom box-shadow.

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

- transition (a value equal to: 'fade', 'skew-up', 'skew-down', 'rotate-right', 'rotate-left', 'slide-down', 'slide-up', 'slide-right', 'slide-left', 'scale-y', 'scale-x', 'scale', 'pop', 'pop-top-left', 'pop-top-right', 'pop-bottom-left', 'pop-bottom-right'; optional):
    Dropdown appear/disappear transition.

- transitionDuration (number; optional):
    Dropdown appear/disappear transition duration.

- transitionTimingFunction (string; optional):
    Dropdown appear/disappear transition timing function, defaults to
    theme.transitionTimingFunction.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- value (boolean | number | string | dict | list; optional):
    Selected date, required with controlled input.

- variant (a value equal to: 'unstyled', 'default', 'filled'; optional):
    Defines input appearance, defaults to default in light color
    scheme and filled in dark.

- weekendDays (list of numbers; optional):
    Indices of weekend days.

- withAsterisk (boolean; optional):
    Determines whether required asterisk should be rendered, overrides
    required prop, does not add required attribute to the input.

- zIndex (number; optional):
    Dropdown zIndex."""
    _children_props = ['icon', 'rightSection', 'label', 'description', 'error']
    _base_nodes = ['icon', 'rightSection', 'label', 'description', 'error', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'DateRangePicker'
    @_explicitize_args
    def __init__(self, value=Component.UNDEFINED, allowSingleDateInRange=Component.UNDEFINED, labelSeparator=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, transition=Component.UNDEFINED, transitionDuration=Component.UNDEFINED, transitionTimingFunction=Component.UNDEFINED, shadow=Component.UNDEFINED, size=Component.UNDEFINED, dropdownType=Component.UNDEFINED, dropdownPosition=Component.UNDEFINED, clearable=Component.UNDEFINED, zIndex=Component.UNDEFINED, fixOnBlur=Component.UNDEFINED, clickOutsideEvents=Component.UNDEFINED, modalZIndex=Component.UNDEFINED, clearButtonTabIndex=Component.UNDEFINED, amountOfMonths=Component.UNDEFINED, paginateBy=Component.UNDEFINED, allowLevelChange=Component.UNDEFINED, initialLevel=Component.UNDEFINED, disabledDates=Component.UNDEFINED, disableOutsideEvents=Component.UNDEFINED, fullWidth=Component.UNDEFINED, preventFocus=Component.UNDEFINED, focusable=Component.UNDEFINED, maxDate=Component.UNDEFINED, minDate=Component.UNDEFINED, hideWeekdays=Component.UNDEFINED, hideOutsideDates=Component.UNDEFINED, weekendDays=Component.UNDEFINED, firstDayOfWeek=Component.UNDEFINED, closeCalendarOnChange=Component.UNDEFINED, openDropdownOnClear=Component.UNDEFINED, inputFormat=Component.UNDEFINED, initiallyOpened=Component.UNDEFINED, initialMonth=Component.UNDEFINED, locale=Component.UNDEFINED, icon=Component.UNDEFINED, iconWidth=Component.UNDEFINED, rightSection=Component.UNDEFINED, rightSectionWidth=Component.UNDEFINED, required=Component.UNDEFINED, radius=Component.UNDEFINED, variant=Component.UNDEFINED, disabled=Component.UNDEFINED, placeholder=Component.UNDEFINED, label=Component.UNDEFINED, description=Component.UNDEFINED, error=Component.UNDEFINED, withAsterisk=Component.UNDEFINED, inputWrapperOrder=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'allowLevelChange', 'allowSingleDateInRange', 'amountOfMonths', 'className', 'clearButtonTabIndex', 'clearable', 'clickOutsideEvents', 'closeCalendarOnChange', 'description', 'disableOutsideEvents', 'disabled', 'disabledDates', 'dropdownPosition', 'dropdownType', 'error', 'firstDayOfWeek', 'fixOnBlur', 'focusable', 'fullWidth', 'hideOutsideDates', 'hideWeekdays', 'icon', 'iconWidth', 'initialLevel', 'initialMonth', 'initiallyOpened', 'inputFormat', 'inputWrapperOrder', 'label', 'labelSeparator', 'locale', 'm', 'maxDate', 'mb', 'minDate', 'ml', 'modalZIndex', 'mr', 'mt', 'mx', 'my', 'openDropdownOnClear', 'p', 'paginateBy', 'pb', 'pl', 'placeholder', 'pr', 'preventFocus', 'pt', 'px', 'py', 'radius', 'required', 'rightSection', 'rightSectionWidth', 'shadow', 'size', 'style', 'styles', 'sx', 'transition', 'transitionDuration', 'transitionTimingFunction', 'unstyled', 'value', 'variant', 'weekendDays', 'withAsterisk', 'zIndex']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'allowLevelChange', 'allowSingleDateInRange', 'amountOfMonths', 'className', 'clearButtonTabIndex', 'clearable', 'clickOutsideEvents', 'closeCalendarOnChange', 'description', 'disableOutsideEvents', 'disabled', 'disabledDates', 'dropdownPosition', 'dropdownType', 'error', 'firstDayOfWeek', 'fixOnBlur', 'focusable', 'fullWidth', 'hideOutsideDates', 'hideWeekdays', 'icon', 'iconWidth', 'initialLevel', 'initialMonth', 'initiallyOpened', 'inputFormat', 'inputWrapperOrder', 'label', 'labelSeparator', 'locale', 'm', 'maxDate', 'mb', 'minDate', 'ml', 'modalZIndex', 'mr', 'mt', 'mx', 'my', 'openDropdownOnClear', 'p', 'paginateBy', 'pb', 'pl', 'placeholder', 'pr', 'preventFocus', 'pt', 'px', 'py', 'radius', 'required', 'rightSection', 'rightSectionWidth', 'shadow', 'size', 'style', 'styles', 'sx', 'transition', 'transitionDuration', 'transitionTimingFunction', 'unstyled', 'value', 'variant', 'weekendDays', 'withAsterisk', 'zIndex']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DateRangePicker, self).__init__(**args)

import atexit
import enum
import io
import statistics
import sys
import time
import typing
from abc import ABC, abstractmethod
from datetime import timedelta
from sys import stdin, stdout
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Literal,
    NoReturn,
    Optional,
    Tuple,
    TypeVar,
)

import blessed
import rich
import rich.markup

# These aren't available on all platforms
try:
    import readline  # type: ignore  (Just importing readline activates it)
    import termios
except ImportError:
    readline = None
    termios = None

__all__ = [
    "Widget",
    "TextLine",
    "ProgressBar",
    "print",
    "print_chapter",
    "warning",
    "error",
    "fatal",
    "input",
    "Option",
    "select",
    "ask_short_option",
    "ask_yes_no",
    "get_docked_widget",
    "escape",
    "unescape",
]


# Keep track of global state
_docked_widget: "Widget | None" = None
_chapter: str | None = None
_is_first_line = True
_is_in_new_line = True


T = TypeVar("T")


_SENTINEL = object()


_py_input = input


class Widget(ABC):
    def __init__(self):
        self._parent: Optional[Widget] = None

    def mark_dirty(self) -> None:
        """
        Mark this widget as dirty, requesting a redraw.
        """

        # If this widget has a parent, let that handle the call instead
        if self._parent is not None:
            self._parent.mark_dirty()
            return

        # The widget isn't docked, there is nothing it can do
        if not self.is_docked:
            return

        # Redraw
        term = blessed.Terminal()
        stdout.write(term.clear_bol())  # type: ignore
        stdout.write(term.move_x(0 if _chapter is None else 3))
        self.draw(term)

    @property
    def is_docked(self) -> bool:
        """
        Returns `True` if this widget is currently docked and `False` otherwise.
        """
        return self is _docked_widget

    def undock(self) -> None:
        global _docked_widget
        if _docked_widget is not self:
            raise ValueError("Widget is not docked")

        _docked_widget = None
        self.on_undock()

    def on_dock(self) -> None:
        """
        Called whenever a widget is being docked.
        """
        pass

    def on_undock(self) -> None:
        """
        Called whenever a widget is being undocked.
        """
        pass

    @abstractmethod
    def draw(self, term: blessed.Terminal) -> None:
        """
        Draw the widget. The curser is at the top left position of the widget.

        TODO: Where should the cursor be after the widget is drawn?
        """
        pass


class TextLine(Widget):
    """
    A simple line of text, optionally formatted with `rich` style markup.
    """

    _text: str

    def __init__(self, text: str = "", *, markup: bool = True):
        super().__init__()

        self.text = text
        self.markup = markup

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: Any) -> None:
        self._text = str(value)
        self.mark_dirty()

    def draw(self, term: blessed.Terminal) -> None:
        if self.markup:
            stdout.write(unescape(self.text))
        else:
            stdout.write(self.text)

        stdout.flush()


class Unit(enum.Enum):
    """
    Internal class for representing a unit.
    """

    COUNT = enum.auto()
    PERCENT = enum.auto()
    BYTE = enum.auto()
    TIME = enum.auto()

    @classmethod
    def from_string(cls, value: str) -> "Unit":
        if value == "count":
            return cls.COUNT
        elif value == "percent":
            return cls.PERCENT
        elif value == "byte":
            return cls.BYTE
        elif value == "time":
            return cls.TIME
        else:
            raise ValueError(f"Unknown unit type: {value}")

    def __str__(self) -> str:
        return self.name.lower()

    def _units(self) -> Iterable[Tuple[str, float, bool]]:
        """
        Return names of all units for this type and the divisor to convert from
        the base unit to them. The results are ordered from smallest to largest.
        In addition, a boolean is also returned, which indicates whether this
        unit is favorable (i.e. not an outdated or otherwise undesirable unit).
        """

        if self is Unit.COUNT:
            yield "", 1, True

        elif self is Unit.PERCENT:
            yield "%", 100, True

        elif self is Unit.BYTE:
            yield "B", 1, True
            yield "KB", 1000, False
            yield "KiB", 1024, True
            yield "MB", 1000**2, False
            yield "MiB", 1024**2, True
            yield "GB", 1000**3, False
            yield "GiB", 1024**3, True
            yield "TB", 1000**4, False
            yield "TiB", 1024**4, True
            yield "PB", 1000**5, False
            yield "PiB", 1024**5, True

        elif self is Unit.TIME:
            yield "ms", 1 / 1000, True
            yield "s", 1, False
            yield "second", 1, True
            yield "m", 60, False
            yield "minute", 60, True
            yield "h", 60 * 60, False
            yield "hour", 60 * 60, True
            yield "d", 60 * 60 * 24, False
            yield "day", 60 * 60 * 24, True

        else:
            raise NotImplementedError(f"Unknown unit type: {self}")

    def pretty_approximate_value(self, value: int | float) -> str:
        # Count specific: there is nothing to do here
        if self == Unit.COUNT:
            return str(value)

        # Time: This is a special case, because multiple units are used in the
        # result
        if self == Unit.TIME:
            seconds = int(value)

            # Special case: 0
            if seconds == 0:
                return "0 seconds"

            # Determine the time, in multiple sub-units
            units = (
                ("second", 60),
                ("minute", 60),
                ("hour", 24),
                ("day", None),
            )

            parts = []

            amount = seconds
            for unit_info in units:
                unit_name, unit_factor = unit_info

                if unit_factor is None:
                    cur = amount
                else:
                    cur = amount % unit_factor
                    amount = amount // unit_factor

                if cur == 0:
                    continue

                parts.append((unit_name, cur))

            # Drop any pointless ones
            while len(parts) > 2:
                parts.pop(0)

            # Turn everything into a string
            chunks = []
            for unit_name, amount in reversed(parts):
                if amount == 1:
                    chunks.append(f"1 {unit_name}")

                else:
                    chunks.append(f"{amount} {unit_name}s")

            return " ".join(chunks)

        # All other units: Find the largest unit that is still smaller than the
        # value
        unit_name, unit_factor = "", 1

        for next_unit_name, next_unit_factor, desirable in self._units():
            if not desirable:
                continue

            if value < next_unit_factor:
                break

            unit_name, unit_factor = next_unit_name, next_unit_factor

        # Round as appropriate
        unit_value = value / unit_factor

        if unit_value == int(unit_value):
            unit_value = int(unit_value)
        elif unit_value < 10:
            unit_value = round(unit_value, 1)
        else:
            unit_value = round(unit_value)

        return f"{unit_value}{unit_name}"  # type: ignore


class ProgressBar(Widget):
    """
    A progress bar, duh.
    """

    _progress: float
    _width: int
    _unit: Unit

    def __init__(
        self,
        progress: int | float = 0.0,
        max: int | float = 1.0,
        width: int = 50,
        unit: Literal["count", "percent", "byte", "time"] = "percent",
    ):
        super().__init__()

        # Data used to predict an ETA. This is a list of (timestamp, progress)
        # tuples, with `progress` being in range [0, 1]
        self._progress_timestamps: List[Tuple[float, float]] = []

        self.max = max  # The `progress` setter uses this value, set it first
        self.progress = progress
        self.width = width
        self.unit = unit

    @property
    def progress(self) -> int | float:
        """
        How far the progress bar is filled. A value of 0 means that the bar is
        empty, while a value of `bar.max` means that the bar is completely
        filled.
        """
        return self._progress

    @progress.setter
    def progress(self, value: int | float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("The progressbar's progress must be an integer or float")

        self._progress = value
        self.mark_dirty()

        # Keep track of the progress so an ETA can be calculated later on. If
        # the progressbar was just reset to 0, it is probably about to be
        # reused, making the previous timestamps invalid
        if value == 0:
            self._progress_timestamps = []
        else:
            self._progress_timestamps.append((time.time(), self.fraction))

            # Don't keep too many timestamps
            time_cutoff = time.time() - 45
            while (
                len(self._progress_timestamps) > 40
                and self._progress_timestamps[1][0] < time_cutoff
            ):
                del self._progress_timestamps[0]

            if len(self._progress_timestamps) > 100:
                self._progress_timestamps = self._progress_timestamps[::2]

    @property
    def max(self) -> int | float:
        """
        The value at which the bar is considered completely filled.
        """
        return self._max

    @max.setter
    def max(self, value: int | float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("The progressbar's maximum value must be a float")

        if value < 0:
            raise ValueError("The progressbar's maximum value cannot be negative")

        self._max = value
        self.mark_dirty()

    @property
    def width(self) -> int:
        """
        The progress bar's width, in characters.
        """
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("The progressbar's width must be an integer")

        if value < 0:
            raise ValueError("The progressbar's width must be a positive integer")

        self._width = value
        self.mark_dirty()

    @property
    def fraction(self) -> float:
        """
        The bar's current progress fraction, as float in range [0, 1].
        """
        try:
            return min(self.progress / self.max, 1.0)
        except ZeroDivisionError:
            return 0.0

    @property
    def unit(self) -> str:
        """
        The unit used to display the progress bar's value.
        """
        return str(self._unit)

    @unit.setter
    def unit(self, value: Literal["count", "percent", "byte", "time"]) -> None:
        self._unit = Unit.from_string(value)
        self.mark_dirty()

    def complete(self) -> None:
        """
        Convenience method which sets the bar's progress to its maximum value
        and undocks the bar if it is docked.
        """
        self.progress = self.max

        if self.is_docked:
            self.undock()

    @property
    def eta(self) -> Optional[timedelta]:
        """
        The estimated time until the progress bar is complete, or `None` if
        there is not enough data to calculate an ETA with reasonable confidence.
        """
        # Not enough data
        if not self._progress_timestamps or len(self._progress_timestamps) < 3:
            return None

        first_time, first_fraction = self._progress_timestamps[0]
        cur_time, cur_fraction = self._progress_timestamps[-1]

        # Funky data
        if first_time >= cur_time or first_fraction >= cur_fraction:
            return None

        # Good data
        speed = (cur_fraction - first_fraction) / (cur_time - first_time)
        assert speed > 0, speed
        return timedelta(seconds=(1 - cur_fraction) / speed)

    @property
    def bar_string(self) -> str:
        """
        The string representation of the progress bar. This only includes the
        bar, not any text around it. The returned string may be colored, and
        thus should be printed as markup.
        """
        blocks = "·▏▎▍▌▋▊▉█"
        fraction = self.fraction

        # Fully filled blocks
        n_blocks_remaining = self.width
        n_blocks_filled = int(fraction * n_blocks_remaining)
        bar_string = "[blue]" + n_blocks_filled * blocks[-1]
        n_blocks_remaining -= n_blocks_filled

        # Partial block
        partial_frac = fraction * self.width - n_blocks_filled
        partial_index = round(partial_frac * (len(blocks) - 1))
        if n_blocks_remaining > 0 and partial_index != 0:
            bar_string += blocks[partial_index]
            n_blocks_remaining -= 1

        bar_string += "[/]"

        # Empty blocks
        bar_string += n_blocks_remaining * blocks[0]

        return bar_string

    def draw(self, term: blessed.Terminal) -> None:
        # Display the bar
        stdout.write(unescape(self.bar_string))

        # Display written progress
        unit = Unit.from_string(self.unit)  # type: ignore
        fraction = self.fraction

        if unit == Unit.PERCENT:
            stdout.write(f" {fraction*100:.1f}%")
        elif unit == Unit.TIME:
            if fraction != 1:
                stdout.write(
                    f"  {unit.pretty_approximate_value(self.max - self.progress)}"
                )
        elif fraction == 0 or fraction == 1:
            stdout.write(f"  {unit.pretty_approximate_value(self.max)}")
        else:
            stdout.write(
                f"  {unit.pretty_approximate_value(self.progress)} ╱ {unit.pretty_approximate_value(self.max)}"
            )

        # Display an ETA
        if fraction != 1:
            eta = self.eta
            if eta is not None:
                pretty_str = Unit.TIME.pretty_approximate_value(eta.total_seconds())
                stdout.write(
                    unescape(f"[bright_black] — about {pretty_str} remaining[/]")
                )

        stdout.flush()


def get_docked_widget() -> Optional[Widget]:
    """
    Returns the currently docked widget, or `None` if no widget is docked.
    """
    return _docked_widget


# Create a console for unescaping `rich` style markup
_rich_term_console = rich.get_console()
_rich_abstract_console = rich.console.Console(
    file=io.StringIO(),
    color_system=_rich_term_console.color_system,  # type: ignore
)
del _rich_term_console


def unescape(text: Any) -> str:
    """
    Unescapes `rich` style markup from a string.
    """
    file = io.StringIO()
    _rich_abstract_console.file = file
    _rich_abstract_console.print(str(text), end="")
    return file.getvalue()


def escape(text: Any) -> str:
    """
    Escapes a string to prevent `rich` style markup from being interpreted.
    """
    return rich.markup.escape(str(text))


def _print_newline(n_newlines: int = 1) -> None:
    global _is_in_new_line
    assert n_newlines >= 0, n_newlines

    if n_newlines == 0:
        return

    if _is_in_new_line:
        n_newlines -= 1

    stdout.write("\n" * n_newlines)
    _is_in_new_line = False


Tprint = TypeVar("Tprint", bound=Widget)


@typing.overload
def print(*values: Tprint, dock: bool = False, markup: bool = True) -> Tprint:
    ...


@typing.overload
def print(*values: Any, dock: bool = False, markup: bool = True) -> TextLine:
    ...


def print(*values: Any, dock: bool = False, markup: bool = True) -> Widget:
    """
    Prints a widget to the terminal, optionally docking it.

    If a single widget is passed it is returned, otherwise the inputs are
    converted to strings, joined with a space and returned as a `TextLine`.
    """
    global _docked_widget, _is_first_line, _is_in_new_line

    # Convert the inputs to a single Widget
    if len(values) == 1 and isinstance(values[0], Widget):
        widget = values[0]
    else:
        widget = TextLine(
            " ".join(str(v) for v in values),
            markup=markup,
        )

    # Position the cursor at the start of a new line, taking any docked widgets
    # into account
    term = blessed.Terminal()
    other_docked_widget_remains_below = _docked_widget is not None and not dock

    if other_docked_widget_remains_below:
        stdout.write(term.clear_bol)  # Clear to the start of the line
    elif dock:
        if _docked_widget is not None:
            _docked_widget.on_undock()

        widget.on_dock()
        _docked_widget = widget

        _print_newline()
    else:
        _print_newline()

    # Display the widget
    stdout.write(term.move_x(0 if _chapter is None else 3))
    widget.draw(term)

    # Re-display the docked widget
    if other_docked_widget_remains_below:
        assert _docked_widget is not None
        _print_newline()
        stdout.write(term.move_x(0 if _chapter is None else 3))
        _docked_widget.draw(term)

    # Update global state
    _is_first_line = False
    _is_in_new_line = False

    return widget


def _basic_print(prefix: str, values: Iterable[Any], markup: bool) -> None:
    values = " ".join(map(str, values))
    if not markup:
        values = escape(values)

    print(f"{prefix}{values}", dock=False)


def warning(*values: Any, markup: bool = True) -> None:
    """
    Displays a warning message, highlighted to draw attention to it.
    """
    _basic_print("[bold][yellow]Warning:[/bold] ", values, markup)


def error(*values: Any, markup: bool = True) -> None:
    """
    Displays an error message, highlighted to draw attention to it.
    """
    _basic_print("[bold][red]Error:[/bold] ", values, markup)


def fatal(*values: Any, status_code: int = 1, markup: bool = True) -> NoReturn:
    """
    Displays an error message, highlighted to draw attention to it, and then
    exits the program.
    """
    _basic_print("[bold][red]ERROR:[/bold] ", values, markup)
    sys.exit(status_code)


def print_chapter(name: str | None) -> None:
    """
    Displays a chapter heading. Chapters are highlighted and create whitespace
    to visually separate them from other widgets.
    """

    global _docked_widget, _is_first_line, _chapter, _is_in_new_line

    # Undock any previously docked widgets
    if _docked_widget is not None:
        _docked_widget.on_undock()
        _docked_widget = None

    # Spacing to previous content
    if not _is_first_line:
        _print_newline(2)

    # Print the chapter name
    if name is not None:
        stdout.write(unescape(f"[bold blue] > {escape(name)}[/]"))

    stdout.flush()

    # Update global state
    _chapter = name
    _is_first_line = False
    _is_in_new_line = False


def input(
    prompt: str = "",
    default: T = _SENTINEL,
    *,
    sep: str = ": ",
    parse: Callable[[str], T] = str,
    markup: bool = True,
) -> T:
    """
    Asks the user for a value and returns it. If `prompt` is given, it is
    displayed first. `parse` is applied to the user's input, and its result
    returned. If `parse` raises a `ValueError` the user is asked for another
    value. Lastly, if `default` is given, it is returned if the user enters an
    empty string.
    """
    global _is_in_new_line

    # Undock any existing widget
    if _docked_widget is not None:
        _docked_widget.undock()

    # Preprocess the prompt
    prompt += sep

    if markup:
        prompt = unescape(prompt)

    if _chapter is not None:
        prompt = f"   {prompt}"

    # Ask for values, until a valid one comes along
    while True:
        # Get a value
        _set_echo(True)
        _set_cursor(True)
        _print_newline()
        stdin.flush()
        try:
            value = _py_input(prompt).strip()
        finally:
            _set_echo(False)
            _set_cursor(False)

        # Use the default value?
        if not value and default is not _SENTINEL:
            return default  # type: ignore

        # Try to parse it, thus verifying it's valid
        try:
            value = parse(value)
        except ValueError:
            continue

        # The user has just pressed `enter`, so the cursor is in a new line
        _is_in_new_line = True

        return value


class Option(Generic[T]):
    def __init__(
        self,
        name: str,
        value: Any,
        alt_names: Iterable[str] = tuple(),
        *,
        is_default: bool = False,
    ):
        if not isinstance(name, str):
            raise TypeError(f"Option names need to be strings, got {name!r}")

        alt_names = list(alt_names)
        for alt_name in alt_names:
            if not isinstance(alt_name, str):
                raise TypeError(
                    f"Option alt-names need to be strings, got {alt_name!r}"
                )

        if not isinstance(is_default, bool):
            raise TypeError(f"Option is_default needs to be a bool, got {is_default!r}")

        self.name = name
        self.value = value
        self.alt_names = alt_names
        self.is_default = is_default

    def _all_names(self) -> Iterable[str]:
        yield self.name
        yield from self.alt_names


def select(prompt: str = "", *options: Option[T]) -> T:
    """
    Asks the user to select one of the given options. If `prompt` is given, it
    is displayed first. The options are displayed as a numbered list, and the
    user is asked to select one of them. If the user enters an empty string, the
    default option is selected if provided.
    """

    opt_list = list(options)
    default_option: Optional[Option] = None

    for opt in opt_list:
        if not isinstance(opt, Option):
            raise TypeError(f"Options need to be Option instances, got {opt!r}")

        if opt.is_default:
            if default_option is not None:
                raise ValueError("Only one option can be the default")

            default_option = opt

    # Display the options
    print(prompt)
    for ii, option in enumerate(opt_list):
        print(unescape(f"[bright_black]{ii + 1}. [/]{escape(option.name)}"))

    # Ask for a selection
    while True:
        selection = input(sep="")

        # Select the default?
        if not selection and default_option is not None:
            return default_option.value

        # Was this a numeric selection?
        try:
            selection = int(selection)
        except ValueError:
            pass
        else:
            if 1 <= selection <= len(opt_list):
                return opt_list[selection - 1].value
            else:
                continue

        # Find all matching options
        matches = []
        selection_normalized = selection.lower()

        for option in opt_list:
            for name in option._all_names():
                name_normalized = name.lower()

                # Exact match, this is it
                if name_normalized == selection_normalized:
                    return option.value

                # Partial match, add it to the list
                if selection_normalized in name_normalized:
                    matches.append(option)
                    break

        # If there are no matches, try again
        if not matches:
            continue

        # If the match is unique, return it
        if len(matches) == 1:
            return matches[0].value

        # Otherwise, ask the user to discriminate between all matches
        return select("", *matches)


def ask_short_option(
    prompt: str,
    options: Dict[str, Any],
    *,
    default_str: Optional[str] = None,
    add_yes_no_options: bool = False,
) -> Any:
    """
    TODO
    """
    for opt in options.keys():
        assert opt == opt.lower(), opt

    # Prepared, commonly used options
    if add_yes_no_options:
        t = {
            "y": True,
            "yes": True,
            "1": True,
            "t": True,
            "true": True,
            "n": False,
            "no": False,
            "0": False,
            "f": False,
            "false": False,
        }
        t.update(options)
        options = t

    # Make sure the default is valid
    assert default_str is None or default_str == default_str.lower(), default_str
    assert default_str is None or default_str in options, (
        default_str,
        options.keys(),
    )

    # Prepare the option strings for the prompt. There's no point in showing all
    # options, as many map to the same values. Instead, show the first option
    # corresponding to each value, while prioritizing the default option.
    #
    # TODO: This currently requires the returned value to be hashable.
    primary_options = {}
    for opt, value in options.items():
        assert opt == opt.lower(), opt

        if default_str is not None and opt == default_str:
            opt = opt.upper()
            primary_options[value] = opt
        else:
            primary_options.setdefault(value, opt)

    options_string = escape("/".join(primary_options.values()))
    full_prompt = f"{prompt} \\[{options_string}]"

    # Keep asking until there is a valid response
    while True:
        # Ask for input
        response = input(full_prompt).strip().lower()

        if not response and default_str is not None:
            response = default_str

        try:
            return options[response]
        except KeyError:
            pass

        # Ask again if it's invalid
        _print_newline()
        sys.stdout.write(f"Please respond with one of {options_string}")


def ask_yes_no(prompt: str, default_value: Optional[bool] = None) -> bool:
    """
    Displays the prompt to the user, and returns True if the user responds with
    yes, and False if the user responds with no. If no input is entered and a
    default value is provided it is returned instead.

    The function makes a best effort to interpret the user's input, and will
    accept a variety of possible values.
    """
    if default_value is None:
        default_str = None
    elif default_value:
        default_str = "y"
    else:
        default_str = "n"

    return ask_short_option(
        prompt,
        {},
        default_str=default_str,
        add_yes_no_options=True,
    )


def _set_echo(enable_echo: bool):
    if termios is None:
        return  # TODO

    fd = sys.stdin.fileno()
    (iflag, oflag, cflag, lflag, ispeed, ospeed, cc) = termios.tcgetattr(fd)

    if enable_echo:
        lflag |= termios.ECHO
    else:
        lflag &= ~termios.ECHO

    new_attr = [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
    termios.tcsetattr(fd, termios.TCSANOW, new_attr)


def _set_cursor(enable_cursor: bool):
    stdout.write("\033[?25h" if enable_cursor else "\033[?25l")
    stdout.flush()


def _on_exit():
    # Clean up the terminal
    _set_echo(True)
    _set_cursor(True)
    stdout.write("\n")
    stdout.flush()


atexit.register(_on_exit)
_set_echo(False)
_set_cursor(False)

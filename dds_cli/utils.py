import rich.console
import numbers

console = rich.console.Console()
stderr_console = rich.console.Console(stderr=True)


def calculate_magnitude(projects, keys, iec_standard=False):
    """Uses the project list, obtains the values assigned to a particular key iteratively and calculates the best magnitude to format this set of values consistently"""

    # initialize the dictionary to be returned
    magnitudes = dict(zip(keys, [None] * len(keys)))

    for key in keys:

        values = [proj[key] for proj in projects]

        if all(isinstance(x, numbers.Number) for x in values):

            if key in ["Size", "Usage"] and iec_standard:
                base = 1024.0
            else:
                base = 1000.0

            # exclude values smaller than base, such that empty projects don't interfer with the calculation
            # ensures that a minimum can be calculated if no val is larger than base
            minimum = (lambda x: min(x) if x else 1)([val for val in values if val >= base])
            mag = 0

            while abs(minimum) >= base:
                mag += 1
                minimum /= base

            magnitudes[key] = mag
    return magnitudes


def format_api_response(response, key, magnitude=None, iec_standard=False):
    """Takes a value e.g. bytes and reformats it to include a unit prefix"""
    if isinstance(response, str):
        return response  # pass the response if already a string

    if isinstance(response, numbers.Number):
        response = float("{:.3g}".format(response))
        mag = 0

        if key in ["Size", "Usage"]:
            if iec_standard:
                # The IEC created prefixes such as kibi, mebi, gibi, etc., to unambiguously denote powers of 1024
                prefixlist = ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi", "Yi"]
                base = 1024.0
            else:
                prefixlist = ["", "K", "M", "G", "T", "P", "E", "Z", "Y"]
                base = 1000.0
            spacerA = " "
            spacerB = ""
        else:
            # Default to the prefixes of the International System of Units (SI)
            prefixlist = ["", "k", "M", "G", "T", "P", "E", "Z", "Y"]
            base = 1000.0
            spacerA = ""
            spacerB = " "

        if not magnitude:
            # calculate a suitable magnitude if not given
            while abs(response) >= base:
                mag += 1
                response /= base
        else:
            # utilize the given magnitude
            response /= base ** magnitude

        if key == "Size":
            unit = "B"  # lock
        elif key == "Usage":
            unit = "Bh"  # arrow up
        elif key == "Cost":
            unit = "SEK"
            prefixlist[1] = "K"  # for currencies, the capital K is more common.
            prefixlist[3] = "B"  # for currencies, Billions are used instead of Giga

        if response > 0:
            if (
                magnitude
            ):  # if magnitude was given, then use fixed number of digits to allow for easier comparisons across projects
                return "{}{}{}".format(
                    "{:.2f}".format(response),
                    spacerA,
                    prefixlist[magnitude] + spacerB + unit,
                )
            else:  # if values are anyway prefixed individually, then strip trailing 0 for readability
                return "{}{}{}".format(
                    "{:.2f}".format(response).rstrip("0").rstrip("."),
                    spacerA,
                    prefixlist[mag] + spacerB + unit,
                )
        else:
            return f"0 {unit}"
    else:
        # Since table.add.row() expects a string, try to return whatever is not yet a string but also not numeric as string
        return str(response)

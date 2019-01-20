from app import factory

VERBOSE = False


def choose_source() -> str:
    """
    Choose the CSV file from which to read sections, questions and answer
    content.
    If the user supplies an argument, look for a file at that filename (and
    complain if one doesn't exist).
    Otherwise use "Source.csv".
    # todo Use a proper argument parser in order to supply a help function.
    :return: a filename (string).
    """
    source = sys.argv[1]
    printv(f'Looking for source data in "{source}".')
    if os.path.isfile(source):
        return source
    else:
        raise Exception(f'File ("{source}") not found.')
        sys.exit()


def user_yes_no(prompt: str, default="n") -> bool:
    """
    Grab a simple yes or no from the user.
    :return: True or False.
    """
    valid_responses = {'y': True, 'n': False}
    result = default
    if VERBOSE:
        prompt += " (y/n)\n".replace(default, default.upper())
        response = input(prompt)
        if not response:
            result = default
        elif response[0].lower()in valid_responses:
            result = response
    return valid_responses[result]


def main() -> None:
    csv_source = choose_source()
    s = factory.Store(csv_source)
    printv(f"RFP Store data created successfully from {csv_source}.")
    count = "{:,}".format(s.questions_count)
    printv(count, "responses recorded.")
    if user_yes_no(f"Write HTML to {HTML_OUTFILE}?", default='y'):
        s.write_html(HTML_OUTFILE)
        printv(f"{HTML_OUTFILE} written.")
        open_file = factory.user_yes_no("Open it now in the web browser?",
                                        default='y')
        if open_file:
            webbrowser.open(HTML_OUTFILE)


if __name__ == "__main__":
    main()

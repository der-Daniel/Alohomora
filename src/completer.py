#!/usr/bin/python

# ------------------------------------------------------------------------------

# I found this snippet on stackoverflow
# source: http://stackoverflow.com/questions/7821661/how-to-code-autocompletion-in-python
# user: Shawn Chin

# ------------------------------------------------------------------------------


class TextCompleter(object):

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:
            if text:
                self.matches = [s for s in self.options
                                if s and s.startswith(text)]
            else:
                self.matches = self.options[:]
        try:
            return self.matches[state]
        except IndexError:
            return None

    def update(self, s):
        l = self.options
        l.append(s)
        l.sort()
        self.options = l

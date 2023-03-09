"""
Lizard extension that counts satd comments according to the patterns provided by http://users.encs.concordia.ca/~eshihab/pubs/Potdar_ICSME2014.pdf.
"""

HACK_PATTERNS = """hack
retarded
at a loss
stupid
remove this code
ugly
take care
something's gone wrong
nuke
is problematic
may cause problem
hacky
unknown why we ever experience this
treat this as a soft error
silly
workaround for bug
kludge
fixme
this isn't quite right
trial and error
give up
this is wrong
hang our heads in shame
temporary solution
causes issue
something bad is going on
cause for issue
this doesn't look right
is this next line safe
this indicates a more fundamental problem
temporary crutch
this can be a mess
this isn't very solid
this is temporary and will go away
is this line really safe
there is a problem
some fatal error
something serious is wrong
don't use this
get rid of this
doubt that this would work
this is bs
give up and go away
risk of this blowing up
just abandon it
prolly a bug
probably a bug
hope everything will work
toss it
barf
something bad happened
fix this crap
yuck
certainly buggy
remove me before production
you can be unhappy now
this is uncool
bail out
it doesn't work yet
crap
inconsistency
abandon all hope


"""

SATD_LINES = HACK_PATTERNS.split('\n')

from lizard import FunctionInfo
from lizard_ext.lizardnd import patch_append_method

class LizardExtension():
    FUNCTION_INFO = {"satd_comments": {"caption": " satd comments "}}
    ordering_index = 0

    def __call__(self, tokens, reader):
        if not hasattr(reader.context.current_function, "satd_comments"):
            setattr(reader.context.current_function, "satd_comments", 0)

        for token in tokens:
            comment = reader.get_comment_from_token(token)
            if comment is not None:
                if any(satd in comment for satd in SATD_LINES):
                    reader.context.current_function.satd_comments += 1
            yield token

def _init_satd_data(self, *_):
    self.satd_comments = 0

patch_append_method(_init_satd_data, FunctionInfo, "__init__")

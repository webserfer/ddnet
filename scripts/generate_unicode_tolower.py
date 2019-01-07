# Needs UnicodeData.txt and confusables.txt in the current directory.
#
# Those can be obtained from unicode.org:
# - http://www.unicode.org/Public/security/<VERSION>/confusables.txt
# - http://www.unicode.org/Public/<VERSION>/ucd/UnicodeData.txt
#
# If executed as a script, it will generate the contents of the file
# `src/base/unicode/confusables_data.h`.

import csv

UNICODEDATA_FIELDS = (
    "Value",
    "Name",
    "General_Category",
    "Canonical_Combining_Class",
    "Bidi_Class",
    "Decomposition_Type",
    "Decomposition_Mapping",
    "Numeric_Type",
    "Numeric_Mapping",
    "Bidi_Mirrored",
    "Unicode_1_Name",
    "ISO_Comment",
    "Simple_Uppercase_Mapping",
    "Simple_Lowercase_Mapping",
    "Simple_Titlecase_Mapping",
)

def unicodedata():
    with open('UnicodeData.txt') as f:
        return list(csv.DictReader(f, fieldnames=UNICODEDATA_FIELDS, delimiter=';'))

def unhex(s):
    return int(s, 16)

def generate_cases():
    ud = unicodedata()
    return [(unhex(u["Value"]), unhex(u["Simple_Lowercase_Mapping"])) for u in ud if u["Simple_Lowercase_Mapping"]]

def main():
    cases = generate_cases()

    print("""\
#include <stdint.h>

struct UPPER_LOWER
{{
\tint32_t upper;
\tint32_t lower;
}};

enum
{{
\tNUM_TOLOWER={},
}};

static const struct UPPER_LOWER tolower[NUM_TOLOWER] = {{""".format(len(cases)))
    for upper_code, lower_code in cases:
        print("\t{{{}, {}}},".format(upper_code, lower_code))
    print("};")

if __name__ == '__main__':
    main()

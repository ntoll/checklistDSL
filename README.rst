ChecklistDSL
============

Turns simple lists into webforms.

Created in preparation for the NHShackday2012.

The DSL
+++++++

Here's what it should look like::

    = A Heading =

    // A comment that isn't rendered.

    Some explanatory text at the start of the list.

    This can be several paragraphs.

    [] A single item in a checklist

    Each item immediately below belongs to this comment.
    [] Item 1
    [] Item 2
    [] Item 3

    The following items are OR'd (rather than AND'd).
    () Item 1
    () Item 2
    () Item 3

    The following items have case insensitive roles assigned to them.
    [] {doctor, nurse} Check the machine that goes ping.
    [] {patient} Give consent.
    [] {surgeon} Make the incision.
    [] {cleaner} Tidy up the gore.

    ---

    You can crete a break with three or more minus signs.

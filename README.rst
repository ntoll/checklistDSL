ChecklistDSL
============

Turns simple lists into webforms. Created in preparation for the NHShackday2012.

Setting Up
++++++++++

In the root directory of this project simply run::

    $ pip install -U requirements.txt

I prefer to do this in a virtualenv. If you don't know what a virtualenv is,
don't worry about it, simply prepend sudo to the command and enter your
password when asked so the software can install.

The DSL
+++++++

Here's what it should look like:

```
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
```

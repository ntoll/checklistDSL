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
    == A Heading ==

    Some explanatory text at the start of the list.

    This can be several paragraphs.

    * A single item with no constraints
    1 An item that needs to be done in order (first)
    2 An item that needs to be done in order (second)

    Some more explanatory text. It can go anywhere in the list.

    It's possible to choose 0-all of the following items.

    () Item A of a multiple choice
    () Item B of a multiple choice
    () Item C of a multiple choice

    It's possible to select only one of the following items:

    [] Item A in a constrained multiple choice
    [] Item B in a constrained multiple choice
    [] Item C in a constrained multiple choice

    * Another single item with no constraints. Note the indentation for nesting.

        == A Sub-heading ==

        A sub description

        () Item A in a nested multiple choice
        () Item B in a nested multiple choice
        () Item C in a nested multiple choice

    The following items have (case insensitive) roles assigned to them:

    * {doctor, nurse} Take blood pressure.
    * {patient} Give consent for something.
    * {cleaner} Wipe up the blood and gore.
```

% SNOWPLOUGH(1)
% Jérôme Belleman <Jerome.Belleman@cern.ch>
% June 2013

# NAME

snowplough – shovel off ServiceNow tickets

# SYNOPSIS

**snowplough** [**-h**] [**--configfile** *CONFIGFILE*] [**--sort**] [**--vim**] *keyword* [*keyword ...*]

**snowplough** [**-h**] [**--configfile** *CONFIGFILE*] **--fields**

**snowplough** [**-h**] [**--configfile** *CONFIGFILE*] [**--mkix** *FILE [CSVNAME]*] [**--quiet**]

# DESCRIPTION

**snowplough** is a simple-minded tool which creates indices and
body-searches vast quantities of ServiceNow tickets, which is useful to
find out how someone before you solved one particular problem. It essentially
does what the ServiceNow Web interface already offers, only with more
typing than clicking, and the UNIX way of doing things in mind so you can
subsequently grep, awk and sed away.

There are three main operations driving **snowplough**: by default,
it body-searches indices for the keywords it's supplied; the **--mkix**
switch generates indices from a ServiceNow report; the **--fields**
switch lists the available fields in the index.


# EXAMPLES

Look for tickets where the user reports his batch jobs aren't being dispatched:

```
snowplough my job isn't running
```

Look for tickets where the user reports his VO membership expired, and display
them in a Vim buffer, each ticket rolled up in a fold:

```
snowplough voms expired --vim
```

List all tickets:

```
snowplough
```

List tickets created today:

```
snowplough created:today
```

List tickets created last sunday:

```
snowplough created:last sunday
```

List tickets created between Xmas and New Year's Eve:

```
snowplough created:24 dec to 31 dec 2012
```

# GENERAL OPTIONS

**-h, --help**
:   Display a friendly help message.

**--configfile CONFIGFILE**
:   Specify a different runtime configuration file (see CONFIGURATION FILE).

# SEARCHING TICKETS

By default, **snowplough** takes any number of arguments as keywords to
look for. These are treated case-insensitively. Wildcards are supported,
as are searches by field and fuzzy dates (see the EXAMPLES).

**--sort**
:   Sort by ticket creation time.

**--vim**
:   Display found tickets with extra information in a Vim buffer. Each ticket
is enclosed in a plain Vim fold which you can open with **zo** and close
with **zc**.  Try **:help fold.txt** in Vim for a complete reference on
folds and how they will change your life.

# MKIX SWITCH

The **--mkix** switch generates indices from a CSV ServiceNow report
file. You can pass it a zip file containing such a report if you can't be
bothered to unpack it yourself.

**--csvname CSVNAME**
:   Specify a different CSV file name to be extracted from the zip file.
Currently defaults to **report.csv**.

**--quiet**
:   Keep quiet while writing indices. This would be for instance desirable,
should **--mkix** be run from a cronjob.

# FIELDS SWITCH

The **--fields** switch lists the available fields which can be used in
queries such as:

```
snowplough created:24 dec to 31 dec 2012 assignee:fred
```

# CONFIGURATION FILE

By default, **snowplough** looks for options from **/etc/snowploughrc**,
then from **~/.snowploughrc**. Any option defined in the latter will
override its value in the former. If **--configfile CONFIGFILE** is
supplied, **CONFIGFILE** will be the only configuration file considered
and options set in e.g. **/etc/snowploughrc** and **~/.snowploughrc**
will be disregarded.

The only currently understood options are the index and temporary file
directory paths:

```ini
[paths]
index = /path/to/blahdiblah # Defaults to ~/.snowplough/index
tmp   = ~/.snowplough/tmp   # Defaults to ~/.snowplough/tmp
```

# BUILDING SERVICENOW REPORTS

The whole of **snowplough** relies on the fact that ServiceNow graciously
allows anyone of us to generate CSV files which are sent by mail. Here's
how it's done.

In ServiceNow web portal, in the left pane, under
the **Reports** rollout, follow the **View / Run** link. Make a new
**Global report**. Give it a name, set the **Type** to **List** and the
**Table** to **Task [task]**. You need to select the following columns in
the following order for **snowplough** to understand the report: **Number,
Created, Short Description, Assignment group, Assigned to, Caller, GGUSID,
Description, Close notes (Internal View), Additional comments (Customer View),
Work notes (Internal View)**.  I've found it particularly relevant to filter
out the tickets by **Functional Element.Organic Unit** being your section.

Save your report and hit the **Schedule** button. Set **Users** to
e.g. yourself, tick the **Active** checkbox and adjust the schedule
according to your needs. Don't forget to set the **Type** to **CSV**.

# RETRIEVING REPORTS FROM A MAILBOX

Once your report is scheduled for being sent to a particular mailbox, the
rest is a matter of programmatically extract it to feed it to **snowplough**.
It could be convenient to have all the report mails be moved to a dedicated
folder.

Periodically retrieve the latest report from the
mailbox. Finally, have a Python script such as **shovel.py** open
the mail from the generated Maildir and extract the attachment which you
can copy to a directory for **snowplough** to pick it up.

# BUGS
Undoubtedly.

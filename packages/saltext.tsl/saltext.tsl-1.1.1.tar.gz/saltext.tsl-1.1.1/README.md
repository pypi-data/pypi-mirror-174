# tsl

saltext TSL The State Library Module

## Maintanance

Developed and maintained by www.turtletraction.com

## Overview

**T**he **S**tate **L**ibrary aims to provide a way to document state files in a consistant manner, similar to `sys.doc`. 

By adding the `DOC`section below to the top of the states file the following feature are enabled.

* State file overview
* Searchable state file estate
* Automated Variable extraction 
** Pillar
** Grains
** Include (To be added)

```
#START-DOC
# File_name: state.sls
# Author: XXXXXX
# Description:
# Grains (if applicable):
# Pillars (if applicable):
# Syntax: XXXXXX
#END-DOC
```


## Quickstart

To get started with tsl:

# Install the extention on the minion

`sudo pip install saltext.tsl`

# Test (Listing states for a specific minion included in highstate) 

`sudo '<minion>' tsl.list`

# Use sys,doc to list all tsl functions

`sudo '<minion>' sys.doc tsl`

For any queries please sedn an email to info@turtletraction


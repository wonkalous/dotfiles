#!/usr/bin/env bash
kill $(ps x | grep "\/chrome *.* --type=renderer" | awk '{print $1}')
#!/bin/osascript

on run argv
  tell application "Messages"
    set targetBuddy to ( item 1 of argv )
    set targetService to id of 1st account whose service type = iMessage
    set textMessage to ( item 2 of argv )
    set theBuddy to participant targetBuddy of account id targetService
    send textMessage to theBuddy
  end tell
end run
# GitMode
A Git mode plugin for Sublime Text 3 that uses the ShellCommand plugin to make customisation and enhancement super easy.

This plugin uses [Sublime Text ShellCommand](https://packagecontrol.io/packages/ShellCommand) to provide its functionality, and consists mainly of commands, key bindings and syntax files. This makes it incredibly easy to change and enhance the core functionality, as well as add personal preferences, without getting into too much coding.

# Why?

The [Git](https://packagecontrol.io/packages/Git) plugin is great, but:
* it relies on a great deal of code for its functionality, yet a lot of this functionality is boiler-plate and could be easily factored out; `GitMode` uses `ShellCommand` which is a factoring of this kind of boilerplate code, plus a few other features;
* relying on code for functionality, rather than configuration, makes it difficult to contribute to and to customise. This is especially frustrating for small features;
* the `Git` plugin uses slightly different terminology to Git itself, which seems unnecessary.

The [SublimeGit](https://packagecontrol.io/packages/SublimeGit) plugin is also nice, but it costs money and is not open source.

## How to use GitMode
The main point of interaction for `GitMode` is a generated buffer that contains the status of a Git repo. This buffer can be created by running the `GitMode: status` command in a project that contains a Git repo. The buffer will look something like this:

![Screenshot of the GitMode status command](https://www.evernote.com/shard/s21/sh/092a14bd-da06-4649-943e-9b54add6917f/b68858b2d9da3a4983e6da08237231cb/deep/0/*GitMode-status*---shell-command.png)

## Changelog

# 2015-01-04 (v0.1.2)

Add platform-specific blank line command. (Fixes #2.)
Remove quotes in status commands. (Fixes #3.)
Disable status command when not in a Git repo. (Closes #4.)

# 2015-01-04 (v0.1.1)

Fix file name for `messages.json`. Fixes issue #1.


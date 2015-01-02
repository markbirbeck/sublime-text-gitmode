# GitMode
A Git mode plugin for Sublime Text 3 that uses the Shell Command plugin to make customisation and enhancement super easy.

This plugin uses [Sublime Text Shell Command](https://packagecontrol.io/packages/Shell%20Command) to provide its functionality, and consists mainly of commands, key bindings and syntax files. This makes it incredibly easy to change and enhance the core functionality, as well as add personal preferences, without getting into too much coding.

# Why?

The [Git](https://packagecontrol.io/packages/Git) plugin is great, but:
* it relies on a great deal of code for its functionality, yet a lot of this functionality is boiler-plate and could be easily factored out; `GitMode` uses `Shell Command` which is a factoring of this kind of boilerplate code, plus a few other features;
* relying on code for functionality, rather than configuration, makes it difficult to contribute to and to customise. This is especially frustrating for small features;
* the `Git` plugin uses slightly different terminology to Git itself, which seems unnecessary.

The [SublimeGit](https://packagecontrol.io/packages/SublimeGit) plugin is also nice, but it costs money and is not open source.

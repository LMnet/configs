zsh
===

oh-my-zsh
=========

scm-breeze
==========

thefuck
=======

[direnv](https://direnv.net)
============================

Sublime text
============

To activate config files make a symlink for all of them:
```
ln -s '~/.configs/sublime-text-3/Preferences.sublime-settings' '~/.config/sublime-text/Packages/User/Preferences.sublime-settings'
ln -s '~/.configs/sublime-text-3/Default (Linux).sublime-keymap' '~/.config/sublime-text/Packages/User/Default (Linux).sublime-keymap'
ln -s '~/.configs/sublime-text-3/Package Control.sublime-settings' '~/.config/sublime-text/Packages/User/Package Control.sublime-settings'
ln -s '~/.configs/sublime-text-3/Pretty JSON.sublime-settings' '~/.config/sublime-text/Packages/User/Pretty JSON.sublime-settings'
```

TODO: https://packagecontrol.io/docs/syncing

MacOS
=====

```
ln -s ~/.configs/macos/DefaultKeyBinding.dict ~/Library/KeyBindings/DefaultKeyBinding.dict
```

Also see:
* https://github.com/ttscoff/KeyBindings for examples
* https://ss64.com/mac/syntax-keybindings.html for manual about bindings

### Must have apps for MacOS to make it usable

* Maccy: clipboard manager
* AltTab: normal alt-tab
* Scroll Reverser: to have different scroll types for mouse and trackpad

Scripts
=======

* `gather_files.py`
  Useful for copying files for LLMs. Makes sense to add an alias `llm-copy` for this script. Requires `uv` and python 3.12+ to run.

Other Tools
===========

* https://github.com/orf/gping
* Collection of usefult tools
# CTags

This Sublime Text package provides support for working with tags generated
by Exuberant CTags or Universal CTags.

`ctags` command is searched for on the system PATH. It works by doing a binary
search of a memory-mapped tags file, so it will work efficiently with very large
(50MB+) tags files if needed.

## Usage

This uses tag files created by the `ctags -R -f .tags` command by default
(although this can be overridden in settings).

The plugin will try to find a `.tags` file in the same directory as the
current view, walking up directories until it finds one. If it can't find one
it will offer to build one (in the directory of the current view)

If a symbol can't be found in a tags file, it will search in additional
locations that are specified in the `CTags.sublime-settings` file (see 
below).

If you are a Rubyist, you can build a Ruby Gem's tags with the following
script:

```ruby
require 'bundler'
paths = Bundler.load.specs.map(&:full_gem_path)
system("ctags -R -f .gemtags #{paths.join(' ')}")
```
# TeleIRC for Weechat

This [Weechat](https://weechat.org) script parses
[TeleIRC](https://github.com/FruitieX/teleirc) messages for easier
reading.

## Install

```
make install
```

## Options

Run `/iset` and filter by "teleirc" options.

## Nick completion

If you want nick completion (with and without `@`), add
"|%(telegram_nicklist)" to `weechat.completion.default_template`.

## Caveats

* With `weechat.look.prefix_same_nick` enabled, messages from different
  persons will appear as if they're coming from the first one that
  talked.

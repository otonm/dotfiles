# dotfiles

Personal dotfiles managed with [chezmoi](https://www.chezmoi.io/). Supports Linux and macOS.

## What's configured

| Tool | Purpose |
|------|---------|
| **Zsh** | Shell — zinit plugin manager, async plugin loading, shared history |
| **Starship** | Prompt — git status, language indicators, Catppuccin Mocha theme |
| **Tmux** | Multiplexer — `Ctrl+A` prefix, TPM plugins, status bar with Tailscale/IP widgets |
| **Ghostty** | Terminal — FiraCode Nerd Font, 95% opacity, Catppuccin Mocha theme |
| **Nano** | Editor — line numbers, soft wrap, Catppuccin Mocha theme, syntax highlighting |

### CLI tools

- **eza** — modern `ls` replacement (aliased as `ls`)
- **bat** — syntax-highlighted `cat` (aliased as `cat`)
- **fzf** — fuzzy finder with Catppuccin Mocha colors and tab-completion integration
- **tlrc** — tldr pages client

All tools use the [Catppuccin Mocha](https://catppuccin.com/) color palette.

## Applying on a new system

### 1. Install chezmoi and apply

```sh
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply otonm
```

This command installs chezmoi, clones the repo, and applies all dotfiles in one step.

### 2. Bootstrap scripts

On first apply, chezmoi automatically runs three setup scripts:

- **`run_once_00-bootstrap-dependencies`** — installs `zsh`, `tmux`, and other system packages via the platform's package manager; installs Homebrew on macOS
- **`run_once_01-install-firacode-nerd-font`** — downloads and installs FiraCode Nerd Font
- **`run_once_02-install-nano-syntax-highlighting`** — clones [galenguyer/nano-syntax-highlighting](https://github.com/galenguyer/nano-syntax-highlighting) to `~/.local/share/nano-syntax-highlighting`

### 3. Set Zsh as the default shell

Zsh is installed by the bootstrap script. To make it your default shell, run:

```sh
# Find the zsh path
which zsh

# Set it as default (replace /usr/bin/zsh with the path above if different)
chsh -s /usr/bin/zsh
```

On macOS, zsh is the default since Catalina and no action is needed.

Log out and back in for the change to take effect.

### 4. Post-install

- **Zsh plugins** — zinit downloads plugins on first shell launch
- **Tmux plugins** — TPM installs plugins on first tmux launch (or press `prefix + I`)
- **Starship** — downloaded automatically by `.zshrc` on first shell launch if not already installed

### Keeping up to date

```sh
chezmoi update
```

`.zshrc` also runs `chezmoi update` automatically in the background once per hour.

## Repository layout

```
dot_zshrc.tmpl                        → ~/.zshrc
dot_tmux.conf.tmpl                    → ~/.tmux.conf
dot_config/starship.toml              → ~/.config/starship.toml
dot_config/ghostty/config.ghostty     → ~/.config/ghostty/config.ghostty
dot_config/nano/nanorc.tmpl           → ~/.config/nano/nanorc
dot_tmux/                             → ~/.tmux/ (status bar widgets)
run_once_00-bootstrap-dependencies... → runs once on first apply
run_once_01-install-firacode-nerd...  → runs once on first apply
```

Files ending in `.tmpl` use chezmoi templates for platform-specific paths and commands (Linux vs macOS).

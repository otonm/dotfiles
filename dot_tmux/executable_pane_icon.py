#!/usr/bin/env python3
"""Maps current tmux pane command to a Nerd Font icon + label for the status bar."""

import os
import sys

# fmt: off
# Icon codepoints from Nerd Fonts v3 (FiraCode Nerd Font Mono).
# Confirmed sources: lang.py codepoints (\ue6xx-\ue7xx range), starship.toml
# symbols, and Font Awesome (\uf0xx) set included in all Nerd Fonts builds.
PROGRAMS: dict[str, tuple[str, str]] = {

    # ── Shells ────────────────────────────────────────────────────────────────
    # \uf489 = nf-dev-terminal
    "zsh":          ("\uf489", "Zsh"),
    "bash":         ("\uf489", "Bash"),
    "fish":         ("\uf489", "Fish"),
    "sh":           ("\uf489", "Shell"),
    "dash":         ("\uf489", "Shell"),
    "ksh":          ("\uf489", "Shell"),
    "tcsh":         ("\uf489", "Shell"),
    "nu":           ("\uf489", "Nu"),

    # ── Editors ───────────────────────────────────────────────────────────────
    # \ue7c5 = nf-dev-vim
    "nvim":         ("\ue7c5", "Neovim"),
    "vim":          ("\ue7c5", "Vim"),
    "vi":           ("\ue7c5", "Vi"),
    "nano":         ("\uf044", "Nano"),         # \uf044 = nf-fa-pencil_square_o
    "emacs":        ("\uf1c9", "Emacs"),        # \uf1c9 = nf-fa-file_code_o
    "hx":           ("\uf040", "Helix"),        # \uf040 = nf-fa-pencil
    "micro":        ("\uf040", "Micro"),
    "ed":           ("\uf15c", "ed"),           # \uf15c = nf-fa-file_text
    "code":         ("\ue70c", "VS Code"),      # \ue70c = nf-dev-visualstudio

    # ── System monitoring ─────────────────────────────────────────────────────
    # \U000f035b = nf-md-memory (confirmed from starship.toml memory_usage symbol)
    "htop":         ("\U000f035b", "htop"),
    "btop":         ("\U000f035b", "btop"),
    "top":          ("\U000f035b", "top"),
    "atop":         ("\U000f035b", "atop"),
    "glances":      ("\U000f035b", "Glances"),
    "iotop":        ("\U000f035b", "iotop"),
    "iftop":        ("\uf1eb", "iftop"),        # \uf1eb = nf-fa-wifi
    "bmon":         ("\uf1eb", "bmon"),
    "nmon":         ("\U000f035b", "nmon"),
    "powertop":     ("\U000f035b", "powertop"),

    # ── File managers ─────────────────────────────────────────────────────────
    # \uf07c = nf-fa-folder_open
    "ranger":       ("\uf07c", "Ranger"),
    "lf":           ("\uf07c", "lf"),
    "nnn":          ("\uf07c", "nnn"),
    "mc":           ("\uf07c", "MC"),
    "vifm":         ("\uf07c", "vifm"),
    "yazi":         ("\uf07c", "Yazi"),
    "broot":        ("\uf07c", "Broot"),

    # ── File viewing / paging ─────────────────────────────────────────────────
    # \uf15c = nf-fa-file_text
    "less":         ("\uf15c", "Less"),
    "more":         ("\uf15c", "More"),
    "most":         ("\uf15c", "Most"),
    "bat":          ("\uf15c", "Bat"),
    "cat":          ("\uf15c", "cat"),

    # ── Search tools ──────────────────────────────────────────────────────────
    # \uf002 = nf-fa-search
    "fzf":          ("\uf002", "FZF"),
    "grep":         ("\uf002", "grep"),
    "rg":           ("\uf002", "Ripgrep"),
    "fd":           ("\uf002", "fd"),
    "ag":           ("\uf002", "ag"),

    # ── Network ───────────────────────────────────────────────────────────────
    # \U000f08c0 = nf-md-ssh (U+F08C0, verified from UTF-8 F3 B0 A3 80)
    # \uf019 = nf-fa-download; \uf1eb = nf-fa-wifi (network generic)
    "ssh":          ("\U000f08c0", "SSH"),
    "scp":          ("\U000f08c0", "scp"),
    "sftp":         ("\U000f08c0", "sftp"),
    "curl":         ("\uf019", "curl"),
    "wget":         ("\uf019", "wget"),
    "ping":         ("\uf1eb", "ping"),
    "nmap":         ("\uf1eb", "nmap"),
    "nc":           ("\uf1eb", "netcat"),
    "netcat":       ("\uf1eb", "netcat"),
    "mtr":          ("\uf1eb", "mtr"),
    "dig":          ("\uf1eb", "dig"),
    "nslookup":     ("\uf1eb", "nslookup"),
    "http":         ("\uf1eb", "HTTPie"),
    "httpie":       ("\uf1eb", "HTTPie"),
    "whois":        ("\uf1eb", "whois"),
    "tcpdump":      ("\uf1eb", "tcpdump"),
    "iperf":        ("\uf1eb", "iperf"),
    "iperf3":       ("\uf1eb", "iperf3"),
    "netstat":      ("\uf1eb", "netstat"),
    "ss":           ("\uf1eb", "ss"),
    "rsync":        ("\uf021", "rsync"),        # \uf021 = nf-fa-refresh (sync)

    # ── Version control ───────────────────────────────────────────────────────
    # \ue702 = nf-dev-git; \uf09b = nf-fa-github
    "git":          ("\ue702", "Git"),
    "gh":           ("\uf09b", "GitHub CLI"),
    "lazygit":      ("\ue702", "Lazygit"),
    "svn":          ("\ue702", "SVN"),
    "hg":           ("\ue702", "Mercurial"),

    # ── Package managers ──────────────────────────────────────────────────────
    # \U000f03d7 = nf-md-package_variant (confirmed from starship.toml package symbol)
    "apt":          ("\U000f03d7", "apt"),
    "apt-get":      ("\U000f03d7", "apt-get"),
    "dpkg":         ("\U000f03d7", "dpkg"),
    "brew":         ("\U000f03d7", "Homebrew"),
    "pacman":       ("\U000f03d7", "pacman"),
    "yay":          ("\U000f03d7", "yay"),
    "paru":         ("\U000f03d7", "paru"),
    "dnf":          ("\U000f03d7", "dnf"),
    "yum":          ("\U000f03d7", "yum"),
    "zypper":       ("\U000f03d7", "zypper"),
    "emerge":       ("\U000f03d7", "emerge"),
    "npm":          ("\ue71e", "npm"),          # \ue71e = nf-dev-npm
    "yarn":         ("\ue71e", "Yarn"),
    "pnpm":         ("\ue71e", "pnpm"),
    "pip":          ("\ue606", "pip"),          # \ue606 = python (from lang.py)
    "pip3":         ("\ue606", "pip3"),
    "cargo":        ("\ue7a8", "Cargo"),        # \ue7a8 = rust (from lang.py)
    "gem":          ("\ue739", "gem"),          # \ue739 = ruby (from lang.py)
    "composer":     ("\ue73d", "Composer"),     # \ue73d = nf-dev-php
    "nix":          ("\uf313", "Nix"),          # \uf313 = nf-linux-nixos
    "nixpkgs":      ("\uf313", "nixpkgs"),

    # ── Build tools ───────────────────────────────────────────────────────────
    # \uf085 = nf-fa-cogs; \U000f0537 = nf-md-meson (confirmed from starship.toml)
    "make":         ("\uf085", "Make"),
    "cmake":        ("\uf085", "CMake"),
    "ninja":        ("\uf085", "Ninja"),
    "gradle":       ("\uf085", "Gradle"),
    "mvn":          ("\uf085", "Maven"),
    "ant":          ("\uf085", "Ant"),
    "meson":        ("\U000f0537", "Meson"),
    "bazel":        ("\uf085", "Bazel"),

    # ── Containers / Cloud ────────────────────────────────────────────────────
    # \uf308 = nf-dev-docker (from lang.py); \U000f0cfe = nf-md-kubernetes
    "docker":       ("\uf308", "Docker"),
    "podman":       ("\uf308", "Podman"),
    "kubectl":      ("\U000f0cfe", "kubectl"),
    "k9s":          ("\U000f0cfe", "k9s"),
    "helm":         ("\U000f0cfe", "Helm"),
    "terraform":    ("\uf013", "Terraform"),    # \uf013 = nf-fa-gear
    "ansible":      ("\uf013", "Ansible"),
    "vagrant":      ("\uf013", "Vagrant"),

    # ── Language runtimes ─────────────────────────────────────────────────────
    # Codepoints from lang.py (\ue6xx-\ue7xx) and starship.toml character literals.
    "python":       ("\ue606", "Python"),
    "python3":      ("\ue606", "Python"),
    "python2":      ("\ue606", "Python 2"),
    "node":         ("\ue718", "Node.js"),      # \ue718 = nf-dev-nodejs_small
    "nodejs":       ("\ue718", "Node.js"),
    "deno":         ("\ue718", "Deno"),
    "bun":          ("\ue718", "Bun"),
    "ruby":         ("\ue739", "Ruby"),
    "irb":          ("\ue739", "IRB"),
    "java":         ("\ue738", "Java"),
    "scala":        ("\ue737", "Scala"),        # \ue737 = nf-dev-scala
    "kotlin":       ("\ue634", "Kotlin"),       # \ue634 = nf-dev-kotlin
    "go":           ("\ue627", "Go"),
    "rustc":        ("\ue7a8", "Rust"),
    "perl":         ("\ue769", "Perl"),         # \ue769 = nf-dev-perl
    "php":          ("\ue73d", "PHP"),
    "lua":          ("\ue620", "Lua"),          # \ue620 = nf-dev-lua
    "julia":        ("\ue624", "Julia"),        # \ue624 = nf-dev-julia
    "swift":        ("\ue755", "Swift"),        # \ue755 = nf-dev-swift
    "elixir":       ("\ue62d", "Elixir"),       # \ue62d = nf-dev-elixir
    "erl":          ("\ue7b1", "Erlang"),       # \ue7b1 = nf-dev-erlang
    "erlang":       ("\ue7b1", "Erlang"),
    "ghc":          ("\ue777", "Haskell"),      # \ue777 = nf-dev-haskell
    "runghc":       ("\ue777", "Haskell"),
    "ocaml":        ("\ue67a", "OCaml"),        # \ue67a = nf-dev-ocaml
    "r":            ("\U000f05d4", "R"),        # confirmed from starship.toml 󰟔
    "rscript":      ("\U000f05d4", "R"),
    "elm":          ("\ue62c", "Elm"),          # \ue62c = nf-dev-elm
    "dart":         ("\ue798", "Dart"),         # \ue798 = nf-dev-dart
    "zig":          ("\ue6a9", "Zig"),          # \ue6a9 = nf-dev-zig
    "crystal":      ("\ue7b2", "Crystal"),      # \ue7b2 = nf-dev-crystal
    "dotnet":       ("\uf481", "dotnet"),       # \uf481 = nf-dev-dotnet

    # ── Database clients ──────────────────────────────────────────────────────
    # \uf1c0 = nf-fa-database; \ue76e = nf-dev-postgresql
    "mysql":        ("\uf1c0", "MySQL"),
    "psql":         ("\ue76e", "PostgreSQL"),
    "sqlite3":      ("\uf1c0", "SQLite"),
    "redis-cli":    ("\uf1c0", "Redis"),
    "mongosh":      ("\uf1c0", "MongoDB"),
    "mongo":        ("\uf1c0", "MongoDB"),
    "clickhouse":   ("\uf1c0", "ClickHouse"),

    # ── Text processing ───────────────────────────────────────────────────────
    # \uf121 = nf-fa-code
    "awk":          ("\uf121", "awk"),
    "sed":          ("\uf121", "sed"),
    "jq":           ("\uf121", "jq"),
    "yq":           ("\uf121", "yq"),

    # ── Archives ─────────────────────────────────────────────────────────────
    # \uf1c6 = nf-fa-file_archive_o
    "tar":          ("\uf1c6", "tar"),
    "zip":          ("\uf1c6", "zip"),
    "unzip":        ("\uf1c6", "unzip"),
    "gzip":         ("\uf1c6", "gzip"),
    "bzip2":        ("\uf1c6", "bzip2"),
    "xz":           ("\uf1c6", "xz"),
    "zstd":         ("\uf1c6", "zstd"),
    "7z":           ("\uf1c6", "7-Zip"),

    # ── Media ─────────────────────────────────────────────────────────────────
    # \uf03d = nf-fa-video_camera; \uf03e = nf-fa-picture_o
    "ffmpeg":       ("\uf03d", "FFmpeg"),
    "mpv":          ("\uf03d", "mpv"),
    "vlc":          ("\uf03d", "VLC"),
    "convert":      ("\uf03e", "ImageMagick"),
    "magick":       ("\uf03e", "ImageMagick"),
    "yt-dlp":       ("\uf019", "yt-dlp"),

    # ── Security ─────────────────────────────────────────────────────────────
    # \uf084 = nf-fa-key
    "gpg":          ("\uf084", "GPG"),
    "openssl":      ("\uf084", "OpenSSL"),
    "pass":         ("\uf084", "pass"),
    "bw":           ("\uf084", "Bitwarden"),
    "ssh-keygen":   ("\uf084", "ssh-keygen"),

    # ── Multiplexers ─────────────────────────────────────────────────────────
    "tmux":         ("\uf489", "Tmux"),
    "screen":       ("\uf489", "Screen"),
    "zellij":       ("\uf489", "Zellij"),

    # ── Debugging / Profiling ─────────────────────────────────────────────────
    # \uf188 = nf-fa-bug
    "gdb":          ("\uf188", "GDB"),
    "lldb":         ("\uf188", "LLDB"),
    "strace":       ("\uf188", "strace"),
    "ltrace":       ("\uf188", "ltrace"),
    "perf":         ("\uf188", "perf"),
    "valgrind":     ("\uf188", "Valgrind"),

    # ── System management ─────────────────────────────────────────────────────
    # \uf013 = nf-fa-gear
    "systemctl":    ("\uf013", "systemctl"),
    "journalctl":   ("\uf15c", "journalctl"),
    "ps":           ("\uf013", "ps"),
    "launchctl":    ("\uf013", "launchctl"),    # macOS

    # ── Documentation ─────────────────────────────────────────────────────────
    # \uf02d = nf-fa-book
    "man":          ("\uf02d", "Manual"),
    "tldr":         ("\uf02d", "tldr"),
    "info":         ("\uf02d", "info"),

    # ── AI / LLM ──────────────────────────────────────────────────────────────
    # \uf086 = nf-fa-comment (speech bubble)
    "claude":       ("\uf086", "Claude"),
    "ollama":       ("\uf086", "Ollama"),
    "aichat":       ("\uf086", "aichat"),
    "llm":          ("\uf086", "LLM"),

    # ── Utilities ────────────────────────────────────────────────────────────
    # \uf073 = nf-fa-calendar; \uf1ec = nf-fa-calculator; \uf017 = nf-fa-clock_o
    "date":         ("\uf073", "date"),
    "cal":          ("\uf073", "cal"),
    "bc":           ("\uf1ec", "bc"),
    "watch":        ("\uf017", "watch"),
    "progress":     ("\uf110", "progress"),    # \uf110 = nf-fa-spinner
}
# fmt: on

FALLBACK_ICON = "\uf120"  # nf-fa-terminal


def main() -> None:
    cmd = os.path.basename(sys.argv[1]) if len(sys.argv) > 1 else "zsh"
    icon, label = PROGRAMS.get(cmd, (FALLBACK_ICON, cmd))
    print(f"{icon}  {label}")


if __name__ == "__main__":
    main()

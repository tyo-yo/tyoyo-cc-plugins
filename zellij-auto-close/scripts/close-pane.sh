#!/bin/bash
# Close the Zellij pane when Claude Code session ends.
#
# This script is triggered by the SessionEnd hook.
# It only runs when inside a Zellij session (detected via ZELLIJ_SESSION_NAME).
#
# To avoid closing the pane on /clear or /new (which exit then restart Claude),
# we wait briefly and check if a new claude process has started from the same
# parent shell. If it has, we skip closing.

# Skip if not running inside Zellij
[ -z "$ZELLIJ_SESSION_NAME" ] && exit 0

# Walk up the process tree to find the parent shell PID
# Returns the PID of the first shell ancestor (zsh, bash, etc.)
find_shell_pid() {
    local pid=$PPID
    local depth=0
    while [ "$depth" -lt 15 ] && [ -n "$pid" ] && [ "$pid" != "0" ]; do
        local comm
        comm=$(ps -o comm= -p "$pid" 2>/dev/null | tr -d ' ')
        case "$comm" in
            zsh|-zsh|bash|-bash|fish|-fish|sh|-sh|dash)
                echo "$pid"
                return 0
                ;;
        esac
        local new_ppid
        new_ppid=$(ps -o ppid= -p "$pid" 2>/dev/null | tr -d ' ')
        [ -z "$new_ppid" ] || [ "$new_ppid" = "0" ] || [ "$new_ppid" = "$pid" ] && return 1
        pid=$new_ppid
        depth=$((depth + 1))
    done
    return 1
}

# Check if claude has restarted as a direct child of the given shell PID
check_claude_restarted() {
    local shell_pid=$1
    for child_pid in $(pgrep -P "$shell_pid" 2>/dev/null); do
        local comm
        comm=$(ps -o comm= -p "$child_pid" 2>/dev/null | tr -d ' ')
        if [ "$comm" = "claude" ]; then
            return 0
        fi
        # Also match node processes running claude (e.g. npx installs)
        local args
        args=$(ps -o args= -p "$child_pid" 2>/dev/null)
        if echo "$args" | grep -q "claude"; then
            return 0
        fi
    done
    return 1
}

SHELL_PID=$(find_shell_pid)

if [ -n "$SHELL_PID" ]; then
    # Wait briefly for Claude to restart (e.g. after /clear or /new)
    sleep 1.5
    if check_claude_restarted "$SHELL_PID"; then
        exit 0  # Claude restarted — skip closing the pane
    fi
fi

# Close the current pane
zellij action close-pane 2>/dev/null || true

exit 0

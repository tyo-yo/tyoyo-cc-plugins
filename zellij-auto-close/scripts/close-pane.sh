#!/bin/bash
# Close the Zellij pane when Claude Code session ends.
#
# This script is triggered by the SessionEnd hook.
# It only runs when inside a Zellij session (detected via ZELLIJ_SESSION_NAME).
# Uses `zellij action close-pane` to close the current pane.

# Skip if not running inside Zellij
[ -z "$ZELLIJ_SESSION_NAME" ] && exit 0

# Close the current pane
zellij action close-pane 2>/dev/null || true

exit 0

# Sourced by the existing unprivileged console/Menu; numeric uptime and fixed phases only.
pcbm_boot_start() {
  local directory=/home/pcbm/.local/state/project-cbm/boot
  [[ $EUID == 1000 ]] || return 0
  PCBM_BOOT_TRACE=$(
    umask 077
    mkdir -p "$directory" && mktemp "$directory/boot.XXXXXXXX.tsv"
  ) || PCBM_BOOT_TRACE=
  export PCBM_BOOT_TRACE
}
pcbm_boot_mark() {
  case ${1:-} in
    console_entry|setup_begin|setup_done|profiles_begin|profiles_done|startup_choice_done|primary_begin|primary_done|menu_exec|menu_entry|menu_preferences_done|status_begin|status_done|dialog_dispatch|first_input) ;;
    *) return 0 ;;
  esac
  [[ ${PCBM_BOOT_TRACE:-} == /home/pcbm/.local/state/project-cbm/boot/boot.*.tsv && -f $PCBM_BOOT_TRACE && ! -L $PCBM_BOOT_TRACE ]] || return 0
  local uptime ignored
  read -r uptime ignored < /proc/uptime || return 0
  [[ $uptime =~ ^[0-9]+\.[0-9]+$ ]] || return 0
  printf '%s\t%s\n' "$uptime" "$1" >> "$PCBM_BOOT_TRACE" || true
}

# First meaningful screen requests release; future children see EOF after release.
pcbm_boot_handoff() {
  local ready=${PCBM_BOOT_READY_FD:-} ack=${PCBM_BOOT_ACK_FD:-} answer
  [[ $ready =~ ^[0-9]+$ && $ack =~ ^[0-9]+$ ]] || return 0
  if read -r -t 0 -u "$ack"; then
    # Buffered acknowledgment or EOF after the completed supervisor handoff.
    read -r -u "$ack" answer 2>/dev/null || true
  else
    printf '1' >&"$ready" 2>/dev/null || return 1
    read -r -t 32 -u "$ack" answer 2>/dev/null || return 1
    [[ $answer == 1 ]] || return 1
  fi
  unset PCBM_BOOT_READY_FD PCBM_BOOT_ACK_FD
}

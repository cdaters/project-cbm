# Private engineering appliance; ordinary login/PAM owns both sessions.
if [ "$(id -u)" = 1000 ]; then
  HISTFILE=/dev/null
  export HISTFILE
  case "$(tty 2>/dev/null)" in
    /dev/tty1) exec /usr/libexec/project-cbm/pcbm-console-session ;;
    /dev/tty2) printf '\nProject CBM engineering diagnostics: run pcbm-diagnostics\nReturn to Menu with Ctrl+Alt+F1.\n' ;;
  esac
fi

#!/bin/sh

help() {
cat << __EOT__
Usage: jstun [--daemon] [--pidfile=FILE] PORT1 IP1 PORT2 IP2
__EOT__
}

while [ "$1" ]; do
		case "$1" in
				--daemon)
					DAEMONIZE="Yes, please do."
					;;
				--help)
					help
					exit
					;;
				--pidfile=*)
					PIDFILE=${1#--pidfile=}
					;;
				--*)
					echo "jstun: invalid option '$1'." >&2
					help
					exit 1
					;;
				*)
					ARGV="$ARGV $1"
					;;
		esac
		shift
done

. /usr/share/java-utils/java-functions

CLASSPATH=$(build-classpath jstun slf4j-api slf4j-jdk14)
MAIN_CLASS=de.javawi.jstun.test.demo.StunServer

if [ "$DAEMONIZE" ]; then
	PIDFILE=${PIDFILE:-"$(mktemp)"}
	(
		trap 'pid=$(cat '$PIDFILE' 2>/dev/null); [ "$pid" ] && kill $pid' TERM INT EXIT
		[ "$PIDFILE" ] && echo '$$' > $PIDFILE
		set_javacmd
		$JAVACMD -classpath $CLASSPATH $MAIN_CLASS $ARGV &
		PID=$!
		echo $PID > $PIDFILE
		wait $PID
		rm $PIDFILE
	) &
else
	run ${1:+"$@"}
fi

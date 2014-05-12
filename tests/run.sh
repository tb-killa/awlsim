#!/bin/sh

basedir="$(dirname "$0")"
[ "$(echo "$basedir" | cut -c1)" = '/' ] || basedir="$PWD/$basedir"

die()
{
	echo "$*"
	exit 1
}

cleanup()
{
	[ -f "$test_time_file" ] && {
		rm -f "$test_time_file"
		test_time_file=
	}
}

# $1=interpreter
# Returns version on stdout as:  MAJOR MINOR PATCHLEVEL
get_interpreter_version()
{
	local interpreter="$1"

	"$interpreter" -c 'import sys; print("%d %d %d" % sys.version_info[0:3]);' 2>/dev/null
}

# $1=interpreter $2=awl_file ($3..$x additional options to awlsimcli)
run_test()
{
	local interpreter="$1"
	local awl="$2"
	shift; shift

	# Check whether a project file with the same basename exists
	# If it exists, run that instead of the raw AWL file
	local dir="$(dirname "$awl")"
	local base="$(basename "$awl" .awl)"
	local awlpro="${dir}/${base}.awlpro"
	[ -r "$awlpro" ] && awl="$awlpro"

	echo -n "Running test '$(basename "$awl")' ..."
	command time -o "$test_time_file" -f '%E' \
	"$interpreter" "$basedir/../awlsimcli" --quiet --onecycle --extended-insns \
		--hardware dummy:inputAddressBase=7:outputAddressBase=8:dummyParam=True \
		--cycle-time 60 \
		"$@" \
		"$awl" ||\
		die "Test failed"
	echo " [$(cat "$test_time_file")]"
}

# $1=interpreter, $2=directory
run_test_directory()
{
	local interpreter="$1"
	local directory="$2"

	echo "--- Entering directory '$directory'"
	for entry in "$directory"/*; do
		[ -d "$entry" ] && continue
		[ "$(echo -n "$entry" | tail -c4)" = ".awl" ] || continue
		run_test "$interpreter" "$entry"
	done
	for entry in "$directory"/*; do
		[ -d "$entry" ] || continue
		run_test_directory "$interpreter" "$entry"
	done
	echo "--- Leaving directory '$directory'"
}

# Run coreserver tests.
# $1=interpreter
run_server_tests()
{
	local interpreter="$1"

	echo "--- Running coreserver tests"
	for testfile in shutdown.awl; do
		run_test "$interpreter" "$basedir/$testfile" \
			--spawn-backend --interpreter "$interpreter"
	done
	echo "--- Finished coreserver tests"
}

# $@=testfiles
do_tests()
{
	for interpreter in "$opt_interpreter" python2 python3 pypy pypy3 jython ipy; do
		[ -z "$interpreter" ] && continue
		which "$interpreter" >/dev/null 2>&1 || {
			echo "=== WARNING: '$interpreter' interpreter not found. Test skipped."
			echo
			[ -n "$opt_interpreter" ] && break || continue
		}

		local interp_ver="$(get_interpreter_version "$interpreter")"
		local interp_ver_dot="$(echo "$interp_ver" | tr ' ' '.')"
		local interp_major="$(echo "$interp_ver" | cut -d' ' -f 1)"
		local interp_minor="$(echo "$interp_ver" | cut -d' ' -f 2)"

		[ "$interp_major" -eq 2 -a "$interp_minor" -lt 7 ] && {
			echo "=== WARNING: '$interpreter' interpreter version '$interp_ver_dot' too old. Test skipped."
			echo
			[ -n "$opt_interpreter" ] && break || continue
		}

		echo "=== Running tests with '$interpreter' interpreter."
		if [ $# -eq 0 ]; then
			run_test_directory "$interpreter" "$basedir"
			run_server_tests "$interpreter"
		else
			for opt in "$@"; do
				if [ -d "$opt" ]; then
					run_test_directory "$interpreter" "$opt"
				else
					run_test "$interpreter" "$opt"
				fi
			done
		fi
		echo

		[ -n "$opt_interpreter" ] && break
	done
}

trap cleanup EXIT INT TERM
test_time_file="$(mktemp --tmpdir=/tmp awlsim-test-time.XXXXXX)"

opt_interpreter=

while [ $# -ge 1 ]; do
	[ "$(echo "$1" | cut -c1)" != "-" ] && break

	case "$1" in
	-i|--interpreter)
		shift
		opt_interpreter="$1"
		which "$opt_interpreter" >/dev/null 2>&1 ||\
			die "Interpreter '${opt_interpreter}' not found"
		;;
	*)
		echo "Unknown option: $1"
		exit 1
		;;
	esac
	shift
done

do_tests "$@"

exit 0

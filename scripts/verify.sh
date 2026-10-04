#!/usr/bin/env bash
# verify.sh - zero-credit build/test check with trimmed output for Copilot.
#   scripts/verify.sh                       # all modules, quiet
#   scripts/verify.sh card-api              # one module (+ modules it depends on)
#   scripts/verify.sh card-api CardServiceTest
# Exit code is the build's. On failure, prints only the useful lines (via ctx.py if present).
set -o pipefail
MODULE="$1"; TEST="$2"
if [ -x ./mvnw ]; then MVN=./mvnw; else MVN=mvn; fi
ARGS=(-q -B)
[ -n "$MODULE" ] && ARGS+=(-pl "$MODULE" -am)
[ -n "$TEST" ] && ARGS+=("-Dtest=$TEST" -Dsurefire.failIfNoSpecifiedTests=false)
LOG=$(mktemp)
"$MVN" "${ARGS[@]}" test >"$LOG" 2>&1
RC=$?
if [ $RC -eq 0 ]; then
  echo "VERIFY: PASS (${MODULE:-all modules}${TEST:+ / $TEST})"
else
  echo "VERIFY: FAIL (${MODULE:-all modules}${TEST:+ / $TEST}) - trimmed output:"
  if [ -f scripts/ctx.py ]; then python3 scripts/ctx.py trace < "$LOG" 2>/dev/null | head -80
  else grep -E "ERROR|FAIL|Exception|Caused by|expected|at .*(Test|com\.)" "$LOG" | head -80; fi
fi
rm -f "$LOG"; exit $RC

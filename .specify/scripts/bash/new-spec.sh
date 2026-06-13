#!/usr/bin/env bash
# new-spec.sh — Scaffold a new SpecKit feature folder
# Usage: bash .specify/scripts/bash/new-spec.sh 005 voice-input
set -e

ID=${1:?"Usage: $0 <id> <slug>  e.g. 005 voice-input"}
SLUG=${2:?"Usage: $0 <id> <slug>  e.g. 005 voice-input"}
DIR="specs/${ID}-${SLUG}"

mkdir -p "$DIR"

for tmpl in spec plan tasks; do
  cp ".specify/templates/${tmpl}_template.md" "$DIR/${tmpl}.md"
  sed -i "s/\[Feature Name\]/${SLUG}/g" "$DIR/${tmpl}.md"
  sed -i "s/NNN/${ID}/g" "$DIR/${tmpl}.md"
done

echo "✅ Scaffolded: $DIR"
echo "   Edit: $DIR/spec.md  → define WHAT & WHY"
echo "   Then: $DIR/plan.md  → define HOW"
echo "   Then: $DIR/tasks.md → define ordered tasks"

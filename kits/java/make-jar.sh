#!/bin/bash

ABSOLUTE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Compiling with Maven..."

mvn -f "$ABSOLUTE_PATH/pom.xml" clean compile assembly:single

echo "Done!"

echo "Moving JavaBot.jar to correct dir..."

mv "$ABSOLUTE_PATH/target/JavaBot.jar" "$ABSOLUTE_PATH/JavaBot.jar"

echo "Done!"
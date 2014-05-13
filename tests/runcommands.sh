#!/bin/bash

# This script runs the swid generator, to check for encoding problems or
# similar problems that are hard to test.

cd ..

python -m swid_generator.main swid && \
python -m swid_generator.main swid --doc-separator=" |||" && \
python -m swid_generator.main swid --full && \
python -m swid_generator.main swid --pretty && \
python -m swid_generator.main swid --pretty --full && \
\
python -m swid_generator.main swid --package bash && \
python -m swid_generator.main swid --package bash --full && \
python -m swid_generator.main swid --package bash --pretty && \
python -m swid_generator.main swid --package bash --pretty --full && \
python -m swid_generator.main swid --package bash --pretty --full --regid="regid.2014-01.foo" --entity-name="F00" && \
\
python -m swid_generator.main software-id && \
python -m swid_generator.main software-id --doc-separator=" ||| " && \
\
echo "It seems that everything went fine."

#### Pre-instructions to send script to interviewer

- Clone the GitHub repository, generate a tarball file
    - On windows, right click and zip it.
    - On Linux,
      ```
      git clone https://github.com/rvemulapati/wpengine-interview.git
      cd wpengine-interview
      tar --create --verbose --gzip --file wpengine.tar.gz .
      ```

#### Instructions to execute the script for wpengine-interview

- Install pre-requisites
  - Python3 [1]
  - pip [2]
- Download and extract the zip file
- Install dependencies
  - `pip install -r requirements.txt`
- Execute python script
  ```
  python parse_wpengine.py input.xlsx output.csv
  cat output.csv
  ```

References:
---
[1] https://www.python.org/downloads/

[2] https://pip.pypa.io/en/stable/installing/

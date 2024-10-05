# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import argparse

header = """# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

def add_license_header(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read()
        with open(filename, 'w') as f:
            f.write(header + "\n\n" + content)
        print(f"Added header to: {filename}")
    except Exception as e:
        print(f"Error processing file {filename}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Add Apache 2.0 License header to files.')
    parser.add_argument('directory', help='Directory containing the files.')
    parser.add_argument('file_extension', help='File extension to process (e.g., .py, .json)')
    args = parser.parse_args()

    for root, _, files in os.walk(args.directory):
        for file in files:
            if file.endswith(args.file_extension):
                add_license_header(os.path.join(root, file))

if __name__ == "__main__":
    main()
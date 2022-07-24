# IPGen
IPGen, a simple tool to create random IPv4 and IPv6 lists, with speed and customizability in mind.

# Usage
```sh
nexus@pop-os:~$ python3 main.py --help

Usage: main.py [-h|--help] [-a|--amount amount] [-t|--threads amount] [-s|--seed seed] [-o|--output
               file] [-b|--buffer file buffer] [-q|--quiet] [-v|--verbose] [-d|--duplicates]
               [-l|--lock] [-4|--ipv4] [-6|--ipv6]

IPGen, a simple tool to create random IPv4 and IPv6 lists, with speed and customizability in mind

Options:
  -h, --help                            show this help message and exit
  -a amount, --amount amount            Amount of IPs to generate (default: 500)
  -t amount, --threads amount           Amount of threads to use (default: 100)
  -s seed, --seed seed                  Seed to use when initializing the Random module (default:
                                        None)
  -o file, --output file                Output file to write results to (default: output.txt)
  -b file buffer, --buffer file buffer  Buffer size to use when writing IPs to output file
                                        (default: 16777216)
  -q, --quiet                           Silence the output (default: False)
  -v, --verbose                         Show extra output (default: False)
  -d, --duplicates                      Allow duplicates (default: False)
  -l, --lock                            Use a thread lock when modifying variables. Can decrease
                                        performance. (default: False)
  -4, --ipv4                            Generate IPv4 addresses (default: False)
  -6, --ipv6                            Generate IPv6 addresses (default: False)

Copyright (c) 2022 Nexus/Nexuzzzz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
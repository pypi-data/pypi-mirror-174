# MaxConsole 0.1.0

MaxConsole is a simple wrapper on top of Rich's Console class that allows you to easily create a console with a custom theme.

## Installation

### Pip

```bash
pip install maxconsole
```

### Pipx (recommended)

```bash
pipx install maxconsole
```

### Poetry

```bash
poetry add maxconsole
```

## Usage
```python
from maxconsole import get_console

console = get_console() # It's that easy.
```

## Custimization

Making your own theme isn't hard but it's nice to have one spelled out for you, without lifting a finger.

![maxconsole](maxconsole.svg)


<hr />
<div style="font-size:0.8em;color:#2e2e2e;background:#e2e2e2;padding:20px;border-radius:5px;">
    <h3>MIT License</h3>
    <p style="font-size:0.8em">Copyright (c) 2021 Max well Owen Ludden</p>
    <p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>
    <p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>
    <p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p>
</div>
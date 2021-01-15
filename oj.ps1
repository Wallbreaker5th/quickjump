$x = Split-Path -Parent $MyInvocation.MyCommand.Definition
python (Join-Path $x py/ojjump.py) $args

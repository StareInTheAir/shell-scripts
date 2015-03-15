# Change permissions recursively
Change all directory permissions to 775 and all file permissions to 644 (which is default)

```bash
find <file/dir> \( -type d -exec chmod 755 {} + \) -o \( -type f -exec chmod 644 {} + \)
```

# String starts with
```bash
while [[ "$1" == -* ]]; do
    # $1 starts with -
done
```
- [[ and == are mandatory
- no quotes araound wildcard expression

[http://tldp.org/LDP/abs/html/comparison-ops.html](http://tldp.org/LDP/abs/html/comparison-ops.html)

# RegEx
```bash
readonly REGEX="[a-fA-F0-9]+\ +(.+)"
[[ $line =~ $REGEX ]]
fileName="${BASH_REMATCH[1]}"
echo $fileName
```

# Arrays
```bash
array=("one" "two")
array+=("foo")
array+=("bar")
```

```bash
containsElement () {
    local e
    for e in "${@:2}"; do [[ "$e" == "$1" ]] && return 0; done
    return 1
}
```
```bash
$ array=("something to search for" "a string" "test2000")
$ containsElement "a string" "${array[@]}"
$ echo $?
0
$ containsElement "blaha" "${array[@]}"
$ echo $?
1
```


# Checking exit codes in if
```bash
if ! grep -q regex options; then
    printf '%s\n' 'myscript: Pattern not found!' >&2
    exit 1
fi
```

# Detect OS
```bash
if [[ "$OSTYPE" == "linux-gnu" ]]; then
        # ...
elif [[ "$OSTYPE" == "darwin"* ]]; then
        # Mac OSX
elif [[ "$OSTYPE" == "cygwin" ]]; then
        # POSIX compatibility layer and Linux environment emulation for Windows
elif [[ "$OSTYPE" == "msys" ]]; then
        # Lightweight shell and GNU utilities compiled for Windows (part of MinGW)
elif [[ "$OSTYPE" == "win32" ]]; then
        # I'm not sure this can happen.
elif [[ "$OSTYPE" == "freebsd"* ]]; then
        # ...
else
        # Unknown.
fi
```
[http://stackoverflow.com/a/8597411](http://stackoverflow.com/a/8597411)
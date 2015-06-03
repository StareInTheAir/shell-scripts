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

# String Length
```bash
${#string}
```

# RegEx
```bash
readonly REGEX="[a-fA-F0-9]+\ +(.+)"
[[ $line =~ $REGEX ]]
fileName="${BASH_REMATCH[1]}"
echo $fileName
```

# Arrays
### define
```bash
array=("one" "two")
array+=("foo")
array+=("bar")
```

### contains
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

### length
```bash
echo ${#array[@]}
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

# Terminal width / height

```bash
echo $LINES
echo $COLUMNS
```

```bash
tput cols
tput lines
```

# Funtion return value and exit code
```bash
doStuff() {
    echo "result"
    return 0
}
```

# Calculate
```bash
echo $((100 / 3))
echo "scale=5; 31.2/494" | bc
```

# Change file times

### Only change the last accessed time
touch -t -a 20110920083000 /home/user/testmsg.txt

### Only change the last modified time
touch -t -m 20110920083000 /home/user/testmsg.txt

### Change both the times - modified and accessed times
touch -t 20110920083000 /home/user/testmsg.txt

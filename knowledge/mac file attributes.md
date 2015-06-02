# Extended attributes

Indicated by @ in ```ls```

### Show extended attributes
```bash
xattr -l <dir/file>
```

### Show extended attributes recursively
```bash
xattr -rl <dir/file>
```

### Clear all extended attributes
```bash
xattr -c <dir/file>
```

### Clear all extended attributes recursively
```bash
xattr -rc <dir/file>
```

# File flags (chflags)

Indicated by nothing in ```ls```

Flags can be:

- arch
- archived
- opaque
- nodump
- sappnd
- sappend
- schg
- schange
- simmutable
- uappnd
- uappend
- uchg
- uchange
- uimmutable
- hidden

### List file flags
```bash
ls -lO <dir/file>
```

### Remove flag
```bash
chflags no<flag> <file/dir>
```

### Remove flag recursively
```bash
chflags -R no<flag> <dir>
```

### Remove flag recursively and be verbose
```bash
chflags -Rvv no<flag> <dir>
```
# Access Control List

Indicated by + in ```ls```

### List flags
```bash
ls -le
```
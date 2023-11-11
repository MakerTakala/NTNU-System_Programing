# HW4

ENV: buildpack-deps:latest on docker

## Compare size

shell code:

```shell
gcc -static -o hello_static -s hello.c /usr/lib/aarch64-linux-gnu/libc.a
echo "hello_static size:"
size hello_static

gcc -o hello_dynamic hello.c
echo "hello_dynamic size:"
size hello_dynamic
```

Result:

```
hello_static size:
   text    data     bss     dec     hex filename
 512226   22808   21840  556874   87f4a hello_static
hello_dynamic size:
   text    data     bss     dec     hex filename
   1606     624       8    2238     8be hello_dynamic
```

## Static link

Shell code:

```shell
gcc -c sayhello.c
ar rcs libfoo.a sayhello.o
gcc -static -o hello-s main.c -L. libfoo.a

echo "hello-s size:"
size hello-s

echo "libfoo.a size:"
size libfoo.a
```

Result:

```
hello-s size:
   text    data     bss     dec     hex filename
 512650   22776   21840  557266   880d2 hello-s
libfoo.a size:
   text    data     bss     dec     hex filename
    173       0       0     173      ad sayhello.o (ex libfoo.a)
```

## Dynamic link

Shell code:

```shell
export LD_LIBRARY_PATH=.
gcc -fPIC -c sayhello.c
gcc -shared sayhello.o -o libmylib.so
gcc -o hello-d main.c libmylib.so

echo "hello-d size:"
size hello-d

echo "libmylib.so size:"
size libmylib.so
```

Result:

```
hello-d size:
   text    data     bss     dec     hex filename
   1597     640       8    2245     8c5 hello-d
libmylib.so size:
   text    data     bss     dec     hex filename
   1448     568       8    2024     7e8 libmylib.so
```

## Bonus

I add a new lib saygoodbye.c

```c
#include <stdio.h>

void saygoodbye(void)
{
   printf("\033[1;32m");
   printf("static-linking library routine: Goodbye!\n");
   printf("\033[0m");
}
```

And change main.c

```c
int main(void)
{
   sayhello();
   saygoodbye();
   return(0);
}
```

Change shell to

```shell
gcc -c sayhello.c
gcc -c saygoodbye.c
ar rcs libfoo1.a sayhello.o
ar rcs libfoo2.a saygoodbye.o
gcc -static -o hello-s main.c -L. libfoo1.a libfoo2.a

echo "hello-s size:"
size hello-s

echo "libfoo1.a size:"
size libfoo1.a

echo "libfoo2.a size:"
size libfoo2.a
```

Result:

```
hello-s size:
   text    data     bss     dec     hex filename
 512746   22776   21840  557362   88132 hello-s
libfoo1.a size:
   text    data     bss     dec     hex filename
    173       0       0     173      ad sayhello.o (ex libfoo1.a)
libfoo2.a size:
   text    data     bss     dec     hex filename
    173       0       0     173      ad saygoodbye.o (ex libfoo2.a)
```

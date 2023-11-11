gcc -static -o hello_static -s hello.c /usr/lib/aarch64-linux-gnu/libc.a
echo "hello_static size:"
size hello_static

gcc -o hello_dynamic hello.c
echo "hello_dynamic size:"
size hello_dynamic
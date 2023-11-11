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
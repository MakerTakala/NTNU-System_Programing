export LD_LIBRARY_PATH=.
gcc -fPIC -c sayhello.c
gcc -shared sayhello.o -o libmylib.so
gcc -o hello-d main.c libmylib.so

echo "hello-d size:"
size hello-d

echo "libmylib.so size:"
size libmylib.so

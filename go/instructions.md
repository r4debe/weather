# Compiling and Running Go code

First you need to install Go

```shell
brew install go
```

To compile and run without generating a binary:

```shell
cd go
go run main.go
```

Very fast compilation eh?!

To compile to a binary and then run manually:

```shell
cd go
go build main.go
```

This will generate a binary `main` this can be run with

```shell
./main
```

If we want to build the binary with a different name:

```shell
cd go
go build main.go -o <name>
```

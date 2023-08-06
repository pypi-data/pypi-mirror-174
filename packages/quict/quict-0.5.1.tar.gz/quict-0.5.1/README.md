# QuICT

## How to use

### In case that you have a favor over Docker

> **CAUTIONS! Dockerfile is WIP!!!**

Though releasing images on Docker Hub is in our agenda, currently
docker users might need to build docker image from sources.
With the docker file we provide in the repository, one can easily
build a docker image with only a little performance loss. 

```
docker build -t quict .
```

### Build & Install QuICT

**Remove old version before install a new one!**

Following commands would build QuICT and install it system-wide.
You might need "sudo" privileges to install QuICT into system python package path.

> Due to a gcc issue, current version has to be built with clang++ and llvm.
> In future versions, gcc will be supported

```
export CC=clang && export CXX=clang++ && ./build.sh && ./install.sh
```

If you are encountered with permission issues during installing, try

```
export CC=clang && export CXX=clang++ && ./build.sh && ./install.sh --user
```

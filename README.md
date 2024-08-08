# cwl-graph-generate

Generates https://view.commonwl.org/ like images, showing a complete workflow in one image.

![complete workflo](https://user-images.githubusercontent.com/6304200/42953526-8f27d446-8b72-11e8-902d-b263bf881846.png)

## Example

```bash
$ CWL_FILE="<insert your favorite cwl workflow>"
$ docker build -t cwl-graph-generate .
# This command assumes the CWL and associated files are in the working directory and a subdirectory of the working directory.
$ docker run --rm -ti -v $PWD:$PWD -w $PWD cwl-graph-generate $CWL_FILE
# The output will be the basename of the $CWL_FILE.png
```

## Limitations

This project was created with the sole purpose of creating the graph above, so the code is not written from a standpoint of maintainability or stability.

## Running the Unit Tests

To run all unit tests, you can use the following command:

```sh
python3 -m unittest discover -s unit_tests


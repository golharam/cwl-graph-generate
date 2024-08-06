# cwl-graph-generate

Generates https://view.commonwl.org/ like images, showing a complete workflow in one image.

![complete workflo](https://user-images.githubusercontent.com/6304200/42953526-8f27d446-8b72-11e8-902d-b263bf881846.png)

## Example

```bash
$ CWL_FILE="<insert your favorite cwl workflow>"
$ docker build -t cwl-graph-generate .
$ docker run --rm -ti cwl-graph-generate /opt/cwl_graph_generate.py $CWL_FILE > graph
$ docker run --rm -ti cwl-graph-generate dot -Tpng graph > output.png
```

## Limitations

This project was created with the sole purpose of creating the graph above, so the code is not written from a standpoint of maintainability or stability.

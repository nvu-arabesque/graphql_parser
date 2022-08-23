This library provides simple parser for using with `dgraph` including graphql and dql (graphql+-). The goal is to auto-generate pydantic schema given definitions written in `graphql` and `dql`. The motivation is inspired by `https://www.graphql-code-generator.com/`, in which we work with `graphql` definitions and use it as a ground truth for our schemas, using which `pydantic` classes can then be generated and used for other processes.

The content is inspired by the work in https://github.com/lsmag/graphql-python/blob/master/graphql/grammar.py, please refer to the aforementioned repo for explaination regarding how this works.

> Note: this is very experimental, use with caution.

## Example
An example is provided in `.scripts/gql.py` which search for all file with extensions `.dql, .gql and .graphql` for generating its python types. From this root directory do:
```console
python3 scripts/gql.py
```
which create a file named `gql_generated_schemas.py`

## TODO

The following has not been coverred (that I can remember):

- types: interface, input, directive, enum
- inheritance
- dql
- how to deal with directives
- fragments
- due to circular class dependencies, we should add `update_forward_refs()` in the generated schemas.


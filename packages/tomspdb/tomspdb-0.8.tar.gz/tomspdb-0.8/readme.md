# tomspdb

My version of Python's pdb debugger pdb with convenience functions.

# Features

* Jump to my code and out of library code (`my`)
* Go to top and bottom of the stack (`top` and `bottom`).
* Interact with pdb object directly (`get_pdb`) useful for customizing pdb
* Interact with the frame object (`get_frame`). You can use this to look at my code
* Exclude directories from `where` to make the output more readable (`pretty_where` or `where`)

# Using

```
pip install tomspdb
python3 -m tomspdb script.py
```

# Prior work

* [This blog post](https://maurcz.github.io/posts/002-customizing-the-python-debugger/) by Mauricio R. Cruz . I found this code sample very useful
* [ipdb](https://pypi.org/project/ipdb/) and [pdbpp](https://pypi.org/project/pdbpp/) are more useful alternatives to pdb

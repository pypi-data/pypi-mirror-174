# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tkx']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tkx',
    'version': '0.1.0',
    'description': '',
    'long_description': '- [Documentation](https://piccoloser.github.io/tkx/)\n- [Development Roadmap](https://github.com/piccoloser/tkx/wiki/Development-Roadmap)\n\n# tkx (tkinter (e)xtension) *\ntkx (pronounced "tics") is a GUI library built on top of tkinter with the intention of minimizing pain while setting up user interfaces. As it stands, tkx is *heavily* under development and it could be quite a while before it reaches maturity.\n\nOne of the first ideas in the conception of tkx was implementing support for CSS, the straightforward syntax of which would make styling tkinter widgets far less painful and verbose. This will also allow developers to separate visual styles from logic.\n\nAs it stands, tkx doesn\'t change much. Here are two code examples with identical output:\n\n### Without tkx\n```python\nimport tkinter as tk\n\n\ndef main():\n    # Create a window.\n    root = tk.Tk()\n    root.title("Hello, World!")\n    root.pack_propagate(0)\n\n    # Add some text.\n    tk.Label(root, text="This is some text.").pack()\n\n    # Run the application.\n    root.mainloop()\n\n\nif __name__ == "__main__":\n    main()\n```\n*Note: `root.pack_propagate(0)` is used to prevent the window from resizing to match the size of the `tk.Label` object. This is the default behavior in tkx, as shown below.*\n\n### With tkx\n```python\nimport tkinter as tk\nimport tkx\n\n\ndef main():\n    # Create a window.\n    root = tkx.Window("Hello, World!")\n\n    # Add some text.\n    root.add(tk.Label, text="This is some text.")\n\n    # Run the application.\n    root.mainloop()\n\n\nif __name__ == "__main__":\n    main()\n```\n\nOn Windows systems, both programs above will output a window resembling the following:\n\n![Standard tkinter window with bright background and black text](../media/images/before.jpg)\n\n# CSS Stylesheets\n\nAll it takes to style elements with tkx is a CSS file and a `Stylesheet` object. Consider the following code:\n\n```python\nimport tkinter as tk\nimport tkx\n\n\ndef main():\n    # Define a stylesheet and main window.\n    stylesheet = tkx.Stylesheet("./main.css")\n    root = tkx.Window("Test!", stylesheet)\n\n    # Add a button and give it some functionality.\n    btn = root.add(tk.Button, text="Click me!")\n    btn.bind("<Button-1>", lambda _: print("Hello, World!"))\n\n    # Add some text.\n    root.add(tk.Label, text="This is text!")\n    root.add(tk.Label, text="This is some more text!")\n\n    root.mainloop()\n\n\nif __name__ == "__main__":\n    main()\n\n```\n\nAnd the following CSS stylesheet:\n\n```css\n/* main.css */\n\n:root {\n    --bg: #333;\n    --fg: #ddd;\n    --blue: #0ac;\n}\n\nWindow {\n    background: var(--bg);\n    width: 300;\n    height: 120;\n}\n\nButton {\n    background: var(--blue);\n    border-style: flat;\n    color: black;\n}\n\nLabel {\n    background: var(--bg);\n    border-style: flat;\n    border-width: 2;\n    color: var(--fg);\n}\n```\n\nThe above code outputs the following:\n\n![Dark gray window with a blue button and white text](../media/images/after.jpg)\n\n<sup>* Name is subject to change.</sup>\n',
    'author': 'Hunter Logan',
    'author_email': '_@piccoloser.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

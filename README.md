# Comics notification thing

This is the start of a web application that will notify you when comics you follow come out. You'll be notified via email and maybe through other options if they're easy and fun to implement.

To set up:

```sh
pip install -f requirements.txt
bower install
```

And in the Python shell:

```python
import comics
comics.db.create_all()
```

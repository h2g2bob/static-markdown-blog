# Simple blog generator

As used by https://dbatley.com/blog/

## Write blog posts in markdown

Put `.md` files in the `public/$YEAR/$MONTH/` directory.

## Generate a static website

Running:

```sh
./build.py
```

Generates all posts:

- html for blog posts
- an `index.html` page
- an RSS feed

## Upload to your website

Set your server location in `env.sh`, and then:

```sh
./rsync.sh
```

## Features

- Adds [opengraph](https://ogp.me/#types) title, description and image for the blog post (used by social media websites to generate nice-looking previews)
- A `htaccess` file which sets a `content-security-policy`

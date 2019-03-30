# Simple blog generator

## Write blog posts in markdown

In the `public/$YEAR/$MONTH/$WHATEVER` directory.

## Generate a static website

Running:

```sh
./build.py
```

Re-generates all posts:

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

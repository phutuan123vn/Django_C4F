# Overview
- Using Django Framework
- Database: `PostgreSQL`
- Using Django Template
- Using Jquery, Ajax and Bootstrap
---

- Basic Login and Register
- CRUD for Blog app
    - User must have an account for accessing more features
    - Can react to other post and give them your opinion
- Real - time Chat app
    - Share your invite `code` to allow others to join your `Room` and chat with them.
    - Real - time chat by utilizing `Django channels` and `Redis`
---
# Installation
- To install `Redis` you can use 
    - [tporadowski/redis](https://github.com/tporadowski/redis)
    - [memurai](https://www.memurai.com/)
    - `Docker` by following the official installation [redis](https://redis.io/kb/doc/1hcec8xg9w/how-can-i-install-redis-on-docker)
- Please edit your `settings.py` when cloning this project and `makemigrations` for first time run

---
# More
- Using `factory_boy` for generate `Fake` data
- Using `autoslug` for auto fill `slug` field in `Blog` model
- Add command to run factory script by using `factory` command in *CLI* instead of `Django Shell`
```
python manage.py factory [your file python script]
EX: python manage.py factory "./blog/factoryScripts/blogCreate.py"
```

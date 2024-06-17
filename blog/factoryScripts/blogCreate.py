from blog.factory import BlogFactory,BlogFactoryNew

for _ in range(10):
    BlogFactoryNew.create()

print("Blog created successfully")
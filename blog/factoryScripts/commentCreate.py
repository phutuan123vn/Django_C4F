from blog.factory import BlogCommentFactory


comments = []
for _ in range(150):
    BlogCommentFactory.create()

print("Comments created successfully")
